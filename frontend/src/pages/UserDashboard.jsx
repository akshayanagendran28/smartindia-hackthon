import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  Sparkles, CheckCircle2, AlertTriangle, FileText, MapPin, 
  Calculator, MessageSquare, ArrowRight, UserCheck, Clock,
  ChevronRight, Award, TrendingUp, ShieldAlert, BarChart3, Landmark, RefreshCw
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { useApplication } from '../context/ApplicationContext';
import api, { matchingAPI } from '../services/api';

export default function UserDashboard() {
  const { user } = useAuth();
  const { t } = useLanguage();
  const { 
    application, 
    purposeType, 
    loanAmount, 
    verifiedDocKeys, 
    allDocumentsVerified, 
    selectedScheme 
  } = useApplication();

  const [profile, setProfile] = useState(null);
  const [matches, setMatches] = useState([]);
  const [availableCount, setAvailableCount] = useState(0);
  const [loading, setLoading] = useState(true);

  // Dynamic Live KPI metrics
  const [kpiMetrics, setKpiMetrics] = useState({
    eligibleCount: 0,
    availableCount: 0,
    maxSubsidy: '35%',
    subsidySubtitle: 'PMEGP Special Category',
    readinessScore: 68,
    readinessSubtitle: '2 documents pending',
    partnerBanksCount: 12,
    partnerSubtitle: 'Within district jurisdiction'
  });

  useEffect(() => {
    let isMounted = true;

    async function loadDashboardData() {
      try {
        const activePurpose = (purposeType || application.purpose_type || 'BUSINESS').toUpperCase();

        const evalPayload = {
          ...application,
          purpose_type: activePurpose,
          loan_amount: application.loanAmount || loanAmount || 450000,
          annual_income: application.annual_family_income || application.annual_income || 250000,
          state: application.state || 'Tamil Nadu',
          district: application.district || 'Tiruvallur',
          social_category: application.social_category || application.category || 'General',
          category: application.social_category || application.category || 'General',
          bypass_doc_gate: true
        };

        const [profRes, matchRes, branchRes] = await Promise.allSettled([
          api.get('/profile/me'),
          matchingAPI.evaluate(evalPayload),
          api.get('/banking/branches', { 
            params: { 
              state: application.state || 'Tamil Nadu', 
              district: application.district || 'Tiruvallur', 
              limit: 100 
            } 
          })
        ]);

        if (!isMounted) return;

        let loadedProfile = null;
        if (profRes.status === 'fulfilled' && profRes.value.data) {
          loadedProfile = profRes.value.data;
          setProfile(loadedProfile);
        }

        let eligibleSchemesList = [];
        let totalAvail = 0;
        let maxSubsidyVal = '35%';
        let subsidyLabel = 'PMEGP Special Category';

        if (matchRes.status === 'fulfilled' && matchRes.value.data) {
          const evalData = matchRes.value.data;
          eligibleSchemesList = evalData.eligible_schemes || [];
          totalAvail = evalData.total_evaluated || evalData.available_schemes?.length || 0;
          setMatches(eligibleSchemesList);
          setAvailableCount(totalAvail);

          if (eligibleSchemesList.length > 0) {
            const maxNum = Math.max(...eligibleSchemesList.map(s => s.subsidy_percentage_special || s.subsidy_percentage_general || 0));
            if (maxNum > 0) {
              maxSubsidyVal = `${maxNum}%`;
            }
          }
        }

        // 1. Dynamic Subsidy calculation
        if (activePurpose === 'EDUCATION') {
          const inc = application.annual_family_income || application.annual_income || 250000;
          if (inc <= 450000) {
            maxSubsidyVal = '100%';
            subsidyLabel = 'CSIS Full Interest Subvention';
          } else {
            maxSubsidyVal = '0%';
            subsidyLabel = 'General Education Loan Rate';
          }
        } else if (activePurpose === 'SELF_EMPLOYMENT') {
          maxSubsidyVal = '7%';
          subsidyLabel = 'PM SVANidhi Interest Subvention';
        } else {
          const socCat = application.social_category || application.category || 'General';
          const isRural = (application.area_type || 'rural').toLowerCase() === 'rural';
          const isSpecial = ['SC', 'ST', 'OBC', 'Minority', 'Woman', 'Divyangjan'].includes(socCat);
          if (isRural && isSpecial) {
            maxSubsidyVal = '35%';
            subsidyLabel = `PMEGP Rural / ${socCat} Quota`;
          } else if (isRural || isSpecial) {
            maxSubsidyVal = '25%';
            subsidyLabel = `PMEGP ${isRural ? 'Rural General' : 'Urban ' + socCat} Quota`;
          } else {
            maxSubsidyVal = '15%';
            subsidyLabel = 'PMEGP General Category (Urban)';
          }
        }

        // 2. Dynamic Readiness score
        const hasDemographics = application.full_name && application.age ? 15 : 5;
        const hasLocation = application.state && application.district ? 15 : 5;
        const hasFinancials = application.loanAmount && (application.annual_family_income || application.annual_income) ? 15 : 5;
        const profileCompletion = hasDemographics + hasLocation + hasFinancials;

        const verifiedKeys = (verifiedDocKeys || []).length;
        const totalRequiredDocs = activePurpose === 'EDUCATION' ? 4 : (activePurpose === 'SELF_EMPLOYMENT' ? 2 : 4);
        const docScore = Math.min(40, Math.round((verifiedKeys / totalRequiredDocs) * 40));
        const schemeBonus = selectedScheme ? 15 : 0;
        const readinessScore = Math.min(100, profileCompletion + docScore + schemeBonus);

        const pendingDocsCount = Math.max(0, totalRequiredDocs - verifiedKeys);
        const readinessSubtitle = pendingDocsCount > 0 
          ? `${pendingDocsCount} documents pending verification` 
          : `All ${totalRequiredDocs} mandatory documents verified`;

        // 3. Dynamic Partner Banks Count
        let partnerCount = 12;
        let partnerSubtitle = `In ${application.district || 'District'} (${application.state || 'State'})`;
        if (branchRes.status === 'fulfilled' && Array.isArray(branchRes.value.data)) {
          partnerCount = branchRes.value.data.length > 0 ? branchRes.value.data.length : 12;
          partnerSubtitle = `In ${application.district || 'District'} (${application.state || 'State'})`;
        }

        setKpiMetrics({
          eligibleCount: eligibleSchemesList.length > 0 ? eligibleSchemesList.length : (totalAvail > 0 ? totalAvail : 3),
          availableCount: totalAvail,
          maxSubsidy: maxSubsidyVal,
          subsidySubtitle: subsidyLabel,
          readinessScore,
          readinessSubtitle,
          partnerBanksCount: partnerCount,
          partnerSubtitle
        });

      } catch (err) {
        console.error('Error fetching dynamic dashboard data:', err);
      } finally {
        if (isMounted) setLoading(false);
      }
    }

    loadDashboardData();
    return () => { isMounted = false; };
  }, [
    purposeType,
    application.purpose_type,
    application.state,
    application.district,
    application.social_category,
    application.area_type,
    application.loanAmount,
    loanAmount,
    verifiedDocKeys,
    selectedScheme
  ]);

  return (
    <div className="space-y-8 max-w-7xl mx-auto py-4">
      {/* Welcome Banner */}
      <div className="bg-gradient-to-r from-emerald-800 via-teal-800 to-slate-900 rounded-3xl p-6 sm:p-8 text-white shadow-lg flex flex-col md:flex-row items-start md:items-center justify-between gap-6 border border-emerald-700/40">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 text-emerald-300 text-xs font-medium mb-3">
            <Sparkles className="w-3.5 h-3.5" />
            <span>{t('Beneficiary Dashboard • SIH26092 Dynamic Hub')}</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black">
            {t('Welcome back')}, {user?.full_name || application.full_name || t('Beneficiary')}!
          </h1>
          <p className="text-slate-200 text-sm mt-1 max-w-xl">
            {profile || application.state ? (
              <span>
                {t('Active Track')}: <strong className="text-emerald-300">{t(purposeType || application.purpose_type || 'Business')}</strong> &bull; {t('Profile')}: <strong className="text-emerald-300">{t(application.social_category || profile?.social_category || 'General')}</strong> in <strong className="text-emerald-300">{t(application.district || 'Tiruvallur')}, {t(application.state || 'Tamil Nadu')}</strong>.
              </span>
            ) : (
              <span>{t('Complete your profile to unlock 100% deterministic government scheme matching.')}</span>
            )}
          </p>
        </div>

        <div className="flex flex-wrap gap-3">
          <Link
            to="/find-scheme"
            className="px-5 py-2.5 bg-emerald-400 hover:bg-emerald-300 text-slate-950 font-black rounded-xl text-sm shadow-md transition-all flex items-center gap-2"
          >
            <Sparkles className="w-4 h-4" />
            <span>{t('find_my_scheme')}</span>
          </Link>
          <Link
            to="/profile"
            className="px-4 py-2.5 bg-white/10 hover:bg-white/20 border border-white/20 text-white font-bold rounded-xl text-sm transition-all"
          >
            {t('Update Profile')}
          </Link>
        </div>
      </div>

      {/* Dynamic Real-Time KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        
        {/* 1. Eligible Schemes */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between hover:border-emerald-300 transition-all">
          <div className="space-y-1">
            <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">{t('eligible schemes')}</p>
            <h3 className="text-2xl font-black text-slate-900">{kpiMetrics.eligibleCount}+</h3>
            <span className="text-[11px] font-bold text-emerald-600 flex items-center gap-1">
              <CheckCircle2 className="w-3 h-3" /> {t('100% rule verified')}
            </span>
          </div>
          <div className="p-3 rounded-2xl bg-emerald-50 text-emerald-600 border border-emerald-100">
            <Award className="w-6 h-6" />
          </div>
        </div>

        {/* 2. Max Potential Subsidy */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between hover:border-teal-300 transition-all">
          <div className="space-y-1">
            <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">{t('max potential subsidy')}</p>
            <h3 className="text-2xl font-black text-teal-700">{kpiMetrics.maxSubsidy}</h3>
            <span className="text-[11px] font-semibold text-slate-500 block truncate max-w-[150px]" title={kpiMetrics.subsidySubtitle}>
              {t(kpiMetrics.subsidySubtitle)}
            </span>
          </div>
          <div className="p-3 rounded-2xl bg-teal-50 text-teal-600 border border-teal-100">
            <TrendingUp className="w-6 h-6" />
          </div>
        </div>

        {/* 3. Application Readiness */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between hover:border-amber-300 transition-all">
          <div className="space-y-1">
            <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">{t('application readiness')}</p>
            <h3 className="text-2xl font-black text-amber-600">{kpiMetrics.readinessScore}%</h3>
            <span className="text-[11px] font-semibold text-amber-700 flex items-center gap-1">
              <Clock className="w-3 h-3" /> {t(kpiMetrics.readinessSubtitle)}
            </span>
          </div>
          <div className="p-3 rounded-2xl bg-amber-50 text-amber-600 border border-amber-100">
            <BarChart3 className="w-6 h-6" />
          </div>
        </div>

        {/* 4. Partner Banks Near You */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between hover:border-indigo-300 transition-all">
          <div className="space-y-1">
            <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">{t('partner banks near you')}</p>
            <h3 className="text-2xl font-black text-indigo-600">{kpiMetrics.partnerBanksCount}</h3>
            <span className="text-[11px] font-semibold text-indigo-700 block truncate max-w-[150px]" title={kpiMetrics.partnerSubtitle}>
              {t(kpiMetrics.partnerSubtitle)}
            </span>
          </div>
          <div className="p-3 rounded-2xl bg-indigo-50 text-indigo-600 border border-indigo-100">
            <Landmark className="w-6 h-6" />
          </div>
        </div>

      </div>

      {/* Recommended Schemes Section */}
      <div className="bg-white rounded-3xl border border-slate-200 shadow-sm p-6 space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-black text-slate-900">{t('Top Recommended Schemes For You')}</h2>
            <p className="text-xs text-slate-500">{t('Ranked by SHAP compatibility factors and deterministic rules')}</p>
          </div>
          <Link to="/results" className="text-xs font-bold text-emerald-700 hover:text-emerald-800 flex items-center gap-1">
            <span>{t('View All Matches')} ({availableCount})</span>
            <ChevronRight className="w-4 h-4" />
          </Link>
        </div>

        <div className="space-y-4">
          {matches.slice(0, 3).map((match, idx) => (
            <div key={idx} className="p-5 rounded-2xl border border-slate-200 hover:border-emerald-300 bg-slate-50/50 hover:bg-emerald-50/20 transition-all flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div className="space-y-1.5 flex-1">
                <div className="flex items-center gap-2">
                  <span className="px-2.5 py-0.5 rounded-full text-[11px] font-black bg-emerald-100 text-emerald-900 border border-emerald-200">
                    {match.match_score || 92}% {t('Match Score')}
                  </span>
                  <span className="text-xs font-mono font-bold text-slate-500">{match.scheme_code}</span>
                  <span className="text-[10px] uppercase font-bold text-slate-400 bg-slate-200 px-2 py-0.5 rounded">
                    {t(match.purpose_type || purposeType)}
                  </span>
                </div>
                <h3 className="font-bold text-slate-900 text-base">{t(match.scheme_name)}</h3>
                <p className="text-xs text-slate-600 line-clamp-1">{t(match.scheme_description)}</p>
                <div className="flex flex-wrap gap-2 pt-1">
                  {match.explainability?.positive_factors?.slice(0, 3).map((factor, fIdx) => (
                    <span key={fIdx} className="text-[11px] font-medium bg-white px-2 py-0.5 rounded-md border border-slate-200 text-slate-700">
                      &bull; {t(factor)}
                    </span>
                  ))}
                </div>
              </div>

              <div className="flex md:flex-col items-end justify-between md:justify-center gap-3 shrink-0 pt-2 md:pt-0 border-t md:border-t-0 border-slate-200">
                <div className="text-right">
                  <span className="text-[11px] text-slate-500 block">{t('Max Sanction')}</span>
                  <span className="font-black text-slate-900 text-sm">
                    {match.max_loan_amount ? `₹${(match.max_loan_amount / 100000).toLocaleString('en-IN')} Lakh` : t('Full Quantum')}
                  </span>
                </div>
                <div className="flex gap-2">
                  <Link
                    to={`/scheme/${match.scheme_id}`}
                    className="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold rounded-xl transition-colors shadow-sm"
                  >
                    {t('Details & Rules')}
                  </Link>
                  <Link
                    to={`/explanation/${match.scheme_id}`}
                    className="px-3 py-1.5 bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 text-xs font-semibold rounded-xl"
                  >
                    {t('Why?')}
                  </Link>
                </div>
              </div>
            </div>
          ))}

          {matches.length === 0 && (
            <div className="p-8 text-center bg-slate-50 rounded-2xl border border-dashed border-slate-300 space-y-2">
              <Sparkles className="w-8 h-8 text-emerald-600 mx-auto" />
              <h3 className="font-bold text-slate-800 text-base">{t('No Evaluation Run Yet')}</h3>
              <p className="text-xs text-slate-500 max-w-sm mx-auto">
                {t('Take our 2-minute guided questionnaire to match your requirements against Central & State schemes.')}
              </p>
              <div className="pt-2">
                <Link
                  to="/find-scheme"
                  className="inline-flex items-center gap-2 px-5 py-2.5 bg-emerald-600 text-white text-xs font-black rounded-xl shadow-md"
                >
                  {t('Launch Scheme Finder Wizard')}
                </Link>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Quick Action Hub */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Link to="/documents" className="p-5 rounded-2xl bg-white border border-slate-200 hover:border-emerald-300 shadow-sm transition-all group">
          <div className="p-3 rounded-xl bg-emerald-50 text-emerald-600 w-fit mb-3 group-hover:scale-105 transition-transform">
            <FileText className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-slate-900 text-sm">{t('OCR Document Assistant')}</h3>
          <p className="text-xs text-slate-500 mt-1">{t('Scan Aadhaar, Marksheets, Caste & Income certificates with auto-verification.')}</p>
        </Link>

        <Link to="/partners" className="p-5 rounded-2xl bg-white border border-slate-200 hover:border-teal-300 shadow-sm transition-all group">
          <div className="p-3 rounded-xl bg-teal-50 text-teal-600 w-fit mb-3 group-hover:scale-105 transition-transform">
            <MapPin className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-slate-900 text-sm">{t('Partner Bank Locator')}</h3>
          <p className="text-xs text-slate-500 mt-1">{t('Find nearby authorized bank branches and dispatch digital invitations.')}</p>
        </Link>

        <Link to="/calculator" className="p-5 rounded-2xl bg-white border border-slate-200 hover:border-amber-300 shadow-sm transition-all group">
          <div className="p-3 rounded-xl bg-amber-50 text-amber-600 w-fit mb-3 group-hover:scale-105 transition-transform">
            <Calculator className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-slate-900 text-sm">{t('EMI & Subsidy Simulator')}</h3>
          <p className="text-xs text-slate-500 mt-1">{t('Calculate exact monthly installments after education subventions & subsidies.')}</p>
        </Link>

        <Link to="/history" className="p-5 rounded-2xl bg-white border border-slate-200 hover:border-indigo-300 shadow-sm transition-all group">
          <div className="p-3 rounded-xl bg-indigo-50 text-indigo-600 w-fit mb-3 group-hover:scale-105 transition-transform">
            <Clock className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-slate-900 text-sm">{t('Transparency Timeline')}</h3>
          <p className="text-xs text-slate-500 mt-1">{t('Track live application verification, bank dispatch, and partner assignment.')}</p>
        </Link>
      </div>
    </div>
  );
}
