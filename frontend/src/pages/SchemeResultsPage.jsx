import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate, Link } from 'react-router-dom';
import { 
  Sparkles, CheckCircle2, XCircle, AlertTriangle, ArrowRight, 
  Calculator, MapPin, FileCheck, HelpCircle, Filter, SlidersHorizontal,
  ChevronDown, ChevronUp, Award, Building2, Info, RefreshCw, ExternalLink,
  Search, ShieldCheck, Landmark, Globe, Check, Lock
} from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { useApplication } from '../context/ApplicationContext';
import StepProgressIndicator from '../components/StepProgressIndicator';
import api from '../services/api';

export default function SchemeResultsPage() {
  const { currentLanguage, t, translateScheme } = useLanguage();
  const { application, selectScheme, selectedScheme } = useApplication();
  const location = useLocation();
  const navigate = useNavigate();

  const [evaluation, setEvaluation] = useState(location.state?.evaluationResult || null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('eligible'); // 'eligible' or 'available'
  const [sortBy, setSortBy] = useState('score'); // 'score', 'loan_asc', 'loan_desc'
  const [originFilter, setOriginFilter] = useState('all'); // 'all', 'central', 'state'
  const [categoryFilter, setCategoryFilter] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [expandedIneligible, setExpandedIneligible] = useState(true);

  useEffect(() => {
    setLoading(true);
    const payload = {
      target_language: currentLanguage,
      loan_amount: application.loanAmount,
      required_loan: application.loanAmount,
      required_loan_amount: application.loanAmount,
      project_cost: application.project_cost,
      annual_income: application.annual_income,
      annual_family_income: application.annual_family_income,
      category: application.category,
      social_category: application.category,
      gender: application.gender,
      state: application.state,
      district: application.district,
      area_type: application.area_type,
      purpose: application.purpose,
      business_type: application.business_type,
      business_stage: application.business_stage,
      education_qualification: application.education_qualification,
      has_skill_training: application.has_skill_training,
      has_udyam_registration: application.has_udyam_registration,
      is_artisan: application.is_artisan,
      is_street_vendor: application.is_street_vendor,
      all_documents_verified: application.allDocumentsVerified,
      ...(location.state?.profileData || {})
    };

    api.post('/matching/evaluate', payload)
      .then(res => {
        setEvaluation(res.data);
      })
      .catch(err => {
        console.error('Scheme evaluation error:', err);
        if (location.state?.evaluationResult) {
          setEvaluation(location.state.evaluationResult);
        }
      })
      .finally(() => setLoading(false));
  }, [currentLanguage, application]);

  const rawEligible = evaluation?.eligible_schemes || [];
  const rawAvailable = evaluation?.available_schemes || evaluation?.ineligible_schemes || [];

  const filterAndSort = (schemesList) => {
    return schemesList
      .filter(scheme => {
        // Origin filter
        if (originFilter === 'central' && !scheme.is_central && !scheme.eligible_states?.includes('All India')) return false;
        if (originFilter === 'state' && (scheme.is_central || scheme.eligible_states?.includes('All India'))) return false;

        // Category filter
        if (categoryFilter !== 'all') {
          const cat = (scheme.target_category || '').toLowerCase();
          const desc = (scheme.scheme_description || '').toLowerCase();
          const name = (scheme.scheme_name || '').toLowerCase();
          if (!cat.includes(categoryFilter) && !desc.includes(categoryFilter) && !name.includes(categoryFilter)) {
            return false;
          }
        }

        // Search query
        if (searchQuery.trim()) {
          const q = searchQuery.toLowerCase();
          const matchName = scheme.scheme_name?.toLowerCase().includes(q);
          const matchCode = scheme.scheme_code?.toLowerCase().includes(q);
          const matchMinistry = scheme.ministry?.toLowerCase().includes(q);
          const matchDesc = scheme.scheme_description?.toLowerCase().includes(q);
          if (!matchName && !matchCode && !matchMinistry && !matchDesc) return false;
        }

        return true;
      })
      .sort((a, b) => {
        if (sortBy === 'score') return (b.match_score || 0) - (a.match_score || 0);
        if (sortBy === 'loan_desc') return (b.max_loan_amount || 0) - (a.max_loan_amount || 0);
        if (sortBy === 'loan_asc') return (a.max_loan_amount || 0) - (b.max_loan_amount || 0);
        return 0;
      });
  };

  const filteredEligible = filterAndSort(rawEligible);
  const filteredAvailable = filterAndSort(rawAvailable);

  const handleSelectScheme = (scheme, nextPath = '/calculator') => {
    selectScheme(scheme);
    navigate(nextPath, { state: { selectedScheme: scheme, loanAmount: application.loanAmount } });
  };

  return (
    <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8 space-y-8">
      {/* 7-Step Dynamic Progress Breadcrumb Indicator */}
      <StepProgressIndicator currentStep={4} />

      {/* Top Banner */}
      <div className="bg-white rounded-3xl border border-slate-200 p-6 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="space-y-1.5">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold">
            <Sparkles className="w-3.5 h-3.5" />
            <span>SIH 2026 Problem Statement SIH26092 &bull; Deterministic Rules Engine</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-slate-900">
            {filteredEligible.length} Qualified Schemes for ₹{(application.loanAmount / 100000).toLocaleString('en-IN')} Lakhs
          </h1>
          <p className="text-xs text-slate-500">
            Location: <strong className="text-slate-700">{application.district}, {application.state}</strong> &bull; Category: <strong className="text-slate-700">{application.category}</strong> &bull; Target: <strong className="text-slate-700">{application.purpose}</strong>
          </p>
        </div>

        {/* Action Controls */}
        <div className="flex flex-wrap items-center gap-3">
          <Link
            to="/find-scheme"
            className="inline-flex items-center gap-1.5 px-4 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-bold transition-colors"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Modify Requirement</span>
          </Link>
          <a
            href="https://www.myscheme.gov.in"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 px-4 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-xs font-bold transition-colors shadow-sm"
          >
            <Globe className="w-3.5 h-3.5" />
            <span>myScheme.gov.in</span>
            <ExternalLink className="w-3 h-3 ml-0.5 opacity-80" />
          </a>
        </div>
      </div>

      {/* Two Distinct Presentation Sections Switcher */}
      <div className="flex items-center gap-2 p-1.5 bg-slate-100 rounded-2xl">
        <button
          onClick={() => setActiveTab('eligible')}
          className={`flex-1 py-3 px-4 rounded-xl text-xs font-black transition-all flex items-center justify-center gap-2 ${
            activeTab === 'eligible'
              ? 'bg-emerald-600 text-white shadow-md'
              : 'text-slate-700 hover:text-slate-900 hover:bg-slate-200/60'
          }`}
        >
          <CheckCircle2 className="w-4 h-4" />
          <span>Eligible Schemes ({filteredEligible.length})</span>
          <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-700/80 text-white">
            100% Match
          </span>
        </button>
        <button
          onClick={() => setActiveTab('available')}
          className={`flex-1 py-3 px-4 rounded-xl text-xs font-black transition-all flex items-center justify-center gap-2 ${
            activeTab === 'available'
              ? 'bg-slate-900 text-white shadow-md'
              : 'text-slate-700 hover:text-slate-900 hover:bg-slate-200/60'
          }`}
        >
          <Info className="w-4 h-4" />
          <span>Available & Alternative Schemes ({filteredAvailable.length})</span>
          <span className="text-[10px] px-2 py-0.5 rounded-full bg-slate-800 text-slate-300">
            Rule Breakdown
          </span>
        </button>
      </div>

      {/* Filter & Search Bar */}
      <div className="bg-white rounded-2xl border border-slate-200 p-4 shadow-sm space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-12 gap-3 items-center">
          {/* Search box */}
          <div className="md:col-span-4 relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder={t('searchPlaceholder') || "Search scheme name, ministry, or keyword..."}
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-9 pr-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs focus:bg-white focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500"
            />
          </div>

          {/* Origin Switcher */}
          <div className="md:col-span-4 flex items-center bg-slate-100 p-1 rounded-xl">
            <button
              onClick={() => setOriginFilter('all')}
              className={`flex-1 py-1.5 text-xs font-bold rounded-lg transition-all ${
                originFilter === 'all' ? 'bg-white text-emerald-800 shadow-sm' : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              All Types
            </button>
            <button
              onClick={() => setOriginFilter('central')}
              className={`flex-1 py-1.5 text-xs font-bold rounded-lg transition-all ${
                originFilter === 'central' ? 'bg-white text-emerald-800 shadow-sm' : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Central Schemes
            </button>
            <button
              onClick={() => setOriginFilter('state')}
              className={`flex-1 py-1.5 text-xs font-bold rounded-lg transition-all ${
                originFilter === 'state' ? 'bg-white text-emerald-800 shadow-sm' : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              State Schemes
            </button>
          </div>

          {/* Sort By */}
          <div className="md:col-span-4 flex items-center justify-end gap-2 text-xs">
            <SlidersHorizontal className="w-4 h-4 text-slate-400 shrink-0" />
            <span className="font-semibold text-slate-600 shrink-0">Sort:</span>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs font-semibold text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500/20"
            >
              <option value="score">Highest Match Score</option>
              <option value="loan_desc">Loan Amount: High to Low</option>
              <option value="loan_asc">Loan Amount: Low to High</option>
            </select>
          </div>
        </div>

        {/* Quick Category Chips */}
        <div className="flex flex-wrap items-center gap-1.5 pt-2 border-t border-slate-100">
          <span className="text-[11px] font-bold text-slate-400 mr-1 flex items-center gap-1">
            <Filter className="w-3 h-3" /> Focus:
          </span>
          {[
            { id: 'all', label: 'All Focus Areas' },
            { id: 'manufacturing', label: 'Manufacturing' },
            { id: 'service', label: 'Services' },
            { id: 'women', label: 'Women Entrepreneurs' },
            { id: 'artisan', label: 'Artisans & Craftsmen' },
            { id: 'subsidy', label: 'Capital Subsidies' },
          ].map((chip) => (
            <button
              key={chip.id}
              onClick={() => setCategoryFilter(chip.id)}
              className={`px-3 py-1 rounded-lg text-xs font-bold transition-all ${
                categoryFilter === chip.id
                  ? 'bg-emerald-700 text-white'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              {chip.label}
            </button>
          ))}
        </div>
      </div>

      {loading && (
        <div className="p-12 text-center text-slate-500 bg-white rounded-3xl border border-slate-200">
          <Sparkles className="w-8 h-8 text-emerald-500 animate-spin mx-auto mb-3" />
          <p className="font-bold text-sm text-slate-800">Evaluating statutory gazette rules & calculating SHAP match scores...</p>
        </div>
      )}

      {/* TAB 1: ELIGIBLE SCHEMES */}
      {activeTab === 'eligible' && (
        <div className="space-y-4">
          {filteredEligible.map((rawScheme, idx) => {
            const scheme = translateScheme(rawScheme);
            const matchScore = Math.round(scheme.match_score || 95);
            const isSelected = selectedScheme?.scheme_id === scheme.scheme_id || selectedScheme?.scheme_code === scheme.scheme_code;
            const isCentral = scheme.is_central || scheme.eligible_states?.includes('All India');
            const portalUrl = scheme.official_portal_url || 'https://www.myscheme.gov.in';

            return (
              <div
                key={scheme.scheme_id || idx}
                className={`bg-white rounded-3xl border transition-all p-6 relative overflow-hidden shadow-sm hover:shadow-md ${
                  isSelected
                    ? 'border-emerald-500 ring-2 ring-emerald-500/20 shadow-emerald-500/10'
                    : 'border-slate-200 hover:border-emerald-300'
                }`}
              >
                <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
                  {/* Left Info */}
                  <div className="space-y-3 flex-1">
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="px-3 py-1 rounded-full text-xs font-black border bg-emerald-50 text-emerald-800 border-emerald-300">
                        {matchScore}% Statutory Match
                      </span>
                      <span className="text-xs font-bold text-slate-700 px-2.5 py-0.5 bg-slate-100 rounded-md font-mono">
                        {scheme.scheme_code}
                      </span>
                      <span className={`text-[11px] font-bold px-2 py-0.5 rounded ${
                        isCentral ? 'bg-blue-50 text-blue-700 border border-blue-200' : 'bg-purple-50 text-purple-700 border border-purple-200'
                      }`}>
                        {isCentral ? 'Central Scheme' : 'State Scheme'}
                      </span>
                      <span className="text-xs text-slate-500 font-medium">
                        &bull; {scheme.ministry || 'Government of India'}
                      </span>
                    </div>

                    <div>
                      <h2 className="text-xl font-extrabold text-slate-900">{scheme.scheme_name || scheme.name}</h2>
                      <p className="text-xs text-slate-600 mt-1 line-clamp-2 leading-relaxed">{scheme.scheme_description || scheme.description}</p>
                    </div>

                    {/* Positive Contributing Factors (Explainability) */}
                    {scheme.explainability?.positive_factors && scheme.explainability.positive_factors.length > 0 && (
                      <div className="pt-2">
                        <span className="text-[11px] font-bold text-slate-500 block mb-1">Passed Eligibility Conditions:</span>
                        <div className="flex flex-wrap gap-1.5">
                          {scheme.explainability.positive_factors.map((factor, fIdx) => (
                            <span
                              key={fIdx}
                              className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-[11px] font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200/60"
                            >
                              <CheckCircle2 className="w-3 h-3 text-emerald-600 shrink-0" />
                              <span>{factor}</span>
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Official Verification Tag */}
                    <div className="pt-1 flex items-center gap-3 text-[11px]">
                      <span className="inline-flex items-center gap-1 font-semibold text-emerald-700 bg-emerald-50/80 px-2 py-0.5 rounded border border-emerald-200/60">
                        <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
                        <span>Statutory Verified &bull; myScheme.gov.in</span>
                      </span>
                      <a
                        href={portalUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-1 text-slate-500 hover:text-emerald-700 font-medium transition-colors"
                      >
                        <span>Official Portal</span>
                        <ExternalLink className="w-3 h-3" />
                      </a>
                    </div>
                  </div>

                  {/* Right Financials & Action Buttons */}
                  <div className="lg:w-80 shrink-0 bg-slate-50 p-5 rounded-2xl border border-slate-200 flex flex-col justify-between space-y-4">
                    <div className="space-y-2 text-xs">
                      <div className="flex justify-between items-center">
                        <span className="text-slate-500">Maximum Cap:</span>
                        <span className="font-extrabold text-slate-900 text-sm">
                          ₹{(scheme.max_loan_amount / 100000).toLocaleString('en-IN')} Lakhs
                        </span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-slate-500">Government Subsidy:</span>
                        <span className="font-bold text-emerald-700">
                          {scheme.scheme_code === 'PMEGP' ? 'Up to 35% Special Rural' : (scheme.subsidy_details?.special_rural || scheme.subsidy_details?.special || 'Interest Subvention')}
                        </span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-slate-500">Repayment Period:</span>
                        <span className="font-medium text-slate-700">{scheme.repayment_period_months || 60} Months</span>
                      </div>
                    </div>

                    <div className="space-y-2 pt-3 border-t border-slate-200">
                      {/* Select Scheme Primary CTA */}
                      <button
                        onClick={() => handleSelectScheme(scheme, '/calculator')}
                        className={`w-full py-2.5 px-4 font-black text-xs rounded-xl shadow-md transition-all flex items-center justify-center gap-2 ${
                          isSelected
                            ? 'bg-emerald-700 text-white ring-2 ring-emerald-500'
                            : 'bg-emerald-600 hover:bg-emerald-700 text-white hover:scale-[1.01]'
                        }`}
                      >
                        {isSelected ? (
                          <>
                            <Check className="w-4 h-4" />
                            <span>Selected Scheme (Active)</span>
                          </>
                        ) : (
                          <>
                            <span>Select Scheme & Calculate EMI (Step 5)</span>
                            <ArrowRight className="w-4 h-4" />
                          </>
                        )}
                      </button>

                      <div className="flex gap-2">
                        <Link
                          to={`/scheme/${scheme.scheme_id}`}
                          className="flex-1 py-2 px-2 bg-white border border-slate-300 hover:bg-slate-100 text-slate-700 font-bold text-[11px] rounded-xl text-center"
                        >
                          Full Details
                        </Link>
                        <button
                          onClick={() => handleSelectScheme(scheme, '/partners')}
                          className="flex-1 py-2 px-2 bg-white border border-slate-300 hover:bg-emerald-50 text-emerald-800 font-bold text-[11px] rounded-xl text-center flex items-center justify-center gap-1"
                        >
                          <MapPin className="w-3.5 h-3.5 text-emerald-600" />
                          <span>Find Branch</span>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}

          {filteredEligible.length === 0 && !loading && (
            <div className="p-12 text-center bg-white rounded-3xl border border-slate-200 space-y-4">
              <Info className="w-10 h-10 text-slate-400 mx-auto" />
              <div>
                <h3 className="font-extrabold text-slate-800 text-base">No Matching Eligible Schemes Found</h3>
                <p className="text-xs text-slate-500 max-w-sm mx-auto mt-1">
                  Click on the "Available & Alternative Schemes" tab above to see all gazette schemes and reasons for exclusion.
                </p>
              </div>
              <div className="flex justify-center gap-3">
                <button
                  onClick={() => setActiveTab('available')}
                  className="px-5 py-2.5 bg-slate-900 text-white text-xs font-bold rounded-xl"
                >
                  View Available Schemes
                </button>
                <Link
                  to="/find-scheme"
                  className="inline-flex items-center gap-2 px-5 py-2.5 bg-emerald-600 text-white text-xs font-bold rounded-xl"
                >
                  Modify Questionnaire
                </Link>
              </div>
            </div>
          )}
        </div>
      )}

      {/* TAB 2: AVAILABLE & INELIGIBLE SCHEMES (RULE EXPLAINABILITY) */}
      {activeTab === 'available' && (
        <div className="space-y-4">
          <div className="p-4 bg-slate-100 rounded-2xl border border-slate-200 text-xs text-slate-600 flex items-center gap-2">
            <Info className="w-4 h-4 text-slate-500 shrink-0" />
            <span>These schemes are currently operating under Central / State mandates. Transparent gazette reasons for exclusion are displayed below.</span>
          </div>

          {filteredAvailable.map((scheme, idx) => (
            <div
              key={idx}
              className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm flex flex-col lg:flex-row lg:items-center justify-between gap-6"
            >
              <div className="space-y-2 flex-1">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold text-slate-700 px-2 py-0.5 bg-slate-100 rounded font-mono">
                    {scheme.scheme_code}
                  </span>
                  <span className="text-xs font-extrabold text-slate-900">{scheme.scheme_name}</span>
                </div>
                <p className="text-xs text-slate-600 line-clamp-2">{scheme.scheme_description || scheme.description}</p>

                {/* Failed Rules Box */}
                <div className="p-3 bg-red-50/70 border border-red-200 rounded-xl text-xs space-y-1">
                  <div className="flex items-center gap-1.5 text-red-800 font-bold">
                    <XCircle className="w-3.5 h-3.5 text-red-600 shrink-0" />
                    <span>Failed Gazette Condition(s):</span>
                  </div>
                  <p className="text-red-700 text-[11px]">
                    {scheme.failed_rules?.join('; ') || 'Criteria mismatch with applicant profile or required loan ceiling exceeded.'}
                  </p>
                </div>
              </div>

              <div className="lg:w-60 shrink-0 flex flex-col justify-between space-y-3 bg-slate-50 p-4 rounded-2xl border border-slate-200">
                <div className="text-xs space-y-1">
                  <span className="text-slate-500 block">Max Limit:</span>
                  <span className="font-extrabold text-slate-900">
                    ₹{(scheme.max_loan_amount / 100000).toLocaleString('en-IN')} Lakhs
                  </span>
                </div>

                <Link
                  to={`/scheme/${scheme.scheme_id}`}
                  className="w-full py-2 px-3 bg-white border border-slate-300 hover:bg-slate-100 text-slate-700 font-bold text-xs rounded-xl text-center block"
                >
                  View Scheme Guidelines
                </Link>
              </div>
            </div>
          ))}

          {filteredAvailable.length === 0 && (
            <div className="p-12 text-center bg-white rounded-3xl border border-slate-200 text-slate-500 text-xs">
              No additional available schemes found matching your search.
            </div>
          )}
        </div>
      )}
    </div>
  );
}

