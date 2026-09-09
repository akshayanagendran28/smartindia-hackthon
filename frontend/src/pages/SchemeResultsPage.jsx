import React, { useState, useEffect } from 'react';
import { useLocation, Link } from 'react-router-dom';
import { 
  Sparkles, CheckCircle2, XCircle, AlertTriangle, ArrowRight, 
  Calculator, MapPin, FileCheck, HelpCircle, Filter, SlidersHorizontal,
  ChevronDown, ChevronUp, Award, Building2, Info, RefreshCw, ExternalLink,
  Search, ShieldCheck, Landmark, Globe
} from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import api from '../services/api';

export default function SchemeResultsPage() {
  const { currentLanguage, t, translateScheme } = useLanguage();
  const location = useLocation();
  const [evaluation, setEvaluation] = useState(location.state?.evaluationResult || null);
  const [loading, setLoading] = useState(false);
  const [sortBy, setSortBy] = useState('score'); // 'score', 'loan_asc', 'loan_desc'
  const [originFilter, setOriginFilter] = useState('all'); // 'all', 'central', 'state'
  const [categoryFilter, setCategoryFilter] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [expandedIneligible, setExpandedIneligible] = useState(false);

  useEffect(() => {
    setLoading(true);
    api.post('/matching/evaluate', {
      target_language: currentLanguage,
      ...(location.state?.profileData || {})
    })
      .then(res => setEvaluation(res.data))
      .catch(err => {
        console.error(err);
        if (location.state?.evaluationResult) setEvaluation(location.state.evaluationResult);
      })
      .finally(() => setLoading(false));
  }, [currentLanguage, location.state]);

  const rawEligible = evaluation?.eligible_schemes || [];
  const ineligibleSchemes = evaluation?.ineligible_schemes || [];

  const filteredSchemes = rawEligible
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

  return (
    <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 space-y-6">
      {/* Top Banner */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold mb-2">
            <Sparkles className="w-3.5 h-3.5" />
            <span>{t('sihBadgeText')} • {t('translationBadge')}</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-slate-900">
            {filteredSchemes.length} {t('resultsTitle')}
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            {t('resultsSubtitle')}
          </p>
        </div>

        {/* Action Controls */}
        <div className="flex flex-wrap items-center gap-3">
          <Link
            to="/find-scheme"
            className="inline-flex items-center gap-1.5 px-4 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-bold transition-colors"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>{t('btnRecalculate')}</span>
          </Link>
          <a
            href="https://www.myscheme.gov.in"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 px-4 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-xs font-bold transition-colors shadow-sm"
          >
            <Globe className="w-3.5 h-3.5" />
            <span>{t('mySchemePortal')}</span>
            <ExternalLink className="w-3 h-3 ml-0.5 opacity-80" />
          </a>
        </div>
      </div>

      {/* Filter & Search Bar */}
      <div className="bg-white rounded-2xl border border-slate-200 p-4 shadow-sm space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-12 gap-3 items-center">
          {/* Search box */}
          <div className="md:col-span-4 relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder={t('searchPlaceholder')}
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
              {t('filterAll')} ({rawEligible.length})
            </button>
            <button
              onClick={() => setOriginFilter('central')}
              className={`flex-1 py-1.5 text-xs font-bold rounded-lg transition-all ${
                originFilter === 'central' ? 'bg-white text-emerald-800 shadow-sm' : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              {t('filterCentral')}
            </button>
            <button
              onClick={() => setOriginFilter('state')}
              className={`flex-1 py-1.5 text-xs font-bold rounded-lg transition-all ${
                originFilter === 'state' ? 'bg-white text-emerald-800 shadow-sm' : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              {t('filterState')}
            </button>
          </div>

          {/* Sort By */}
          <div className="md:col-span-4 flex items-center justify-end gap-2 text-xs">
            <SlidersHorizontal className="w-4 h-4 text-slate-400 shrink-0" />
            <span className="font-semibold text-slate-600 shrink-0">{t('sortByScore').split(' ')[0]}:</span>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs font-semibold text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500/20"
            >
              <option value="score">{t('sortByScore')}</option>
              <option value="loan_desc">{t('sortByLoanDesc')}</option>
              <option value="loan_asc">{t('sortByLoanAsc')}</option>
            </select>
          </div>
        </div>

        {/* Quick Category Chips */}
        <div className="flex flex-wrap items-center gap-1.5 pt-2 border-t border-slate-100">
          <span className="text-[11px] font-bold text-slate-400 mr-1 flex items-center gap-1">
            <Filter className="w-3 h-3" /> Focus:
          </span>
          {[
            { id: 'all', label: 'All Sectors' },
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
        <div className="p-12 text-center text-slate-500 bg-white rounded-2xl border border-slate-200">
          <Sparkles className="w-8 h-8 text-emerald-500 animate-spin mx-auto mb-3" />
          <p className="font-semibold text-sm">Evaluating gazette rules and generating SHAP-style explainability scores...</p>
        </div>
      )}

      {/* Eligible Schemes Grid */}
      <div className="space-y-4">
        {filteredSchemes.map((rawScheme, idx) => {
          const scheme = translateScheme(rawScheme);
          const matchScore = Math.round(scheme.match_score || 85);
          const scoreColor = matchScore >= 80 
            ? 'text-emerald-700 bg-emerald-50 border-emerald-300' 
            : 'text-teal-700 bg-teal-50 border-teal-300';
          const isCentral = scheme.is_central || scheme.eligible_states?.includes('All India');
          const portalUrl = scheme.official_portal_url || 'https://www.myscheme.gov.in';

          return (
            <div
              key={scheme.scheme_id || idx}
              className="bg-white rounded-2xl border border-slate-200 hover:border-emerald-300 shadow-sm hover:shadow-md transition-all p-6 relative overflow-hidden"
            >
              <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
                {/* Left Info */}
                <div className="space-y-3 flex-1">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className={`px-3 py-1 rounded-full text-xs font-black border ${scoreColor}`}>
                      {matchScore}% {t('schemeMatchScore')}
                    </span>
                    <span className="text-xs font-bold text-slate-700 px-2.5 py-0.5 bg-slate-100 rounded-md font-mono">
                      {scheme.scheme_code}
                    </span>
                    <span className={`text-[11px] font-bold px-2 py-0.5 rounded ${
                      isCentral ? 'bg-blue-50 text-blue-700 border border-blue-200' : 'bg-purple-50 text-purple-700 border border-purple-200'
                    }`}>
                      {isCentral ? t('filterCentral') : t('filterState')}
                    </span>
                    <span className="text-xs text-slate-500 font-medium">
                      &bull; {scheme.ministry || 'Government of India'}
                    </span>
                  </div>

                  <div>
                    <h2 className="text-xl font-extrabold text-slate-900">{scheme.scheme_name || scheme.name}</h2>
                    <p className="text-xs text-slate-600 mt-1 line-clamp-2 leading-relaxed">{scheme.scheme_description || scheme.description}</p>
                  </div>

                  {/* Positive Contributing Factors */}
                  {scheme.explainability?.positive_factors && scheme.explainability.positive_factors.length > 0 && (
                    <div className="pt-2">
                      <span className="text-[11px] font-bold text-slate-500 block mb-1">{t('positiveFactors')}:</span>
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

                  {/* Missing Documents Alert if any */}
                  {scheme.missing_documents && scheme.missing_documents.length > 0 && (
                    <div className="flex items-center gap-2 text-[11px] text-amber-700 bg-amber-50 px-3 py-1.5 rounded-lg border border-amber-200/60">
                      <AlertTriangle className="w-3.5 h-3.5 shrink-0" />
                      <span>{t('limitingFactors')}: <strong>{scheme.missing_documents.join(', ')}</strong></span>
                      <Link to="/documents" className="font-bold underline ml-auto text-amber-900">{t('navDocAssistant')}</Link>
                    </div>
                  )}

                  {/* myScheme Verification badge with direct external link */}
                  <div className="pt-1 flex items-center gap-3 text-[11px]">
                    <span className="inline-flex items-center gap-1 font-semibold text-emerald-700 bg-emerald-50/80 px-2 py-0.5 rounded border border-emerald-200/60">
                      <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
                      <span>{t('sihBadgeText')} • myScheme.gov.in</span>
                    </span>
                    <a
                      href={portalUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 text-slate-500 hover:text-emerald-700 font-medium transition-colors"
                    >
                      <span>{t('mySchemePortal')}</span>
                      <ExternalLink className="w-3 h-3" />
                    </a>
                  </div>
                </div>

                {/* Right Financials & Action Buttons */}
                <div className="lg:w-72 shrink-0 bg-slate-50 p-4 rounded-xl border border-slate-200 flex flex-col justify-between space-y-4">
                  <div className="space-y-2 text-xs">
                    <div className="flex justify-between items-center">
                      <span className="text-slate-500">{t('maxLoan')}:</span>
                      <span className="font-extrabold text-slate-900 text-sm">
                        ₹{(scheme.max_loan_amount / 100000).toLocaleString('en-IN')} {t('unitLakh')}
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-slate-500">{t('subsidyRate')}:</span>
                      <span className="font-bold text-emerald-700">
                        {scheme.scheme_code === 'PMEGP' ? t('specialRural') : (scheme.subsidy_details?.special_rural || scheme.subsidy_details?.special || t('lowInterest'))}
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-slate-500">{t('tenor')}:</span>
                      <span className="font-medium text-slate-700">{scheme.repayment_period_months || 60} {t('unitMonths')}</span>
                    </div>
                  </div>

                  <div className="space-y-2 pt-2 border-t border-slate-200">
                    <Link
                      to={`/scheme/${scheme.scheme_id}`}
                      className="w-full py-2 px-3 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs rounded-lg shadow-sm transition-colors text-center block"
                    >
                      {t('btnViewDetails')}
                    </Link>

                    <div className="flex gap-1.5">
                      <Link
                        to={`/explanation/${scheme.scheme_id}`}
                        state={{ schemeData: scheme, evaluationResult: evaluation }}
                        className="flex-1 py-1.5 px-2 bg-white border border-slate-300 hover:bg-slate-100 text-slate-700 font-semibold text-[11px] rounded-lg text-center flex items-center justify-center gap-1"
                        title="Explainable SHAP breakdown"
                      >
                        <HelpCircle className="w-3.5 h-3.5 text-blue-600" />
                        <span>{t('btnWhyEligible')}</span>
                      </Link>

                      <Link
                        to="/calculator"
                        state={{ loanAmount: scheme.max_loan_amount, interestRate: 8.5 }}
                        className="flex-1 py-1.5 px-2 bg-white border border-slate-300 hover:bg-slate-100 text-slate-700 font-semibold text-[11px] rounded-lg text-center flex items-center justify-center gap-1"
                      >
                        <Calculator className="w-3.5 h-3.5 text-amber-600" />
                        <span>{t('navEmi')}</span>
                      </Link>

                      <Link
                        to="/partners"
                        state={{ schemeCode: scheme.scheme_code }}
                        className="flex-1 py-1.5 px-2 bg-white border border-slate-300 hover:bg-slate-100 text-slate-700 font-semibold text-[11px] rounded-lg text-center flex items-center justify-center gap-1"
                      >
                        <MapPin className="w-3.5 h-3.5 text-emerald-600" />
                        <span>{t('navPartners')}</span>
                      </Link>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          );
        })}

        {filteredSchemes.length === 0 && !loading && (
          <div className="p-12 text-center bg-white rounded-2xl border border-slate-200">
            <Info className="w-8 h-8 text-slate-400 mx-auto mb-2" />
            <h3 className="font-bold text-slate-800 text-base">No Matching Schemes Found</h3>
            <p className="text-xs text-slate-500 max-w-sm mx-auto mt-1">
              Try changing your filter criteria or search keyword to view other Central and State schemes.
            </p>
            <div className="mt-4 flex justify-center gap-3">
              <button
                onClick={() => { setOriginFilter('all'); setCategoryFilter('all'); setSearchQuery(''); }}
                className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-lg"
              >
                Reset Filters
              </button>
              <Link
                to="/find-scheme"
                className="inline-flex items-center gap-2 px-5 py-2 bg-emerald-600 text-white text-xs font-bold rounded-lg"
              >
                Modify Questionnaire
              </Link>
            </div>
          </div>
        )}
      </div>

      {ineligibleSchemes.length > 0 && (
        <div className="bg-slate-50 rounded-2xl border border-slate-200 overflow-hidden">
          <button
            onClick={() => setExpandedIneligible(!expandedIneligible)}
            className="w-full p-5 flex items-center justify-between text-left hover:bg-slate-100/80 transition-colors"
          >
            <div className="flex items-center gap-2">
              <XCircle className="w-5 h-5 text-red-500" />
              <div>
                <h3 className="font-bold text-slate-900 text-sm">
                  {ineligibleSchemes.length} Schemes Ineligible for Current Profile
                </h3>
                <p className="text-xs text-slate-500">Transparently view gazette rules that caused exclusion</p>
              </div>
            </div>
            {expandedIneligible ? <ChevronUp className="w-5 h-5 text-slate-400" /> : <ChevronDown className="w-5 h-5 text-slate-400" />}
          </button>

          {expandedIneligible && (
            <div className="p-5 pt-0 space-y-3 border-t border-slate-200 bg-white">
              {ineligibleSchemes.map((scheme, idx) => (
                <div key={idx} className="p-4 rounded-xl border border-red-100 bg-red-50/30 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
                  <div>
                    <span className="font-bold text-slate-800">{scheme.scheme_name}</span>
                    <span className="text-slate-500 ml-2 font-mono">({scheme.scheme_code})</span>
                    <div className="text-red-700 mt-1 font-medium">
                      <strong>Failed Gazette Rules:</strong> {scheme.failed_rules?.join('; ') || 'Criteria mismatch with profile'}
                    </div>
                  </div>
                  <Link
                    to={`/explanation/${scheme.scheme_id}`}
                    state={{ schemeData: scheme }}
                    className="shrink-0 px-3 py-1.5 bg-white border border-red-200 text-red-700 rounded-lg font-semibold hover:bg-red-50"
                  >
                    View Rule Breakdown
                  </Link>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
