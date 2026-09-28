import React, { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import { 
  Sparkles, CheckCircle2, AlertTriangle, FileText, MapPin, 
  Calculator, MessageSquare, ArrowRight, UserCheck, Clock,
  ChevronRight, Award, TrendingUp, ShieldAlert, BarChart3, 
  Landmark, RefreshCw, Calendar, DollarSign, Send, Check,
  Radio, Bell, ShieldCheck, CheckCircle, Phone, ArrowUpRight
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
  const [refreshing, setRefreshing] = useState(false);
  const [myApplications, setMyApplications] = useState([]);
  const [selectedAppIndex, setSelectedAppIndex] = useState(0);
  const [lastSyncedTime, setLastSyncedTime] = useState(new Date().toLocaleTimeString('en-IN'));

  // Dynamic Live KPI metrics
  const [kpiMetrics, setKpiMetrics] = useState({
    eligibleCount: 0,
    availableCount: 0,
    maxSubsidy: '0%',
    subsidySubtitle: 'Scheme matching pending',
    readinessScore: 0,
    readinessSubtitle: 'No documents uploaded',
    partnerBanksCount: 0,
    partnerSubtitle: 'Local branches'
  });

  const loadDashboardData = async (isManual = false) => {
    try {
      if (isManual) setRefreshing(true);
      const activePurpose = (purposeType || application.purpose_type || 'BUSINESS').toUpperCase();

      const evalPayload = {
        ...application,
        purpose_type: activePurpose,
        loan_amount: application.loanAmount || loanAmount || 450000,
        annual_income: application.annual_family_income || application.annual_income || 250000,
        state: application.state || user?.state || 'Maharashtra',
        district: application.district || user?.district || 'Mumbai',
        social_category: application.social_category || application.category || profile?.social_category || 'SC',
        gender: application.gender || profile?.gender || 'female',
        age: application.age || profile?.age || 28
      };

      const [profRes, branchRes, myAppsRes] = await Promise.allSettled([
        api.get('/profile/me'),
        api.get('/banking/branches', { 
          params: { 
            state: application.state || user?.state || '', 
            district: application.district || user?.district || '', 
            limit: 100 
          } 
        }),
        api.get('/applications/my-applications')
      ]);

      const profData = profRes.status === 'fulfilled' ? profRes.value.data : null;
      if (profData) {
        setProfile(profData);
      }

      if (myAppsRes.status === 'fulfilled' && myAppsRes.value.data) {
        setMyApplications(myAppsRes.value.data || []);
      }

      let eligibleSchemesList = [];
      let totalAvail = 0;
      let maxSubsidyVal = '0%';
      let subsidyLabel = 'Complete profile to calculate subsidy';

      const userAge = application.age || profData?.age;
      const userState = application.state || profData?.state || user?.state;
      const userLoan = application.loanAmount || loanAmount || application.required_loan || profData?.required_loan;

      if (userAge && userState && userLoan) {
        const evalPayload = {
          ...application,
          purpose_type: activePurpose,
          loan_amount: Number(userLoan) || 0,
          required_loan: Number(userLoan) || 0,
          annual_income: application.annual_family_income || application.annual_income || profData?.annual_family_income || 0,
          state: userState,
          district: application.district || profData?.district || user?.district || '',
          social_category: application.social_category || application.category || profData?.social_category || 'SC',
          gender: application.gender || profData?.gender || 'female',
          age: Number(userAge) || 0,
          bypass_doc_gate: true
        };

        try {
          const matchRes = await matchingAPI.evaluate(evalPayload);
          if (matchRes.data) {
            const evalData = matchRes.data;
            eligibleSchemesList = evalData.eligible_schemes || [];
            totalAvail = evalData.total_evaluated || evalData.available_schemes?.length || 0;
            setMatches(eligibleSchemesList);
            setAvailableCount(totalAvail);

            if (eligibleSchemesList.length > 0) {
              const maxNum = Math.max(...eligibleSchemesList.map(s => s.subsidy_percentage_special || s.subsidy_percentage_general || 0));
              if (maxNum > 0) {
                maxSubsidyVal = `${maxNum}%`;
                subsidyLabel = 'Maximum eligible subsidy';
              }
            }
          }
        } catch (err) {
          console.warn('Dashboard matching evaluation failed:', err);
        }
      } else {
        setMatches([]);
        setAvailableCount(0);
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
        const socCat = application.social_category || application.category || profile?.social_category || 'SC';
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
      const verifiedCount = (verifiedDocKeys || []).length;
      let totalRequired = 6;
      if (activePurpose === 'EDUCATION') totalRequired = 6;
      if (activePurpose === 'SELF_EMPLOYMENT') totalRequired = 4;

      let score = 0;
      let readinessSub = 'No documents uploaded';
      if (verifiedCount > 0) {
        score = Math.round((verifiedCount / totalRequired) * 100);
        if (score > 100) score = 100;
        readinessSub = `${totalRequired - verifiedCount} documents pending`;
      }
      if (allDocumentsVerified) {
        score = 100;
        readinessSub = '100% Ready for Bank Sanction';
      } else if (score >= 70) {
        readinessSub = 'Mandatory KYC complete';
      }

      // 3. Dynamic Nearby Partner Bank Desks
      let nearbyCount = 0;
      if (branchRes.status === 'fulfilled' && branchRes.value.data) {
        nearbyCount = branchRes.value.data.total_branches ?? branchRes.value.data.total ?? (branchRes.value.data.branches?.length || 0);
      }

      setKpiMetrics({
        eligibleCount: eligibleSchemesList.length,
        availableCount: totalAvail,
        maxSubsidy: maxSubsidyVal,
        subsidySubtitle: subsidyLabel,
        readinessScore: score,
        readinessSubtitle: readinessSub,
        partnerBanksCount: nearbyCount,
        partnerSubtitle: `Within ${application.district || user?.district || 'district'} jurisdiction`
      });

      setLastSyncedTime(new Date().toLocaleTimeString('en-IN'));

    } catch (err) {
      console.error('Error loading dashboard data:', err);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  // Initial load
  useEffect(() => {
    loadDashboardData();
  }, [purposeType, verifiedDocKeys, allDocumentsVerified]);

  // Real-time Background Polling every 6 seconds for instant loan status reflection
  useEffect(() => {
    const interval = setInterval(() => {
      // Background silent sync
      api.get('/applications/my-applications')
        .then(res => {
          if (res.data && Array.isArray(res.data)) {
            setMyApplications(res.data);
            setLastSyncedTime(new Date().toLocaleTimeString('en-IN'));
          }
        })
        .catch(err => console.debug('Background status polling:', err));
    }, 6000);

    return () => clearInterval(interval);
  }, []);

  const activeApp = myApplications?.[selectedAppIndex] || myApplications?.[0];

  return (
    <div className="space-y-8 max-w-7xl mx-auto py-4 font-sans text-slate-900">
      
      {/* Citizen Welcome Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-emerald-950 to-slate-900 text-white rounded-3xl p-6 sm:p-8 shadow-xl relative overflow-hidden border border-slate-800">
        <div className="absolute -right-10 -bottom-10 w-72 h-72 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />
        
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="space-y-2">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 text-xs font-bold uppercase tracking-wider border border-emerald-500/30">
              <ShieldAlert className="w-3.5 h-3.5" />
              <span>{t('Government-Verified Scheme Intelligence')}</span>
            </div>
            
            <h1 className="text-2xl sm:text-3xl font-black tracking-tight text-white">
              {t('Welcome')}, {user?.full_name || 'Citizen Beneficiary'} 👋
            </h1>
            
            <p className="text-slate-300 text-xs sm:text-sm max-w-2xl leading-relaxed">
              {profile || application.state || user?.state ? (
                <span>
                  {t('Active Track')}: <strong className="text-emerald-300">{t(purposeType || application.purpose_type || profile?.purpose || 'Business')}</strong> &bull; {t('Profile')}: <strong className="text-emerald-300">{profile?.social_category || application.social_category || 'SC'}</strong> in <strong className="text-emerald-300">{profile?.district || application.district || user?.district || 'Mumbai'}, {profile?.state || application.state || user?.state || 'Maharashtra'}</strong>.
                </span>
              ) : (
                <span>{t('Complete your profile to unlock 100% deterministic government scheme matching.')}</span>
              )}
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <Link
              to="/find-scheme"
              className="px-5 py-2.5 bg-emerald-400 hover:bg-emerald-300 text-slate-950 font-black rounded-xl text-sm shadow-md transition-all flex items-center gap-2 cursor-pointer"
            >
              <Sparkles className="w-4 h-4" />
              <span>{t('find_my_scheme')}</span>
            </Link>
            <Link
              to="/profile"
              className="px-4 py-2.5 bg-white/10 hover:bg-white/20 border border-white/20 text-white font-bold rounded-xl text-sm transition-all cursor-pointer"
            >
              {t('Update Profile')}
            </Link>
          </div>
        </div>
      </div>

      {/* LIVE APPLICATION STATUS & REAL-TIME TRANSACTION TRACKER */}
      {activeApp && (
        <div className="bg-white rounded-3xl p-6 sm:p-8 border-2 border-emerald-300 shadow-xl space-y-6 animate-in fade-in relative overflow-hidden">
          
          {/* Top Real-Time Connection Ribbon */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-slate-100">
            <div className="flex items-center gap-2.5">
              <span className="flex h-3 w-3 relative">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
              </span>
              <span className="text-xs font-black uppercase tracking-wider text-emerald-800">
                Real-Time Loan &amp; Subsidy Transaction Stream
              </span>
              <span className="text-[11px] text-slate-400 font-mono hidden md:inline">
                (Last synced: {lastSyncedTime})
              </span>
            </div>

            <div className="flex items-center gap-2">
              {myApplications.length > 1 && (
                <select
                  value={selectedAppIndex}
                  onChange={(e) => setSelectedAppIndex(Number(e.target.value))}
                  className="px-3 py-1.5 rounded-xl border border-slate-200 text-xs font-bold bg-slate-50 text-slate-700 outline-none"
                >
                  {myApplications.map((app, idx) => (
                    <option key={app.id} value={idx}>
                      App {idx + 1}: {app.scheme_code || 'Scheme'} ({app.application_number})
                    </option>
                  ))}
                </select>
              )}

              <button
                onClick={() => loadDashboardData(true)}
                disabled={refreshing}
                className="px-3 py-1.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-xs flex items-center gap-1.5 transition-all cursor-pointer"
                title="Force refresh status from government database"
              >
                <RefreshCw className={`w-3.5 h-3.5 ${refreshing ? 'animate-spin text-emerald-600' : ''}`} />
                <span>Sync Now</span>
              </button>

              <Link
                to="/history"
                className="px-3.5 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs flex items-center gap-1 shadow-sm transition-all"
              >
                <span>Full Audit Trail</span>
                <ChevronRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          </div>

          {/* Active Application Main Header */}
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 text-white p-6 rounded-2xl shadow-lg">
            <div className="space-y-1.5">
              <div className="flex flex-wrap items-center gap-2">
                <span className="font-mono text-xs font-black bg-emerald-400/20 text-emerald-300 px-2.5 py-0.5 rounded-lg border border-emerald-400/30">
                  {activeApp.application_number}
                </span>
                <span className="px-2.5 py-0.5 rounded-full text-[10px] font-black uppercase tracking-wider bg-white/10 text-white border border-white/20">
                  {activeApp.status}
                </span>
                <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-indigo-500/20 text-indigo-300">
                  {activeApp.purpose_type || 'BUSINESS'}
                </span>
              </div>

              <h2 className="text-xl sm:text-2xl font-black text-white">
                {activeApp.scheme_name} ({activeApp.scheme_code})
              </h2>

              <p className="text-xs text-slate-300 flex flex-wrap items-center gap-3 pt-1">
                <span>Sanction Quantum: <strong className="text-emerald-300 font-mono">₹{(activeApp.loan_amount || 0).toLocaleString('en-IN')}</strong></span>
                <span>&bull;</span>
                <span>Govt Subsidy: <strong className="text-amber-300 font-mono">₹{(activeApp.fund_amount || activeApp.subsidy_amount || 0).toLocaleString('en-IN')}</strong></span>
                <span>&bull;</span>
                <span>Interest: <strong className="text-slate-200">{activeApp.interest_rate || 8.5}% p.a.</strong></span>
              </p>
            </div>

            {/* Quick Action / Contact Partner Desk */}
            <div className="flex flex-col sm:items-end gap-2 shrink-0">
              <div className="text-left sm:text-right">
                <span className="text-[10px] uppercase font-bold text-slate-400 block tracking-wider">Nodal Partner Desk</span>
                <span className="font-bold text-emerald-300 text-sm block">{activeApp.partner_name || 'Awaiting Partner Invitation'}</span>
                {activeApp.partner_branch && <span className="text-[11px] text-slate-400 block">{activeApp.partner_branch}</span>}
              </div>
            </div>
          </div>

          {/* 4 Live Lifecycle Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            
            {/* Card 1: Loan Appraisal & Sanction */}
            <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-2 hover:border-emerald-300 transition-all">
              <div className="flex items-center justify-between">
                <span className="text-[10px] uppercase font-bold text-slate-400 tracking-wider">1. Loan Sanction Stage</span>
                <span className={`w-2.5 h-2.5 rounded-full ${
                  activeApp.loan_status === 'APPROVED' || activeApp.loan_status === 'SANCTIONED'
                    ? 'bg-emerald-500 animate-pulse'
                    : activeApp.loan_status === 'UNDER_REVIEW'
                    ? 'bg-amber-500 animate-pulse'
                    : activeApp.loan_status === 'REJECTED'
                    ? 'bg-rose-500'
                    : 'bg-slate-400'
                }`} />
              </div>
              <div>
                <span className={`font-black text-sm block ${
                  activeApp.loan_status === 'APPROVED' || activeApp.loan_status === 'SANCTIONED'
                    ? 'text-emerald-700'
                    : activeApp.loan_status === 'UNDER_REVIEW'
                    ? 'text-amber-700'
                    : activeApp.loan_status === 'REJECTED'
                    ? 'text-rose-700'
                    : 'text-slate-800'
                }`}>
                  {activeApp.loan_status}
                </span>
                <p className="text-[11px] text-slate-500 mt-0.5">
                  {activeApp.loan_status === 'APPROVED' || activeApp.loan_status === 'SANCTIONED'
                    ? 'Formal credit sanction letter issued by nodal bank branch.'
                    : activeApp.loan_status === 'UNDER_REVIEW'
                    ? 'Branch appraisal in progress.'
                    : activeApp.loan_status === 'REJECTED'
                    ? 'Application was not feasible under current guidelines.'
                    : 'Awaiting branch appraisal initiation.'}
                </p>
              </div>
            </div>

            {/* Card 2: Govt Margin Subsidy & Fund Release */}
            <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-2 hover:border-emerald-300 transition-all">
              <div className="flex items-center justify-between">
                <span className="text-[10px] uppercase font-bold text-slate-400 tracking-wider">2. Margin Subsidy Status</span>
                <span className={`w-2.5 h-2.5 rounded-full ${
                  activeApp.fund_status === 'RELEASED'
                    ? 'bg-emerald-500'
                    : activeApp.fund_status === 'PROCESSING' || activeApp.fund_status === 'APPROVED'
                    ? 'bg-indigo-500 animate-pulse'
                    : activeApp.fund_status === 'ON_HOLD'
                    ? 'bg-amber-500'
                    : 'bg-slate-400'
                }`} />
              </div>
              <div>
                <span className={`font-black text-sm block ${
                  activeApp.fund_status === 'RELEASED'
                    ? 'text-emerald-700'
                    : activeApp.fund_status === 'PROCESSING' || activeApp.fund_status === 'APPROVED'
                    ? 'text-indigo-700'
                    : activeApp.fund_status === 'ON_HOLD'
                    ? 'text-amber-700'
                    : 'text-slate-800'
                }`}>
                  {activeApp.fund_status}
                </span>
                <p className="text-[11px] text-slate-500 mt-0.5">
                  {activeApp.fund_amount > 0 ? (
                    <strong className="text-emerald-700">₹{activeApp.fund_amount.toLocaleString('en-IN')} Approved grant</strong>
                  ) : (
                    'Calculated based on affirmative category quota.'
                  )}
                  {activeApp.fund_release_date && <span className="block text-[10px] text-slate-400 mt-0.5">Released: {new Date(activeApp.fund_release_date).toLocaleDateString('en-IN')}</span>}
                </p>
              </div>
            </div>

            {/* Card 3: Partner Desk & Verification */}
            <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-2 hover:border-emerald-300 transition-all">
              <div className="flex items-center justify-between">
                <span className="text-[10px] uppercase font-bold text-slate-400 tracking-wider">3. Bank Desk Verification</span>
                <CheckCircle2 className={`w-3.5 h-3.5 ${activeApp.partner_name ? 'text-emerald-600' : 'text-slate-400'}`} />
              </div>
              <div>
                <span className="font-black text-sm text-slate-900 block truncate">
                  {activeApp.partner_name || 'No Partner Assigned'}
                </span>
                <p className="text-[11px] text-slate-500 mt-0.5">
                  {activeApp.partner_phone ? `Helpline: ${activeApp.partner_phone}` : 'District Lead Bank Coordination'}
                </p>
              </div>
            </div>

            {/* Card 4: Physical Appointment Desk */}
            <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-2 hover:border-emerald-300 transition-all">
              <div className="flex items-center justify-between">
                <span className="text-[10px] uppercase font-bold text-slate-400 tracking-wider">4. Physical Appointment</span>
                <Calendar className={`w-3.5 h-3.5 ${activeApp.appointment_status === 'SCHEDULED' ? 'text-indigo-600' : 'text-slate-400'}`} />
              </div>
              <div>
                <span className={`font-black text-sm block ${
                  activeApp.appointment_status === 'SCHEDULED'
                    ? 'text-indigo-700'
                    : activeApp.appointment_status === 'COMPLETED'
                    ? 'text-emerald-700'
                    : 'text-slate-800'
                }`}>
                  {activeApp.appointment_status}
                </span>
                <p className="text-[11px] text-slate-500 mt-0.5 truncate" title={activeApp.appointment_venue || ''}>
                  {activeApp.appointment_date 
                    ? `${new Date(activeApp.appointment_date).toLocaleDateString('en-IN')} (${activeApp.appointment_time || '10:30 AM'})` 
                    : 'No desk visit scheduled yet'}
                </p>
              </div>
            </div>

          </div>

          {/* SPECIAL ACTION PASS: When Appointment is Scheduled */}
          {activeApp.appointment_status === 'SCHEDULED' && (
            <div className="p-5 rounded-2xl bg-gradient-to-r from-indigo-900 via-indigo-950 to-slate-900 text-white space-y-3 border border-indigo-700 shadow-md">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <div className="flex items-center gap-3">
                  <div className="p-2.5 rounded-xl bg-indigo-500/20 text-indigo-300 border border-indigo-400/30">
                    <Calendar className="w-6 h-6" />
                  </div>
                  <div>
                    <h4 className="font-black text-base text-white">📅 Official Branch Verification Appointment Confirmed</h4>
                    <p className="text-xs text-indigo-200">
                      Date: <strong>{new Date(activeApp.appointment_date).toLocaleDateString('en-IN')}</strong> &bull; Time Window: <strong>{activeApp.appointment_time || '10:30 AM - 1:00 PM'}</strong>
                    </p>
                  </div>
                </div>

                <span className="px-3 py-1 rounded-full bg-indigo-400 text-slate-950 font-black text-xs uppercase self-start sm:self-auto">
                  Confirmed Pass
                </span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-2 border-t border-indigo-800 text-xs">
                <div>
                  <span className="text-indigo-300 block font-bold">Venue Branch Address:</span>
                  <span className="text-white font-medium">{activeApp.appointment_venue || 'District Lead Bank Office Desk'}</span>
                </div>
                <div>
                  <span className="text-indigo-300 block font-bold">Important Instructions for Citizen:</span>
                  <span className="text-slate-200">
                    {activeApp.appointment_remarks || 'Please bring original Aadhaar, PAN, Caste Certificate, and Project Report.'}
                  </span>
                </div>
              </div>
            </div>
          )}

          {/* SPECIAL ALERT: When Subsidy is Released */}
          {activeApp.fund_status === 'RELEASED' && (
            <div className="p-5 rounded-2xl bg-emerald-900 text-white space-y-2 border border-emerald-700 shadow-md">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2.5">
                  <CheckCircle className="w-6 h-6 text-emerald-300 shrink-0" />
                  <div>
                    <h4 className="font-black text-base text-white">🎉 Government Margin Subsidy Disbursed!</h4>
                    <p className="text-xs text-emerald-200">
                      Subsidy amount of <strong>₹{(activeApp.fund_amount || 0).toLocaleString('en-IN')}</strong> has been credited to your nodal bank branch escrow account.
                    </p>
                  </div>
                </div>
                <span className="px-3 py-1 rounded-full bg-emerald-300 text-emerald-950 font-black text-xs uppercase">
                  Disbursed
                </span>
              </div>
              {activeApp.fund_remarks && (
                <p className="text-xs text-emerald-100 bg-emerald-950/60 p-2.5 rounded-xl border border-emerald-800 font-medium">
                  <strong>Nodal Release Remarks:</strong> {activeApp.fund_remarks}
                </p>
              )}
            </div>
          )}

          {/* Interactive 5-Stage Live Milestones */}
          <div className="space-y-3 pt-2">
            <h3 className="text-xs font-black uppercase text-slate-400 tracking-wider">Live Transaction Progress Milestones</h3>
            
            <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 text-xs">
              <div className="p-3 rounded-2xl bg-emerald-50 text-emerald-900 border border-emerald-200 space-y-1">
                <div className="flex items-center gap-1.5 font-bold">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                  <span>1. Submitted</span>
                </div>
                <p className="text-[10px] text-emerald-700">Dossier confirmed</p>
              </div>

              <div className="p-3 rounded-2xl bg-emerald-50 text-emerald-900 border border-emerald-200 space-y-1">
                <div className="flex items-center gap-1.5 font-bold">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                  <span>2. Docs Verified</span>
                </div>
                <p className="text-[10px] text-emerald-700">OCR gate cleared</p>
              </div>

              <div className={`p-3 rounded-2xl space-y-1 border ${
                activeApp.partner_name ? 'bg-emerald-50 text-emerald-900 border-emerald-200' : 'bg-slate-50 text-slate-500 border-slate-200'
              }`}>
                <div className="flex items-center gap-1.5 font-bold">
                  {activeApp.partner_name ? <CheckCircle2 className="w-4 h-4 text-emerald-600" /> : <Clock className="w-4 h-4 text-slate-400" />}
                  <span>3. Bank Desk</span>
                </div>
                <p className="text-[10px] text-slate-600 truncate">{activeApp.partner_name || 'Pending Invite'}</p>
              </div>

              <div className={`p-3 rounded-2xl space-y-1 border ${
                activeApp.loan_status === 'APPROVED' || activeApp.loan_status === 'SANCTIONED'
                  ? 'bg-emerald-50 text-emerald-900 border-emerald-200'
                  : activeApp.loan_status === 'UNDER_REVIEW'
                  ? 'bg-amber-50 text-amber-900 border-amber-200'
                  : 'bg-slate-50 text-slate-500 border-slate-200'
              }`}>
                <div className="flex items-center gap-1.5 font-bold">
                  {activeApp.loan_status === 'APPROVED' || activeApp.loan_status === 'SANCTIONED' ? (
                    <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                  ) : (
                    <Clock className="w-4 h-4 text-amber-600" />
                  )}
                  <span>4. Loan Sanction</span>
                </div>
                <p className="text-[10px] text-slate-600">
                  {activeApp.loan_status === 'APPROVED' ? 'Credit Approved' : activeApp.loan_status === 'SANCTIONED' ? 'Sanctioned' : 'Appraisal'}
                </p>
              </div>

              <div className={`p-3 rounded-2xl space-y-1 border col-span-2 sm:col-span-1 ${
                activeApp.fund_status === 'RELEASED'
                  ? 'bg-emerald-50 text-emerald-900 border-emerald-200'
                  : activeApp.fund_status === 'PROCESSING' || activeApp.fund_status === 'APPROVED'
                  ? 'bg-indigo-50 text-indigo-900 border-indigo-200'
                  : 'bg-slate-50 text-slate-500 border-slate-200'
              }`}>
                <div className="flex items-center gap-1.5 font-bold">
                  {activeApp.fund_status === 'RELEASED' ? (
                    <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                  ) : (
                    <Clock className="w-4 h-4 text-indigo-600" />
                  )}
                  <span>5. Subsidy Escrow</span>
                </div>
                <p className="text-[10px] text-slate-600">
                  {activeApp.fund_status === 'RELEASED' ? 'Funds Released' : activeApp.fund_status === 'APPROVED' ? 'Approved for Release' : 'Pending Sanction'}
                </p>
              </div>
            </div>
          </div>

          {/* Live Step Audit Trail Stream (Last 3 events) */}
          {activeApp.status_history?.length > 0 && (
            <div className="pt-2 border-t border-slate-100 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">
                  Real-Time Event Stream ({activeApp.status_history.length} events logged)
                </span>
                <Link to="/history" className="text-xs font-bold text-emerald-700 hover:text-emerald-800">
                  View Full History &rarr;
                </Link>
              </div>

              <div className="space-y-2">
                {activeApp.status_history.slice(-2).reverse().map((h, idx) => (
                  <div key={idx} className="flex items-start gap-3 text-xs bg-slate-50 p-3 rounded-xl border border-slate-200/70">
                    <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 mt-1 shrink-0" />
                    <div className="flex-1">
                      <div className="flex items-center justify-between">
                        <span className="font-black text-slate-900">{h.title || h.status}</span>
                        <span className="text-[10px] text-slate-400 font-mono">
                          {h.timestamp ? new Date(h.timestamp).toLocaleString('en-IN') : ''}
                        </span>
                      </div>
                      <p className="text-slate-600 text-[11px] mt-0.5">{h.description}</p>
                      <span className="text-[10px] font-bold text-indigo-700 block mt-1">
                        Updated by: {h.updated_by} ({h.actor_role || 'ADMIN'})
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

        </div>
      )}

      {/* Dynamic Real-Time KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        
        {/* 1. Eligible Schemes */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between hover:border-emerald-300 transition-all">
          <div className="space-y-1">
            <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">{t('eligible schemes')}</p>
            <h3 className="text-2xl font-black text-slate-900">{kpiMetrics.eligibleCount > 0 ? kpiMetrics.eligibleCount : 0}</h3>
            <span className="text-[11px] font-bold text-emerald-600 flex items-center gap-1">
              <CheckCircle2 className="w-3.5 h-3.5" /> {t('100% rule verified')}
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
              <Clock className="w-3.5 h-3.5" /> {t(kpiMetrics.readinessSubtitle)}
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

        {loading ? (
          <div className="p-12 text-center text-slate-400 text-xs flex flex-col items-center justify-center gap-2">
            <RefreshCw className="w-6 h-6 animate-spin text-emerald-600" />
            <span>{t('Evaluating Government Gazette rules...')}</span>
          </div>
        ) : matches.length === 0 ? (
          <div className="p-8 text-center text-slate-500 bg-slate-50 rounded-2xl text-xs space-y-3">
            <p>{t('No exact matches found for your current profile filters. Try adjusting loan quantum or track.')}</p>
            <Link to="/find-scheme" className="px-4 py-2 bg-emerald-600 text-white font-bold rounded-xl text-xs inline-block">
              {t('Explore Questionnaire')}
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {matches.slice(0, 3).map((scheme, idx) => (
              <div 
                key={scheme.id || idx}
                className="p-5 rounded-2xl border border-slate-200 hover:border-emerald-300 hover:shadow-md transition-all flex flex-col justify-between space-y-4 bg-white"
              >
                <div className="space-y-2.5">
                  <div className="flex items-start justify-between gap-2">
                    <span className="font-mono text-xs font-black px-2 py-0.5 rounded bg-emerald-50 text-emerald-800 border border-emerald-200">
                      {scheme.code}
                    </span>
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-slate-100 text-slate-700">
                      {scheme.purpose_type || 'MSME'}
                    </span>
                  </div>

                  <h3 className="font-black text-slate-900 text-sm leading-snug">
                    {scheme.name}
                  </h3>

                  <p className="text-xs text-slate-500 line-clamp-2">
                    {scheme.description}
                  </p>
                </div>

                <div className="pt-3 border-t border-slate-100 flex items-center justify-between">
                  <div>
                    <span className="text-[10px] text-slate-400 uppercase font-bold block">Max Quantum</span>
                    <span className="font-black text-slate-900 text-xs font-mono">
                      ₹{(scheme.max_loan_amount || 1000000).toLocaleString('en-IN')}
                    </span>
                  </div>

                  <Link
                    to={`/scheme/${scheme.code || scheme.id}`}
                    className="px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs flex items-center gap-1 shadow-sm transition-all"
                  >
                    <span>{t('View Scheme')}</span>
                    <ChevronRight className="w-3.5 h-3.5" />
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

    </div>
  );
}
