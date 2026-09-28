import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { 
  Building2, CheckCircle2, FileText, ArrowLeft, ExternalLink,
  ShieldCheck, Calculator, MapPin, Award, DollarSign, Calendar,
  HelpCircle, ChevronRight, AlertCircle, Globe, Check
} from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import api from '../services/api';

export default function SchemeDetailsPage() {
  const { id } = useParams();
  const { t, translateScheme } = useLanguage();
  const [scheme, setScheme] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!id || id === 'undefined' || id === 'null') {
      setError('No scheme has been selected yet.');
      setLoading(false);
      return;
    }
    api.get(`/schemes/${id}`)
      .then(res => setScheme(res.data))
      .catch(err => {
        console.error(err);
        if (err.response?.status === 404) {
          setError('No scheme available yet.');
        } else {
          setError('Unable to load scheme details. Please try again.');
        }
      })
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) {
    return <div className="p-12 text-center text-slate-500 font-semibold">{t('loading')}</div>;
  }

  if (error || !scheme) {
    return (
      <div className="max-w-2xl mx-auto py-12 text-center space-y-4">
        <AlertCircle className="w-10 h-10 text-amber-500 mx-auto" />
        <h2 className="text-xl font-bold text-slate-900">{t(error || 'No scheme has been selected yet.')}</h2>
        <p className="text-xs text-slate-500">
          {t('Explore available government schemes or complete your evaluation questionnaire to view eligible schemes.')}
        </p>
        <div className="flex items-center justify-center gap-4 pt-2">
          <Link to="/results" className="inline-flex items-center gap-1 text-sm font-bold text-emerald-600 hover:text-emerald-700">
            <ArrowLeft className="w-4 h-4" /> {t('Matching Schemes')}
          </Link>
          <Link to="/find-scheme" className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs rounded-xl shadow transition-all">
            {t('Find Schemes')}
          </Link>
        </div>
      </div>
    );
  }

  let subsidy = {};
  if (scheme.subsidy_details) {
    try {
      subsidy = typeof scheme.subsidy_details === 'string' ? JSON.parse(scheme.subsidy_details) : scheme.subsidy_details;
    } catch(e) {
      subsidy = {};
    }
  }

  let eligiblePurposes = [];
  try {
    eligiblePurposes = typeof scheme.eligible_purposes === 'string' ? JSON.parse(scheme.eligible_purposes) : (scheme.eligible_purposes || []);
  } catch(e) {}

  let eligibleCategories = [];
  try {
    eligibleCategories = typeof scheme.eligible_categories === 'string' ? JSON.parse(scheme.eligible_categories) : (scheme.eligible_categories || []);
  } catch(e) {}

  let eligibleStates = [];
  try {
    eligibleStates = typeof scheme.eligible_states === 'string' ? JSON.parse(scheme.eligible_states) : (scheme.eligible_states || []);
  } catch(e) {}

  const isCentral = eligibleStates.includes('All India');
  const portalUrl = scheme.official_portal_url || 'https://www.myscheme.gov.in';
  const localizedScheme = translateScheme(scheme);

  return (
    <div className="max-w-5xl mx-auto py-8 px-4 sm:px-6 space-y-8">
      {/* Navigation breadcrumb */}
      <div className="flex items-center justify-between">
        <Link to="/results" className="inline-flex items-center gap-1.5 text-xs font-bold text-emerald-700 hover:text-emerald-800">
          <ArrowLeft className="w-4 h-4" />
          <span>{t('Previous')} / {t('Matching Schemes')}</span>
        </Link>
        <span className="text-[11px] font-semibold text-slate-500 flex items-center gap-1">
          <Globe className="w-3.5 h-3.5 text-emerald-600" />
          <span>Official Gazette Registry • myScheme.gov.in</span>
        </span>
      </div>

      {/* Main Scheme Header Card */}
      <div className="bg-gradient-to-r from-emerald-900 via-teal-900 to-slate-900 text-white rounded-2xl p-6 sm:p-8 shadow-xl relative overflow-hidden">
        <div className="space-y-3 relative z-10 max-w-3xl">
          <div className="flex flex-wrap items-center gap-2">
            <span className="px-3 py-1 rounded-full text-xs font-black bg-emerald-400 text-slate-950 uppercase tracking-wide">
              {t('targetMarginalized', 'Target Beneficiaries')}
            </span>
            <span className="text-xs font-mono bg-white/10 px-2.5 py-1 rounded-md text-emerald-300">
              {localizedScheme.code || localizedScheme.scheme_code}
            </span>
            <span className={`text-[11px] font-bold px-2.5 py-1 rounded-md ${
              isCentral ? 'bg-blue-400/20 text-blue-200 border border-blue-400/30' : 'bg-purple-400/20 text-purple-200 border border-purple-400/30'
            }`}>
              {isCentral ? t('filterCentral', 'Central Scheme') : t('filterState', 'State Scheme')}
            </span>
            <span className="text-xs text-slate-300">&bull; {localizedScheme.department || localizedScheme.ministry}</span>
          </div>

          <h1 className="text-2xl sm:text-4xl font-black">{localizedScheme.name || localizedScheme.scheme_name}</h1>
          <p className="text-slate-200 text-xs sm:text-sm leading-relaxed">{localizedScheme.description || localizedScheme.scheme_description}</p>
        </div>

        {/* Quick Action Bar on Card */}
        <div className="mt-6 pt-6 border-t border-white/15 flex flex-wrap items-center gap-4 relative z-10">
          <Link
            to={`/explanation/${scheme.id}`}
            className="px-5 py-2.5 bg-emerald-400 hover:bg-emerald-300 text-slate-950 font-bold rounded-xl text-xs shadow transition-all flex items-center gap-2"
          >
            <ShieldCheck className="w-4 h-4" />
            <span>{t('Why Eligible')}</span>
          </Link>

          <Link
            to="/calculator"
            state={{ loanAmount: scheme.max_loan_amount }}
            className="px-4 py-2.5 bg-white/10 hover:bg-white/20 border border-white/20 text-white font-semibold rounded-xl text-xs transition-all flex items-center gap-1.5"
          >
            <Calculator className="w-4 h-4 text-emerald-300" />
            <span>{t('EMI Calculator')}</span>
          </Link>

          <Link
            to="/partners"
            state={{ schemeCode: scheme.code }}
            className="px-4 py-2.5 bg-white/10 hover:bg-white/20 border border-white/20 text-white font-semibold rounded-xl text-xs transition-all flex items-center gap-1.5"
          >
            <MapPin className="w-4 h-4 text-teal-300" />
            <span>{t('Channel Partners')}</span>
          </Link>

          <a
            href={portalUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="px-4 py-2.5 bg-white/10 hover:bg-white/20 border border-white/20 text-white font-semibold rounded-xl text-xs transition-all flex items-center gap-1.5 ml-auto"
          >
            <span>{t('mySchemePortal')}</span>
            <ExternalLink className="w-3.5 h-3.5 text-slate-300" />
          </a>
        </div>
      </div>

      {/* 4 Financial Metric Highlights */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
          <span className="text-xs font-semibold text-slate-500 block">{t('maxLoan')}</span>
          <span className="text-2xl font-black text-slate-900 mt-1 block">
            ₹{(scheme.max_loan_amount / 100000).toLocaleString('en-IN')} {t('unitLakh')}
          </span>
          <span className="text-[11px] text-slate-500 mt-0.5 block">Min: ₹{(scheme.min_loan_amount || 10000).toLocaleString('en-IN')}</span>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
          <span className="text-xs font-semibold text-slate-500 block">{t('subsidyRate')}</span>
          <span className="text-2xl font-black text-emerald-700 mt-1 block">
            {scheme.code === 'PMEGP' ? t('specialRural') : (subsidy.special_rural || subsidy.special || `${scheme.subsidy_percentage_special || 25}%`)}
          </span>
          <span className="text-[11px] text-slate-500 mt-0.5 block">{t('scStFounders')} & {t('womenEntrepreneurs')}</span>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
          <span className="text-xs font-semibold text-slate-500 block">{t('tenor')}</span>
          <span className="text-2xl font-black text-teal-700 mt-1 block">
            {scheme.repayment_period_months || 60} {t('unitMonths')}
          </span>
          <span className="text-[11px] text-slate-500 mt-0.5 block">{scheme.moratorium_months || 6} {t('unitMonths')} moratorium</span>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
          <span className="text-xs font-semibold text-slate-500 block">{t('interestRateLabel')}</span>
          <span className="text-2xl font-black text-indigo-700 mt-1 block">
            {scheme.interest_rate_min}% - {scheme.interest_rate_max}%
          </span>
          <span className="text-[11px] text-slate-500 mt-0.5 block">{scheme.interest_rate_display || t('lowInterest')}</span>
        </div>
      </div>

      {/* Gazette Subsidy & Margin Slabs Table */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
        <h2 className="text-base font-extrabold text-slate-900 flex items-center gap-2">
          <Award className="w-5 h-5 text-emerald-600" />
          <span>{t('Subsidy Slabs & Beneficiary Contribution (Gazette Statutory Rules)')}</span>
        </h2>

        <div className="overflow-x-auto">
          <table className="w-full text-xs text-left">
            <thead className="bg-slate-50 text-slate-700 border-b border-slate-200 uppercase font-bold text-[10px] tracking-wider">
              <tr>
                <th className="px-4 py-3">{t('Beneficiary Category')}</th>
                <th className="px-4 py-3">{t('Own Margin Contribution')}</th>
                <th className="px-4 py-3">{t('Urban Subsidy Rate')}</th>
                <th className="px-4 py-3">{t('Rural Subsidy Rate')}</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              <tr className="hover:bg-slate-50">
                <td className="px-4 py-3 font-bold text-slate-900">
                  {t('Special Category (SC, ST, OBC, Women, Minorities, PwD, NER)')}
                </td>
                <td className="px-4 py-3 font-semibold text-emerald-700">{t('5% of Project Cost')}</td>
                <td className="px-4 py-3 font-bold text-slate-800">
                  {subsidy.special_urban || '25%'}
                </td>
                <td className="px-4 py-3 font-extrabold text-emerald-700">
                  {subsidy.special_rural || '35%'}
                </td>
              </tr>
              <tr className="hover:bg-slate-50">
                <td className="px-4 py-3 font-bold text-slate-900">{t('General Category (Male)')}</td>
                <td className="px-4 py-3 font-semibold text-slate-700">{t('10% of Project Cost')}</td>
                <td className="px-4 py-3 text-slate-700">
                  {subsidy.general_urban || '15%'}
                </td>
                <td className="px-4 py-3 font-semibold text-slate-800">
                  {subsidy.general_rural || '25%'}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* Eligibility Rules Checklist & Required Documents */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
          <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-emerald-600" />
            <span>{t('Eligible Categories & Purposes')}</span>
          </h3>
          
          <div className="space-y-3 text-xs">
            <div>
              <span className="font-bold text-slate-700 block mb-1">{t('Target Categories:')}</span>
              <div className="flex flex-wrap gap-1.5">
                {eligibleCategories.map((c, i) => (
                  <span key={i} className="px-2.5 py-1 bg-emerald-50 text-emerald-800 border border-emerald-200 rounded-md font-semibold text-[11px]">
                    {t(c)}
                  </span>
                ))}
              </div>
            </div>

            <div>
              <span className="font-bold text-slate-700 block mb-1">{t('Allowed Business Purposes:')}</span>
              <div className="flex flex-wrap gap-1.5">
                {eligiblePurposes.map((p, i) => (
                  <span key={i} className="px-2.5 py-1 bg-slate-100 text-slate-800 rounded-md font-medium text-[11px]">
                    {t(p)}
                  </span>
                ))}
              </div>
            </div>

            <div>
              <span className="font-bold text-slate-700 block mb-1">{t('Age Limits & Income Ceiling:')}</span>
              <p className="text-slate-600">
                {t('Age')}: <strong>{scheme.min_age || 18} - {scheme.max_age || 65} {t('unitYears', 'years')}</strong> &bull; {t('Income Ceiling')}: <strong>{scheme.max_income_limit ? `₹${scheme.max_income_limit.toLocaleString('en-IN')}/${t('yr')}` : t('No Income Ceiling')}</strong>
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-3">
          <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
            <FileText className="w-4 h-4 text-emerald-600" />
            <span>{t('Required Documents Checklist')}</span>
          </h3>
          <ul className="space-y-2 text-xs text-slate-600">
            {(() => {
              const isEdu = scheme.loan_type === 'EDUCATION' || 
                            scheme.purpose_type === 'EDUCATION' || 
                            ['CSIS', 'NSFDC-EDU', 'NBCFDC-EL'].includes((scheme.code || '').toUpperCase());
              const defaultEduDocs = [
                '10th Standard Marksheet / Passing Certificate',
                '12th Standard Marksheet / Passing Certificate',
                'Aadhaar Card (UIDAI Linked)',
                'PAN Card (Permanent Account Number)',
                'Income Certificate / Revenue Authority Proof',
                'Caste Certificate (if claiming quota subvention)'
              ];
              const defaultBizDocs = [
                'Aadhaar Card (UIDAI Linked)',
                'PAN Card (ITD Verified)',
                'Detailed Project Report (DPR)',
                'Annual Family Income Certificate',
                'Caste / Category Certificate',
                'Udyam MSME Registration Certificate'
              ];
              const docList = isEdu ? defaultEduDocs : (scheme.required_documents || defaultBizDocs);
              return docList.map((doc, dIdx) => (
                <li key={dIdx} className="flex items-center justify-between p-2.5 bg-slate-50 rounded-lg border border-slate-100">
                  <span className="font-medium text-slate-800">{t(doc)}</span>
                  <Link to="/documents" className="text-emerald-700 font-bold hover:underline text-[11px]">{t('Verify OCR')}</Link>
                </li>
              ));
            })()}
          </ul>
        </div>
      </div>
    </div>
  );
}
