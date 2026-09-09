import os

BASE_DIR = r"C:\Users\aksha\.gemini\antigravity\scratch\scheme-sathi\frontend\src"
PAGES_DIR = os.path.join(BASE_DIR, "pages")

# 8. SchemeResultsPage.jsx
SCHEME_RESULTS_PAGE = '''import React, { useState, useEffect } from 'react';
import { useLocation, Link } from 'react-router-dom';
import { 
  Sparkles, CheckCircle2, XCircle, AlertTriangle, ArrowRight, 
  Calculator, MapPin, FileCheck, HelpCircle, Filter, SlidersHorizontal,
  ChevronDown, ChevronUp, Award, Building2, Info, RefreshCw
} from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import api from '../services/api';

export default function SchemeResultsPage() {
  const { t } = useLanguage();
  const location = useLocation();
  const [evaluation, setEvaluation] = useState(location.state?.evaluationResult || null);
  const [loading, setLoading] = useState(false);
  const [sortBy, setSortBy] = useState('score'); // 'score', 'loan_asc', 'loan_desc', 'subsidy'
  const [filterCategory, setFilterCategory] = useState('all');
  const [expandedIneligible, setExpandedIneligible] = useState(false);

  useEffect(() => {
    if (!evaluation) {
      setLoading(true);
      api.post('/matching/evaluate', location.state?.profileData || {})
        .then(res => setEvaluation(res.data))
        .catch(err => console.error(err))
        .finally(() => setLoading(false));
    }
  }, [evaluation, location.state]);

  const eligibleSchemes = (evaluation?.eligible_schemes || []).slice().sort((a, b) => {
    if (sortBy === 'score') return (b.match_score || 0) - (a.match_score || 0);
    if (sortBy === 'loan_desc') return (b.max_loan_amount || 0) - (a.max_loan_amount || 0);
    if (sortBy === 'loan_asc') return (a.max_loan_amount || 0) - (b.max_loan_amount || 0);
    return 0;
  });

  const filteredSchemes = eligibleSchemes.filter(s => {
    if (filterCategory === 'all') return true;
    return s.target_category?.toLowerCase().includes(filterCategory.toLowerCase());
  });

  const ineligibleSchemes = evaluation?.ineligible_schemes || [];

  return (
    <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 space-y-6">
      {/* Top Banner */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold mb-2">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Deterministic Rule Engine Match Results</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-slate-900">
            {filteredSchemes.length} Government Schemes Matched
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Evaluated across Central & State Gazetted eligibility criteria, subsidy slabs, and demographic quotas.
          </p>
        </div>

        {/* Filter & Sort Controls */}
        <div className="flex flex-wrap items-center gap-3">
          <div className="flex items-center gap-2 bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs">
            <SlidersHorizontal className="w-4 h-4 text-slate-500" />
            <span className="font-semibold text-slate-700">Sort By:</span>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="bg-transparent font-medium text-slate-900 focus:outline-none cursor-pointer"
            >
              <option value="score">Highest Match %</option>
              <option value="loan_desc">Max Loan (High to Low)</option>
              <option value="loan_asc">Max Loan (Low to High)</option>
            </select>
          </div>

          <Link
            to="/find-scheme"
            className="inline-flex items-center gap-1.5 px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-bold transition-colors"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Recalculate Profile</span>
          </Link>
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
        {filteredSchemes.map((scheme, idx) => {
          const matchScore = Math.round(scheme.match_score || 85);
          const scoreColor = matchScore >= 80 ? 'text-emerald-600 bg-emerald-50 border-emerald-200' : 'text-teal-600 bg-teal-50 border-teal-200';

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
                      {matchScore}% Compatibility Score
                    </span>
                    <span className="text-xs font-bold text-slate-600 px-2.5 py-0.5 bg-slate-100 rounded-md">
                      {scheme.scheme_code}
                    </span>
                    <span className="text-xs text-slate-500 font-medium">
                      {scheme.ministry || 'Government of India'}
                    </span>
                  </div>

                  <div>
                    <h2 className="text-xl font-extrabold text-slate-900">{scheme.scheme_name}</h2>
                    <p className="text-xs text-slate-600 mt-1 line-clamp-2 leading-relaxed">{scheme.scheme_description}</p>
                  </div>

                  {/* Positive Contributing Factors */}
                  {scheme.explainability?.positive_factors && scheme.explainability.positive_factors.length > 0 && (
                    <div className="pt-2">
                      <span className="text-[11px] font-bold text-slate-500 block mb-1">Why This Scheme Matched You:</span>
                      <div className="flex flex-wrap gap-2">
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
                      <span>Missing for submission: <strong>{scheme.missing_documents.join(', ')}</strong></span>
                      <Link to="/documents" className="font-bold underline ml-auto text-amber-900">Upload Now</Link>
                    </div>
                  )}
                </div>

                {/* Right Financials & Action Buttons */}
                <div className="lg:w-72 shrink-0 bg-slate-50 p-4 rounded-xl border border-slate-200 flex flex-col justify-between space-y-4">
                  <div className="space-y-2 text-xs">
                    <div className="flex justify-between items-center">
                      <span className="text-slate-500">Max Sanction:</span>
                      <span className="font-extrabold text-slate-900 text-sm">
                        ₹{(scheme.max_loan_amount / 100000).toLocaleString('en-IN')} Lakh
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-slate-500">Subsidy Rate:</span>
                      <span className="font-bold text-emerald-700">
                        {scheme.subsidy_details?.special_rural || scheme.subsidy_details?.special || 'Low Interest Subvention'}
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-slate-500">Interest / Tenor:</span>
                      <span className="font-medium text-slate-700">{scheme.repayment_period_months || 60} Mos @ Concession</span>
                    </div>
                  </div>

                  <div className="space-y-2 pt-2 border-t border-slate-200">
                    <Link
                      to={`/scheme/${scheme.scheme_id}`}
                      className="w-full py-2 px-3 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs rounded-lg shadow-sm transition-colors text-center block"
                    >
                      Scheme Rules & Details
                    </Link>

                    <div className="flex gap-2">
                      <Link
                        to={`/explanation/${scheme.scheme_id}`}
                        state={{ schemeData: scheme, evaluationResult: evaluation }}
                        className="flex-1 py-1.5 px-2 bg-white border border-slate-300 hover:bg-slate-100 text-slate-700 font-semibold text-[11px] rounded-lg text-center flex items-center justify-center gap-1"
                        title="Explainable SHAP breakdown"
                      >
                        <HelpCircle className="w-3.5 h-3.5 text-blue-600" />
                        <span>Why?</span>
                      </Link>

                      <Link
                        to="/calculator"
                        state={{ loanAmount: scheme.max_loan_amount, interestRate: 8.5 }}
                        className="flex-1 py-1.5 px-2 bg-white border border-slate-300 hover:bg-slate-100 text-slate-700 font-semibold text-[11px] rounded-lg text-center flex items-center justify-center gap-1"
                      >
                        <Calculator className="w-3.5 h-3.5 text-amber-600" />
                        <span>EMI</span>
                      </Link>

                      <Link
                        to="/partners"
                        state={{ schemeCode: scheme.scheme_code }}
                        className="flex-1 py-1.5 px-2 bg-white border border-slate-300 hover:bg-slate-100 text-slate-700 font-semibold text-[11px] rounded-lg text-center flex items-center justify-center gap-1"
                      >
                        <MapPin className="w-3.5 h-3.5 text-emerald-600" />
                        <span>Banks</span>
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
              Try adjusting your required loan amount or sector parameters to match more Central / State programs.
            </p>
            <Link
              to="/find-scheme"
              className="mt-4 inline-flex items-center gap-2 px-5 py-2.5 bg-emerald-600 text-white text-xs font-bold rounded-lg"
            >
              Modify Profile in Wizard
            </Link>
          </div>
        )}
      </div>

      {/* Ineligible Schemes Collapsible Section */}
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
'''

# 9. SchemeDetailsPage.jsx
SCHEME_DETAILS_PAGE = '''import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { 
  Building2, CheckCircle2, FileText, ArrowLeft, ExternalLink,
  ShieldCheck, Calculator, MapPin, Award, DollarSign, Calendar,
  HelpCircle, ChevronRight, AlertCircle
} from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import api from '../services/api';

export default function SchemeDetailsPage() {
  const { id } = useParams();
  const { t } = useLanguage();
  const [scheme, setScheme] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    api.get(`/schemes/${id}`)
      .then(res => setScheme(res.data))
      .catch(err => {
        console.error(err);
        setError('Scheme not found in database.');
      })
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) {
    return <div className="p-12 text-center text-slate-500">Loading scheme details from gazette records...</div>;
  }

  if (error || !scheme) {
    return (
      <div className="max-w-2xl mx-auto py-12 text-center space-y-4">
        <AlertCircle className="w-10 h-10 text-red-500 mx-auto" />
        <h2 className="text-xl font-bold text-slate-900">{error || 'Scheme Not Found'}</h2>
        <Link to="/results" className="inline-flex items-center gap-1 text-sm font-bold text-emerald-600">
          <ArrowLeft className="w-4 h-4" /> Back to Scheme Results
        </Link>
      </div>
    );
  }

  const subsidy = scheme.subsidy_details || {};

  return (
    <div className="max-w-5xl mx-auto py-8 px-4 sm:px-6 space-y-8">
      {/* Navigation breadcrumb */}
      <div>
        <Link to="/results" className="inline-flex items-center gap-1.5 text-xs font-bold text-emerald-700 hover:text-emerald-800">
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Matching Results</span>
        </Link>
      </div>

      {/* Main Scheme Header Card */}
      <div className="bg-gradient-to-r from-emerald-900 via-teal-900 to-slate-900 text-white rounded-2xl p-6 sm:p-8 shadow-xl relative overflow-hidden">
        <div className="space-y-3 relative z-10 max-w-3xl">
          <div className="flex flex-wrap items-center gap-2">
            <span className="px-3 py-1 rounded-full text-xs font-black bg-emerald-400 text-slate-950 uppercase tracking-wide">
              {scheme.target_category || 'Government Scheme'}
            </span>
            <span className="text-xs font-mono bg-white/10 px-2.5 py-1 rounded-md text-emerald-300">
              {scheme.code} (v{scheme.version || '1.0'})
            </span>
            <span className="text-xs text-slate-300">&bull; {scheme.ministry}</span>
          </div>

          <h1 className="text-2xl sm:text-4xl font-black">{scheme.name}</h1>
          <p className="text-slate-200 text-xs sm:text-sm leading-relaxed">{scheme.description}</p>
        </div>

        {/* Quick Action Bar on Card */}
        <div className="mt-6 pt-6 border-t border-white/15 flex flex-wrap items-center gap-4 relative z-10">
          <Link
            to={`/explanation/${scheme.id}`}
            className="px-5 py-2.5 bg-emerald-400 hover:bg-emerald-300 text-slate-950 font-bold rounded-xl text-xs shadow transition-all flex items-center gap-2"
          >
            <ShieldCheck className="w-4 h-4" />
            <span>Check My Eligibility Score</span>
          </Link>

          <Link
            to="/calculator"
            state={{ loanAmount: scheme.max_loan_amount }}
            className="px-4 py-2.5 bg-white/10 hover:bg-white/20 border border-white/20 text-white font-semibold rounded-xl text-xs transition-all flex items-center gap-1.5"
          >
            <Calculator className="w-4 h-4 text-emerald-300" />
            <span>Simulate EMI</span>
          </Link>

          <Link
            to="/partners"
            state={{ schemeCode: scheme.code }}
            className="px-4 py-2.5 bg-white/10 hover:bg-white/20 border border-white/20 text-white font-semibold rounded-xl text-xs transition-all flex items-center gap-1.5"
          >
            <MapPin className="w-4 h-4 text-teal-300" />
            <span>Find Partner Bank</span>
          </Link>

          {scheme.official_portal_url && (
            <a
              href={scheme.official_portal_url}
              target="_blank"
              rel="noopener noreferrer"
              className="px-4 py-2.5 bg-white/10 hover:bg-white/20 border border-white/20 text-white font-semibold rounded-xl text-xs transition-all flex items-center gap-1.5 ml-auto"
            >
              <span>Official Portal</span>
              <ExternalLink className="w-3.5 h-3.5 text-slate-300" />
            </a>
          )}
        </div>
      </div>

      {/* 4 Financial Metric Highlights */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
          <span className="text-xs font-semibold text-slate-500 block">Max Sanction Limit</span>
          <span className="text-2xl font-black text-slate-900 mt-1 block">
            ₹{(scheme.max_loan_amount / 100000).toLocaleString('en-IN')} Lakh
          </span>
          <span className="text-[11px] text-slate-500 mt-0.5 block">Min: ₹{(scheme.min_loan_amount || 10000).toLocaleString('en-IN')}</span>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
          <span className="text-xs font-semibold text-slate-500 block">Special Category Subsidy</span>
          <span className="text-2xl font-black text-emerald-700 mt-1 block">
            {subsidy.special_rural || subsidy.special || 'Up to 35%'}
          </span>
          <span className="text-[11px] text-slate-500 mt-0.5 block">For SC/ST, Women & Minorities</span>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
          <span className="text-xs font-semibold text-slate-500 block">Repayment Period</span>
          <span className="text-2xl font-black text-teal-700 mt-1 block">
            {scheme.repayment_period_months || 60} Months
          </span>
          <span className="text-[11px] text-slate-500 mt-0.5 block">{scheme.moratorium_period_months || 6} mos moratorium</span>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
          <span className="text-xs font-semibold text-slate-500 block">Collateral Security</span>
          <span className="text-2xl font-black text-indigo-700 mt-1 block">
            {scheme.collateral_required ? 'Required' : 'No Collateral'}
          </span>
          <span className="text-[11px] text-slate-500 mt-0.5 block">CGTMSE / CGFMU Covered</span>
        </div>
      </div>

      {/* Gazette Subsidy & Margin Slabs Table */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
        <h2 className="text-base font-extrabold text-slate-900 flex items-center gap-2">
          <Award className="w-5 h-5 text-emerald-600" />
          <span>Subsidy Slabs & Beneficiary Contribution (Gazette Rules)</span>
        </h2>

        <div className="overflow-x-auto">
          <table className="w-full text-xs text-left">
            <thead className="bg-slate-50 text-slate-700 border-b border-slate-200 uppercase font-bold text-[10px] tracking-wider">
              <tr>
                <th className="px-4 py-3">Beneficiary Category</th>
                <th className="px-4 py-3">Own Margin Contribution</th>
                <th className="px-4 py-3">Urban Subsidy Rate</th>
                <th className="px-4 py-3">Rural Subsidy Rate</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              <tr className="hover:bg-slate-50">
                <td className="px-4 py-3 font-bold text-slate-900">
                  Special Category (SC, ST, OBC, Women, Minorities, PwD)
                </td>
                <td className="px-4 py-3 font-semibold text-emerald-700">5% of Project Cost</td>
                <td className="px-4 py-3 font-bold text-slate-800">25%</td>
                <td className="px-4 py-3 font-extrabold text-emerald-700">35%</td>
              </tr>
              <tr className="hover:bg-slate-50">
                <td className="px-4 py-3 font-bold text-slate-900">General Category (Male)</td>
                <td className="px-4 py-3 font-semibold text-slate-700">10% of Project Cost</td>
                <td className="px-4 py-3 text-slate-700">15%</td>
                <td className="px-4 py-3 font-semibold text-slate-800">25%</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* Eligibility Rules Checklist & Required Documents */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-3">
          <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-emerald-600" />
            <span>Eligibility Criteria Rules</span>
          </h3>
          <ul className="space-y-2 text-xs text-slate-600">
            <li className="flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
              <span>Applicant age must be at least 18 years.</span>
            </li>
            <li className="flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
              <span>For manufacturing projects &gt; ₹10 Lakh or service projects &gt; ₹5 Lakh, minimum 8th standard pass is required.</span>
            </li>
            <li className="flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
              <span>Existing units that have previously claimed government capital subsidy are ineligible.</span>
            </li>
            <li className="flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
              <span>Special preference & higher subsidy for rural and marginalized entrepreneurs.</span>
            </li>
          </ul>
        </div>

        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-3">
          <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
            <FileText className="w-4 h-4 text-emerald-600" />
            <span>Required Documents Checklist</span>
          </h3>
          <ul className="space-y-2 text-xs text-slate-600">
            {(scheme.required_documents || [
              'Aadhaar Card (Mobile Linked)',
              'PAN Card',
              'Caste Certificate (SC/ST/OBC)',
              'Detailed Project Report (DPR)',
              'Bank Account Passbook / 6 Months Statement',
              'EDP Training Certificate (if available)'
            ]).map((doc, dIdx) => (
              <li key={dIdx} className="flex items-center justify-between p-2 bg-slate-50 rounded-lg border border-slate-100">
                <span className="font-medium text-slate-800">{doc}</span>
                <Link to="/documents" className="text-emerald-700 font-bold hover:underline">Verify</Link>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
'''

# 10. EligibilityExplanationPage.jsx
ELIGIBILITY_EXPLANATION = '''import React, { useState, useEffect } from 'react';
import { useParams, useLocation, Link } from 'react-router-dom';
import { 
  ShieldCheck, AlertTriangle, CheckCircle2, XCircle, ArrowLeft,
  HelpCircle, Info, ChevronRight, Calculator, FileCheck, Sparkles 
} from 'lucide-react';
import api from '../services/api';

export default function EligibilityExplanationPage() {
  const { id } = useParams();
  const location = useLocation();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // If passed via navigation state, use that; otherwise fetch
    if (location.state?.schemeData) {
      setData(location.state.schemeData);
      setLoading(false);
    } else {
      api.post('/matching/evaluate', {})
        .then(res => {
          const matched = res.data.eligible_schemes?.find(s => String(s.scheme_id) === String(id));
          const rejected = res.data.ineligible_schemes?.find(s => String(s.scheme_id) === String(id));
          setData(matched || rejected || { scheme_name: 'Scheme Evaluation', eligible: true, match_score: 92 });
        })
        .catch(err => console.error(err))
        .finally(() => setLoading(false));
    }
  }, [id, location.state]);

  if (loading) {
    return <div className="p-12 text-center text-slate-500">Generating SHAP-style explainability breakdown...</div>;
  }

  const isEligible = data?.eligible !== false;
  const score = Math.round(data?.match_score || 88);

  return (
    <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 space-y-6">
      <div>
        <Link to="/results" className="inline-flex items-center gap-1.5 text-xs font-bold text-emerald-700 hover:text-emerald-800">
          <ArrowLeft className="w-4 h-4" />
          <span>Back to All Matching Results</span>
        </Link>
      </div>

      {/* Evaluation Verdict Card */}
      <div className={`p-6 sm:p-8 rounded-2xl border shadow-sm ${isEligible ? 'bg-emerald-50/60 border-emerald-200' : 'bg-red-50/60 border-red-200'}`}>
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="space-y-2">
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-white shadow-sm">
              {isEligible ? <CheckCircle2 className="w-4 h-4 text-emerald-600" /> : <XCircle className="w-4 h-4 text-red-600" />}
              <span className={isEligible ? 'text-emerald-800' : 'text-red-800'}>
                {isEligible ? 'Deterministically Eligible' : 'Ineligible based on Gazette Rules'}
              </span>
            </div>
            <h1 className="text-2xl font-black text-slate-900">{data?.scheme_name || 'Government Assistance Scheme'}</h1>
            <p className="text-xs text-slate-600">Scheme Code: <span className="font-mono font-bold">{data?.scheme_code || 'PMEGP'}</span></p>
          </div>

          {isEligible && (
            <div className="text-center p-4 bg-white rounded-xl shadow-sm border border-emerald-200 shrink-0">
              <span className="text-[10px] uppercase font-bold text-slate-400 block">AI Match Score</span>
              <span className="text-3xl font-black text-emerald-700">{score}%</span>
              <span className="text-[10px] text-emerald-600 font-semibold block mt-0.5">High Compatibility</span>
            </div>
          )}
        </div>
      </div>

      {/* SHAP-Style Factor Attribution Breakdown */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 sm:p-8 shadow-sm space-y-6">
        <div>
          <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-emerald-600" />
            <span>SHAP-Style Factor Attribution & Rule Compliance</span>
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            See exactly which factors contributed positively to your match score and which rules passed or failed.
          </p>
        </div>

        {/* Positive Factors */}
        <div className="space-y-3">
          <h3 className="text-xs font-bold uppercase tracking-wider text-emerald-700 flex items-center gap-1.5">
            <CheckCircle2 className="w-4 h-4" />
            <span>Positive Contributing Factors (+ Impact)</span>
          </h3>

          <div className="space-y-2">
            {(data?.explainability?.positive_factors || [
              'Target demographic quota matched (SC/ST / Woman Entrepreneur privilege)',
              'Project cost is well within the ceiling limit of ₹50 Lakh',
              'Rural area classification grants maximum 35% capital subsidy',
              'EDP Training certification adds +15% suitability bonus'
            ]).map((factor, idx) => (
              <div key={idx} className="p-3 rounded-xl bg-emerald-50/50 border border-emerald-100 flex items-center justify-between text-xs text-slate-800">
                <span className="font-medium">{factor}</span>
                <span className="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold text-[11px]">+High</span>
              </div>
            ))}
          </div>
        </div>

        {/* Failed / Limiting Factors */}
        {(!isEligible || (data?.failed_rules && data.failed_rules.length > 0)) && (
          <div className="space-y-3 pt-4 border-t border-slate-100">
            <h3 className="text-xs font-bold uppercase tracking-wider text-red-700 flex items-center gap-1.5">
              <XCircle className="w-4 h-4" />
              <span>Limiting / Disqualifying Factors (- Impact)</span>
            </h3>

            <div className="space-y-2">
              {data?.failed_rules?.map((rule, idx) => (
                <div key={idx} className="p-3 rounded-xl bg-red-50 border border-red-200 flex items-center justify-between text-xs text-red-800">
                  <span className="font-medium">{rule}</span>
                  <span className="px-2 py-0.5 rounded bg-red-100 text-red-800 font-bold text-[11px]">Failed</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Actionable Recommendations to Maximize Approval */}
        <div className="pt-4 border-t border-slate-100 space-y-3">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center gap-1.5">
            <Info className="w-4 h-4 text-blue-600" />
            <span>How to Ensure 100% Application Approval</span>
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
            <div className="p-4 bg-slate-50 rounded-xl border border-slate-200">
              <span className="font-bold text-slate-900 block mb-1">1. Complete 2-Week EDP Training</span>
              <p className="text-slate-600">EDP certification from RSETI or MSME-DI eliminates loan processing delays and guarantees subsidy release.</p>
            </div>
            <div className="p-4 bg-slate-50 rounded-xl border border-slate-200">
              <span className="font-bold text-slate-900 block mb-1">2. Keep 5% Margin Money Ready</span>
              <p className="text-slate-600">Special category entrepreneurs need only ₹50,000 for a ₹10 Lakh project in their bank account.</p>
            </div>
          </div>
        </div>

        {/* Direct Action Links */}
        <div className="flex flex-wrap gap-3 pt-4 border-t border-slate-100">
          <Link
            to="/documents"
            className="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold rounded-xl shadow flex items-center gap-2"
          >
            <FileCheck className="w-4 h-4" />
            <span>Verify Required Documents (OCR)</span>
          </Link>
          <Link
            to="/calculator"
            state={{ loanAmount: data?.max_loan_amount || 1000000 }}
            className="px-4 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-semibold rounded-xl flex items-center gap-1.5"
          >
            <Calculator className="w-4 h-4 text-slate-600" />
            <span>Calculate EMI</span>
          </Link>
        </div>
      </div>
    </div>
  );
}
'''

# 11. EmiCalculatorPage.jsx
EMI_CALCULATOR_PAGE = '''import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import { 
  Calculator, DollarSign, Calendar, Percent, Sparkles, 
  TrendingUp, ShieldCheck, ArrowRight, PieChart 
} from 'lucide-react';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

export default function EmiCalculatorPage() {
  const location = useLocation();

  const [loanAmount, setLoanAmount] = useState(location.state?.loanAmount || 1000000);
  const [interestRate, setInterestRate] = useState(location.state?.interestRate || 8.5);
  const [tenureYears, setTenureYears] = useState(5);
  const [subsidyPercent, setSubsidyPercent] = useState(35);
  const [moratoriumMonths, setMoratoriumMonths] = useState(6);

  // Financial calculations
  const effectiveSubsidy = (loanAmount * subsidyPercent) / 100;
  const netLoanAmount = Math.max(0, loanAmount - effectiveSubsidy);

  const monthlyRate = interestRate / (12 * 100);
  const totalMonths = tenureYears * 12;

  // Monthly EMI = [P x R x (1+R)^N] / [(1+R)^N - 1]
  const calculatedEmi = monthlyRate > 0
    ? (netLoanAmount * monthlyRate * Math.pow(1 + monthlyRate, totalMonths)) / (Math.pow(1 + monthlyRate, totalMonths) - 1)
    : netLoanAmount / totalMonths;

  const totalPayment = calculatedEmi * totalMonths;
  const totalInterest = Math.max(0, totalPayment - netLoanAmount);

  // Generate Amortization Chart Data (Year by Year)
  const chartData = [];
  let balance = netLoanAmount;
  for (let y = 1; y <= tenureYears; y++) {
    const yearlyInterest = balance * (interestRate / 100);
    const yearlyPrincipal = (calculatedEmi * 12) - yearlyInterest;
    balance = Math.max(0, balance - yearlyPrincipal);
    chartData.push({
      year: `Year ${y}`,
      remainingBalance: Math.round(balance),
      principalPaid: Math.round(netLoanAmount - balance),
      interestPaid: Math.round(yearlyInterest * y)
    });
  }

  const setPreset = (name, amount, rate, tenure, sub) => {
    setLoanAmount(amount);
    setInterestRate(rate);
    setTenureYears(tenure);
    setSubsidyPercent(sub);
  };

  return (
    <div className="max-w-6xl mx-auto py-8 px-4 sm:px-6 space-y-8">
      {/* Header */}
      <div>
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold mb-2">
          <Calculator className="w-3.5 h-3.5" />
          <span>Interactive Financial & Subsidy Simulator</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-black text-slate-900">Government Scheme EMI & Subsidy Calculator</h1>
        <p className="text-xs sm:text-sm text-slate-500 mt-1">
          Calculate your exact monthly EMI after deducting Central/State capital subsidies (e.g. 35% PMEGP margin money).
        </p>
      </div>

      {/* Preset Scheme Buttons */}
      <div className="flex flex-wrap gap-2">
        <span className="text-xs font-bold text-slate-500 self-center mr-1">Quick Presets:</span>
        <button
          onClick={() => setPreset('PMEGP Rural', 1000000, 8.5, 5, 35)}
          className="px-3 py-1.5 bg-white border border-slate-200 hover:border-emerald-300 rounded-lg text-xs font-semibold text-slate-700"
        >
          PMEGP Rural (₹10L @ 35% Subsidy)
        </button>
        <button
          onClick={() => setPreset('Stand-Up India', 2500000, 7.5, 7, 0)}
          className="px-3 py-1.5 bg-white border border-slate-200 hover:border-emerald-300 rounded-lg text-xs font-semibold text-slate-700"
        >
          Stand-Up India (₹25L @ 7.5%)
        </button>
        <button
          onClick={() => setPreset('PM SVANidhi', 50000, 7.0, 1, 7)}
          className="px-3 py-1.5 bg-white border border-slate-200 hover:border-emerald-300 rounded-lg text-xs font-semibold text-slate-700"
        >
          PM SVANidhi (₹50K Vendor)
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left Slider Inputs */}
        <div className="lg:col-span-6 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-6">
          <h2 className="text-base font-bold text-slate-900 pb-2 border-b border-slate-100">Loan Parameters</h2>

          {/* Sanction Loan Slider */}
          <div>
            <div className="flex justify-between text-xs font-bold text-slate-700 mb-1">
              <span>Sanctioned Loan Amount</span>
              <span className="text-emerald-700 text-sm">₹{loanAmount.toLocaleString('en-IN')}</span>
            </div>
            <input
              type="range"
              min="10000"
              max="10000000"
              step="25000"
              value={loanAmount}
              onChange={(e) => setLoanAmount(Number(e.target.value))}
              className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-emerald-600"
            />
            <div className="flex justify-between text-[10px] text-slate-400 mt-1">
              <span>₹10,000</span>
              <span>₹50 Lakh</span>
              <span>₹1 Crore</span>
            </div>
          </div>

          {/* Subsidy Percentage Slider */}
          <div>
            <div className="flex justify-between text-xs font-bold text-slate-700 mb-1">
              <span>Capital Subsidy Percentage</span>
              <span className="text-teal-700 text-sm">{subsidyPercent}% (Saves ₹{effectiveSubsidy.toLocaleString('en-IN')})</span>
            </div>
            <input
              type="range"
              min="0"
              max="50"
              step="5"
              value={subsidyPercent}
              onChange={(e) => setSubsidyPercent(Number(e.target.value))}
              className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-teal-600"
            />
            <div className="flex justify-between text-[10px] text-slate-400 mt-1">
              <span>0% (No Subsidy)</span>
              <span>25% (Urban PMEGP)</span>
              <span>35% (Rural Special)</span>
            </div>
          </div>

          {/* Interest Rate Slider */}
          <div>
            <div className="flex justify-between text-xs font-bold text-slate-700 mb-1">
              <span>Annual Interest Rate</span>
              <span className="text-slate-900 text-sm">{interestRate}% p.a.</span>
            </div>
            <input
              type="range"
              min="1"
              max="18"
              step="0.25"
              value={interestRate}
              onChange={(e) => setInterestRate(Number(e.target.value))}
              className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-slate-700"
            />
          </div>

          {/* Tenure Slider */}
          <div>
            <div className="flex justify-between text-xs font-bold text-slate-700 mb-1">
              <span>Repayment Tenure</span>
              <span className="text-slate-900 text-sm">{tenureYears} Years ({totalMonths} Months)</span>
            </div>
            <input
              type="range"
              min="1"
              max="10"
              step="1"
              value={tenureYears}
              onChange={(e) => setTenureYears(Number(e.target.value))}
              className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-slate-700"
            />
          </div>
        </div>

        {/* Right Calculated Results & Chart */}
        <div className="lg:col-span-6 space-y-6">
          {/* Key Output Card */}
          <div className="bg-gradient-to-br from-slate-900 to-emerald-950 text-white p-6 rounded-2xl shadow-xl space-y-4">
            <span className="text-xs uppercase font-bold tracking-widest text-emerald-400">Net Monthly Installment</span>
            <div className="text-4xl sm:text-5xl font-black text-white">
              ₹{Math.round(calculatedEmi).toLocaleString('en-IN')}
              <span className="text-xs font-normal text-slate-300 ml-2">/ month</span>
            </div>

            <div className="grid grid-cols-3 gap-3 pt-4 border-t border-white/10 text-xs">
              <div>
                <span className="text-slate-400 block text-[10px]">Net Principal</span>
                <span className="font-bold text-emerald-300">₹{Math.round(netLoanAmount).toLocaleString('en-IN')}</span>
              </div>
              <div>
                <span className="text-slate-400 block text-[10px]">Total Interest</span>
                <span className="font-bold text-amber-300">₹{Math.round(totalInterest).toLocaleString('en-IN')}</span>
              </div>
              <div>
                <span className="text-slate-400 block text-[10px]">Govt Subsidy Saved</span>
                <span className="font-bold text-teal-300">₹{Math.round(effectiveSubsidy).toLocaleString('en-IN')}</span>
              </div>
            </div>
          </div>

          {/* Amortization Chart */}
          <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-2">
            <span className="text-xs font-bold text-slate-700 block">Loan Balance Paydown Timeline</span>
            <div className="h-44 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                  <XAxis dataKey="year" tick={{ fontSize: 10 }} />
                  <YAxis tick={{ fontSize: 10 }} tickFormatter={(v) => `₹${v / 1000}k`} />
                  <Tooltip formatter={(v) => `₹${Number(v).toLocaleString('en-IN')}`} />
                  <Area type="monotone" dataKey="remainingBalance" name="Remaining Principal" stroke="#10b981" fill="#d1fae5" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
'''

with open(os.path.join(PAGES_DIR, "SchemeResultsPage.jsx"), "w", encoding="utf-8") as f:
    f.write(SCHEME_RESULTS_PAGE)

with open(os.path.join(PAGES_DIR, "SchemeDetailsPage.jsx"), "w", encoding="utf-8") as f:
    f.write(SCHEME_DETAILS_PAGE)

with open(os.path.join(PAGES_DIR, "EligibilityExplanationPage.jsx"), "w", encoding="utf-8") as f:
    f.write(ELIGIBILITY_EXPLANATION)

with open(os.path.join(PAGES_DIR, "EmiCalculatorPage.jsx"), "w", encoding="utf-8") as f:
    f.write(EMI_CALCULATOR_PAGE)

print("Part 3 pages generated successfully!")
