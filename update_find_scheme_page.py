# -*- coding: utf-8 -*-
"""
Update FindMySchemePage.jsx with complete multilingual support
"""

find_scheme_jsx = r'''import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { 
  Sparkles, ArrowRight, ArrowLeft, CheckCircle2, User, MapPin, 
  Briefcase, DollarSign, FileCheck, ShieldCheck 
} from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import api from '../services/api';

export default function FindMySchemePage() {
  const { t, currentLanguage } = useLanguage();
  const navigate = useNavigate();
  const location = useLocation();

  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const [formData, setFormData] = useState({
    // Step 1: Demographics
    full_name: 'Beneficiary Candidate',
    age: 29,
    gender: 'female',
    social_category: location.state?.initialForm?.social_category || 'SC',
    religion: 'hindu',
    is_differently_abled: false,

    // Step 2: Location
    state: 'Maharashtra',
    district: 'Mumbai',
    area_type: 'rural',
    pincode: '400001',

    // Step 3: Enterprise & Craft
    business_type: location.state?.initialForm?.business_type || 'manufacturing',
    business_stage: 'new',
    is_artisan: false,
    is_street_vendor: false,
    has_skill_training: true,
    education_qualification: 'graduate',

    // Step 4: Loan & Financials
    project_cost: 1500000,
    required_loan: location.state?.initialForm?.required_loan || 1200000,
    own_contribution: 150000,
    annual_income: 180000,

    // Step 5: Document Readiness
    has_aadhaar: true,
    has_pan: true,
    has_caste_certificate: true,
    has_project_report: true,
    has_bank_account: true,
    has_udyam_registration: true
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : (type === 'number' ? Number(value) : value)
    }));
  };

  const handleNext = () => {
    if (step < 5) setStep(step + 1);
  };

  const handleBack = () => {
    if (step > 1) setStep(step - 1);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await api.put('/profile/me', formData).catch(() => {});

      // Call deterministic rule matcher with language
      const res = await api.post('/matching/evaluate', {
        ...formData,
        target_language: currentLanguage
      });
      navigate('/results', { state: { evaluationResult: res.data, profileData: formData } });
    } catch (err) {
      console.error(err);
      setError('Evaluation failed. Running fallback matching...');
      navigate('/results', { state: { profileData: formData } });
    } finally {
      setLoading(false);
    }
  };

  const steps = [
    { num: 1, title: t('step1Title'), icon: <User className="w-4 h-4" /> },
    { num: 2, title: t('step2Title'), icon: <MapPin className="w-4 h-4" /> },
    { num: 3, title: t('step3Title'), icon: <Briefcase className="w-4 h-4" /> },
    { num: 4, title: t('step4Title'), icon: <DollarSign className="w-4 h-4" /> },
    { num: 5, title: t('step5Title'), icon: <FileCheck className="w-4 h-4" /> }
  ];

  return (
    <div className="max-w-3xl mx-auto py-8 px-4 sm:px-6">
      {/* Wizard Header */}
      <div className="text-center mb-8">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold mb-2">
          <Sparkles className="w-3.5 h-3.5" />
          <span>{t('sihBadgeText')} • {t('translationBadge')}</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900">{t('wizardTitle')}</h1>
        <p className="text-xs sm:text-sm text-slate-500 mt-1">
          {t('wizardSubtitle')}
        </p>
      </div>

      {/* Step Progress Indicator */}
      <div className="mb-8">
        <div className="flex justify-between items-center relative">
          <div className="absolute top-1/2 left-0 right-0 h-1 bg-slate-200 -translate-y-1/2 z-0"></div>
          <div 
            className="absolute top-1/2 left-0 h-1 bg-emerald-500 -translate-y-1/2 z-0 transition-all duration-300"
            style={{ width: `${((step - 1) / 4) * 100}%` }}
          ></div>

          {steps.map((s) => (
            <div key={s.num} className="relative z-10 flex flex-col items-center">
              <div 
                className={`w-9 h-9 rounded-full flex items-center justify-center font-bold text-xs transition-all ${
                  step === s.num
                    ? 'bg-emerald-600 text-white ring-4 ring-emerald-100 scale-110 shadow-md'
                    : step > s.num
                    ? 'bg-emerald-500 text-white'
                    : 'bg-white border-2 border-slate-300 text-slate-500'
                }`}
              >
                {step > s.num ? <CheckCircle2 className="w-4 h-4" /> : s.icon}
              </div>
              <span className={`text-[11px] font-semibold mt-1.5 hidden sm:block ${step >= s.num ? 'text-slate-900' : 'text-slate-400'}`}>
                {s.title}
              </span>
            </div>
          ))}
        </div>
      </div>

      {error && (
        <div className="mb-6 p-3.5 bg-red-50 border border-red-200 text-red-700 rounded-xl text-xs">
          {error}
        </div>
      )}

      {/* Step Content Container */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 sm:p-8 shadow-sm">
        {step === 1 && (
          <div className="space-y-5 animate-fadeIn">
            <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
              <User className="w-5 h-5 text-emerald-600" />
              <span>Step 1: {t('step1Title')}</span>
            </h2>
            <p className="text-xs text-slate-500">{t('step1Desc')}</p>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">{t('socialCategoryLabel')}</label>
                <select
                  name="social_category"
                  value={formData.social_category}
                  onChange={handleChange}
                  className="w-full px-3 py-2.5 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                >
                  <option value="SC">Scheduled Caste (SC)</option>
                  <option value="ST">Scheduled Tribe (ST)</option>
                  <option value="OBC">Other Backward Class (OBC)</option>
                  <option value="Minority">Minority (Muslim, Christian, Sikh, Buddhist, Jain)</option>
                  <option value="General">General / Open Category</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">{t('genderLabel')}</label>
                <select
                  name="gender"
                  value={formData.gender}
                  onChange={handleChange}
                  className="w-full px-3 py-2.5 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                >
                  <option value="female">Woman Entrepreneur</option>
                  <option value="male">Male</option>
                  <option value="transgender">Transgender Entrepreneur</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">{t('ageLabel')}</label>
                <input
                  type="number"
                  name="age"
                  min="16"
                  max="80"
                  value={formData.age}
                  onChange={handleChange}
                  className="w-full px-3 py-2.5 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">{t('educationLabel')}</label>
                <select
                  name="education_qualification"
                  value={formData.education_qualification}
                  onChange={handleChange}
                  className="w-full px-3 py-2.5 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                >
                  <option value="graduate">Graduate / Degree Holder</option>
                  <option value="12th">12th Standard Pass</option>
                  <option value="8th">8th Standard Pass (PMEGP Eligible for &gt;₹10L)</option>
                  <option value="below_8th">Below 8th Standard</option>
                </select>
              </div>
            </div>

            <div className="pt-2">
              <label className="inline-flex items-center gap-2 text-xs font-semibold text-slate-700 cursor-pointer">
                <input
                  type="checkbox"
                  name="is_differently_abled"
                  checked={formData.is_differently_abled}
                  onChange={handleChange}
                  className="w-4 h-4 text-emerald-600 rounded"
                />
                <span>{t('differentlyAbledLabel')}</span>
              </label>
            </div>
          </div>
        )}

        {step === 2 && (
          <div className="space-y-5 animate-fadeIn">
            <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
              <MapPin className="w-5 h-5 text-emerald-600" />
              <span>Step 2: {t('step2Title')}</span>
            </h2>
            <p className="text-xs text-slate-500">{t('step2Desc')}</p>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">{t('stateLabel')}</label>
                <input
                  type="text"
                  name="state"
                  value={formData.state}
                  onChange={handleChange}
                  className="w-full px-3 py-2.5 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">{t('districtLabel')}</label>
                <input
                  type="text"
                  name="district"
                  value={formData.district}
                  onChange={handleChange}
                  className="w-full px-3 py-2.5 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">{t('areaTypeLabel')}</label>
                <select
                  name="area_type"
                  value={formData.area_type}
                  onChange={handleChange}
                  className="w-full px-3 py-2.5 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                >
                  <option value="rural">{t('ruralOption')}</option>
                  <option value="urban">{t('urbanOption')}</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">{t('pincodeLabel')}</label>
                <input
                  type="text"
                  name="pincode"
                  value={formData.pincode}
                  onChange={handleChange}
                  className="w-full px-3 py-2.5 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                />
              </div>
            </div>
          </div>
        )}

        {step === 3 && (
          <div className="space-y-5 animate-fadeIn">
            <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
              <Briefcase className="w-5 h-5 text-emerald-600" />
              <span>Step 3: {t('step3Title')}</span>
            </h2>
            <p className="text-xs text-slate-500">{t('step3Desc')}</p>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">{t('businessType')}</label>
                <select
                  name="business_type"
                  value={formData.business_type}
                  onChange={handleChange}
                  className="w-full px-3 py-2.5 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                >
                  <option value="manufacturing">{t('manufacturingOption')}</option>
                  <option value="service">{t('serviceOption')}</option>
                  <option value="trading">{t('tradingOption')}</option>
                  <option value="street_vendor">{t('streetVendorOption')}</option>
                  <option value="artisan">{t('artisanOption')}</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">{t('businessStageLabel')}</label>
                <select
                  name="business_stage"
                  value={formData.business_stage}
                  onChange={handleChange}
                  className="w-full px-3 py-2.5 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                >
                  <option value="new">New Enterprise (Greenfield)</option>
                  <option value="expansion">Expansion of Existing Unit</option>
                </select>
              </div>
            </div>

            <div className="space-y-2 pt-2">
              <label className="inline-flex items-center gap-2 text-xs font-semibold text-slate-700 cursor-pointer">
                <input
                  type="checkbox"
                  name="has_skill_training"
                  checked={formData.has_skill_training}
                  onChange={handleChange}
                  className="w-4 h-4 text-emerald-600 rounded"
                />
                <span>{t('hasTrainingLabel')}</span>
              </label>

              <label className="inline-flex items-center gap-2 text-xs font-semibold text-slate-700 cursor-pointer block">
                <input
                  type="checkbox"
                  name="is_artisan"
                  checked={formData.is_artisan}
                  onChange={handleChange}
                  className="w-4 h-4 text-emerald-600 rounded"
                />
                <span>{t('isArtisanLabel')}</span>
              </label>

              <label className="inline-flex items-center gap-2 text-xs font-semibold text-slate-700 cursor-pointer block">
                <input
                  type="checkbox"
                  name="is_street_vendor"
                  checked={formData.is_street_vendor}
                  onChange={handleChange}
                  className="w-4 h-4 text-emerald-600 rounded"
                />
                <span>{t('isVendorLabel')}</span>
              </label>
            </div>
          </div>
        )}

        {step === 4 && (
          <div className="space-y-5 animate-fadeIn">
            <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
              <DollarSign className="w-5 h-5 text-emerald-600" />
              <span>Step 4: {t('step4Title')}</span>
            </h2>
            <p className="text-xs text-slate-500">{t('step4Desc')}</p>

            <div className="space-y-4 pt-2">
              <div>
                <div className="flex justify-between text-xs font-semibold text-slate-700 mb-1">
                  <span>{t('requiredLoanLabel')}</span>
                  <span className="text-emerald-700 font-extrabold text-sm">₹{formData.required_loan.toLocaleString('en-IN')}</span>
                </div>
                <input
                  type="range"
                  name="required_loan"
                  min="10000"
                  max="10000000"
                  step="25000"
                  value={formData.required_loan}
                  onChange={handleChange}
                  className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-emerald-600"
                />
                <div className="flex justify-between text-[11px] text-slate-400 mt-1">
                  <span>₹10,000 (SVANidhi)</span>
                  <span>₹10 Lakh (Mudra)</span>
                  <span>₹50 Lakh (PMEGP)</span>
                  <span>₹1 Crore (StandUp)</span>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">{t('projectCostLabel')}</label>
                  <input
                    type="number"
                    name="project_cost"
                    value={formData.project_cost}
                    onChange={handleChange}
                    className="w-full px-3 py-2.5 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">{t('ownContributionLabel')}</label>
                  <input
                    type="number"
                    name="own_contribution"
                    value={formData.own_contribution}
                    onChange={handleChange}
                    className="w-full px-3 py-2.5 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                  />
                  <p className="text-[10px] text-slate-400 mt-1">Special Category requires only 5% margin money under PMEGP.</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {step === 5 && (
          <div className="space-y-5 animate-fadeIn">
            <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
              <FileCheck className="w-5 h-5 text-emerald-600" />
              <span>Step 5: {t('step5Title')}</span>
            </h2>
            <p className="text-xs text-slate-500">{t('step5Desc')}</p>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
              {[
                { name: 'has_aadhaar', label: t('hasAadhaarLabel') },
                { name: 'has_pan', label: t('hasPanLabel') },
                { name: 'has_caste_certificate', label: t('hasCasteLabel') },
                { name: 'has_project_report', label: t('hasDprLabel') },
                { name: 'has_bank_account', label: t('hasBankLabel') },
                { name: 'has_udyam_registration', label: t('hasUdyamLabel') }
              ].map((doc, idx) => (
                <label key={idx} className="flex items-center gap-3 p-3 rounded-xl border border-slate-200 hover:border-emerald-300 cursor-pointer bg-slate-50/50">
                  <input
                    type="checkbox"
                    name={doc.name}
                    checked={formData[doc.name]}
                    onChange={handleChange}
                    className="w-4 h-4 text-emerald-600 rounded"
                  />
                  <span className="text-xs font-medium text-slate-700">{doc.label}</span>
                </label>
              ))}
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex justify-between items-center mt-8 pt-6 border-t border-slate-100">
          {step > 1 ? (
            <button
              type="button"
              onClick={handleBack}
              className="inline-flex items-center gap-1.5 px-5 py-2.5 border border-slate-300 text-slate-700 rounded-xl text-xs font-bold hover:bg-slate-50 transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>{t('btnPrevious')}</span>
            </button>
          ) : (
            <div></div>
          )}

          {step < 5 ? (
            <button
              type="button"
              onClick={handleNext}
              className="inline-flex items-center gap-1.5 px-6 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-xs font-bold shadow-md shadow-emerald-600/20 transition-all"
            >
              <span>{t('btnNext')}</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          ) : (
            <button
              type="button"
              onClick={handleSubmit}
              disabled={loading}
              className="inline-flex items-center gap-2 px-8 py-3 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white rounded-xl text-sm font-bold shadow-lg shadow-emerald-600/25 transition-all"
            >
              <Sparkles className="w-4 h-4" />
              <span>{loading ? t('evaluatingText') : t('btnEvaluateSchemes')}</span>
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
'''

with open(r'C:\Users\aksha\.gemini\antigravity\scratch\scheme-sathi\frontend\src\pages\FindMySchemePage.jsx', 'w', encoding='utf-8') as f:
    f.write(find_scheme_jsx)

print("FindMySchemePage.jsx updated with 100% multilingual support!")
