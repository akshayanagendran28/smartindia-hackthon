import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { 
  Sparkles, ArrowRight, ArrowLeft, CheckCircle2, User, MapPin, 
  Briefcase, DollarSign, FileCheck, ShieldCheck, GraduationCap, Hammer, Store, Info,
  BookOpen, Building2, HelpCircle, Layers
} from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { useApplication } from '../context/ApplicationContext';
import { locationsAPI, questionsAPI } from '../services/api';
import StepProgressIndicator from '../components/StepProgressIndicator';

export default function FindMySchemePage() {
  const { t } = useLanguage();
  const location = useLocation();
  const { 
    application, 
    purposeType, 
    updatePurposeType, 
    updateApplication, 
    updateLoanAmount, 
    confirmAndSaveProfile 
  } = useApplication();
  const navigate = useNavigate();

  // Pick up any initialForm passed from LandingPage
  useEffect(() => {
    if (location.state?.initialForm) {
      const init = location.state.initialForm;
      if (init.purpose_type && init.purpose_type !== purposeType) {
        updatePurposeType(init.purpose_type);
      }
      setFormData(prev => ({
        ...prev,
        ...init,
        loanAmount: init.required_loan || prev.loanAmount,
        required_loan_amount: init.required_loan || prev.required_loan_amount
      }));
      if (init.required_loan) {
        updateLoanAmount(init.required_loan);
      }
    }
  }, [location.state]);

  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [questionsData, setQuestionsData] = useState([]);
  const [purposeOptions, setPurposeOptions] = useState([]);
  
  // Location dropdown states
  const [statesList, setStatesList] = useState([]);
  const [districtsList, setDistrictsList] = useState([]);
  const [loadingDistricts, setLoadingDistricts] = useState(false);

  // Form state
  const [formData, setFormData] = useState({
    ...application,
    purpose_type: purposeType || 'EDUCATION',
    location_state: application.location_state || application.state || 'Maharashtra',
    location_district: application.location_district || application.district || 'Mumbai',
    annual_family_income: application.annual_family_income || 250000,
    required_loan_amount: application.loanAmount || 450000,
  });

  // 1. Fetch Purpose Options and Dynamic Questions when purposeType changes
  useEffect(() => {
    questionsAPI.getPurposes()
      .then(res => setPurposeOptions(res.data || []))
      .catch(err => console.warn('Could not load purposes', err));

    setLoading(true);
    questionsAPI.getQuestions(purposeType)
      .then(res => {
        if (res.data && res.data.questions) {
          setQuestionsData(res.data.questions);
          // Set initial defaults from questionnaire if not already present
          const defaults = {};
          res.data.questions.forEach(q => {
            if (formData[q.id] === undefined && q.default !== undefined) {
              defaults[q.id] = q.default;
            }
          });
          setFormData(prev => ({ ...prev, ...defaults }));
        }
      })
      .catch(err => console.warn('Could not load dynamic questions', err))
      .finally(() => setLoading(false));
  }, [purposeType]);

  // 2. Load States
  useEffect(() => {
    locationsAPI.getStates()
      .then(res => {
        if (res.data && res.data.length > 0) {
          setStatesList(res.data);
        }
      })
      .catch(err => console.warn('Could not load states', err));
  }, []);

  // 3. Load Districts when State changes
  const activeState = formData.location_state || formData.state || 'Maharashtra';
  useEffect(() => {
    if (activeState) {
      setLoadingDistricts(true);
      locationsAPI.getDistricts(activeState)
        .then(res => {
          const list = res.data?.districts || [];
          setDistrictsList(list);
          if (list.length > 0 && (!formData.location_district || !list.includes(formData.location_district))) {
            setFormData(prev => ({ ...prev, location_district: list[0], district: list[0] }));
            updateApplication({ location_state: activeState, location_district: list[0], state: activeState, district: list[0] });
          }
        })
        .catch(err => {
          console.warn('Could not load districts for state', activeState, err);
          setDistrictsList([]);
        })
        .finally(() => setLoadingDistricts(false));
    }
  }, [activeState]);

  // Handle Purpose Switcher
  const handlePurposeChange = (newPurpose) => {
    updatePurposeType(newPurpose);
    setFormData(prev => ({
      ...prev,
      purpose_type: newPurpose,
      purposeType: newPurpose
    }));
    setStep(1);
  };

  // Generic Field Change Handler
  const handleChange = (fieldId, value) => {
    setFormData(prev => {
      const updated = { ...prev, [fieldId]: value };
      
      // Auto-calculate required loan for education if fee/duration change
      if (purposeType === 'EDUCATION' && (fieldId === 'annual_course_fee' || fieldId === 'course_duration_years')) {
        const fee = Number(fieldId === 'annual_course_fee' ? value : prev.annual_course_fee) || 120000;
        const dur = Number(fieldId === 'course_duration_years' ? value : prev.course_duration_years) || 4;
        const totalFee = fee * dur;
        const estimatedLoan = Math.round(totalFee * 0.9);
        updated.required_loan_amount = estimatedLoan;
        updated.loanAmount = estimatedLoan;
        updated.required_loan = estimatedLoan;
        updated.project_cost = totalFee;
        updateLoanAmount(estimatedLoan);
      }

      if (fieldId === 'required_loan_amount' || fieldId === 'loanAmount') {
        updated.loanAmount = Number(value);
        updated.required_loan = Number(value);
        updated.required_loan_amount = Number(value);
        updateLoanAmount(value);
      }

      if (fieldId === 'location_state') {
        updated.state = value;
      }
      if (fieldId === 'location_district') {
        updated.district = value;
      }

      updateApplication(updated);
      return updated;
    });
  };

  const handleNext = () => {
    if (step < 3) {
      setStep(step + 1);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else {
      // Step 3 Confirmation: Save and advance to Document Assistant
      confirmAndSaveProfile(formData);
      navigate('/documents');
    }
  };

  const handleBack = () => {
    if (step > 1) {
      setStep(step - 1);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  // Filter questions by Step
  const totalQuestions = questionsData.length;
  const step1Questions = questionsData.slice(0, Math.ceil(totalQuestions / 2));
  const step2Questions = questionsData.slice(Math.ceil(totalQuestions / 2));

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {/* Step Progress Workflow */}
      <StepProgressIndicator currentStep={2} />

      {/* Header Banner */}
      <div className="bg-gradient-to-r from-teal-700 via-emerald-700 to-teal-800 rounded-2xl p-6 text-white shadow-xl mb-8">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className="bg-emerald-400/20 text-emerald-200 text-xs font-semibold px-2.5 py-0.5 rounded-full border border-emerald-400/30">
                {t('SIH26092 Official myScheme Intelligence')}
              </span>
            </div>
            <h1 className="text-2xl md:text-3xl font-bold tracking-tight">
              {t('Dynamic Scheme Eligibility & Recommendation Engine')}
            </h1>
            <p className="text-teal-100 text-sm mt-1">
              {t('Select your track. All subsequent questions, documents, loan ceilings, and subsidies will dynamically adapt.')}
            </p>
          </div>
          <div className="bg-white/10 backdrop-blur-md rounded-xl p-3 border border-white/20 text-center min-w-[140px]">
            <span className="text-xs text-teal-200 uppercase font-bold tracking-wider block">{t('Target Track')}</span>
            <span className="text-lg font-bold text-white capitalize">{t(purposeType)}</span>
          </div>
        </div>
      </div>

      {/* 1. Track Selector / Purpose Tabs */}
      <div className="bg-white rounded-2xl p-4 shadow-sm border border-slate-200 mb-8">
        <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-3">
          {t('Step 1: Choose Your Primary Focus / Objective')}
        </label>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          <button
            type="button"
            onClick={() => handlePurposeChange('EDUCATION')}
            className={`p-4 rounded-xl border-2 text-left transition-all relative ${
              purposeType === 'EDUCATION'
                ? 'border-emerald-600 bg-emerald-50/70 shadow-md ring-2 ring-emerald-500/20'
                : 'border-slate-200 hover:border-slate-300 bg-white'
            }`}
          >
            <div className="flex items-start gap-3">
              <div className={`p-2.5 rounded-lg ${purposeType === 'EDUCATION' ? 'bg-emerald-600 text-white' : 'bg-slate-100 text-slate-600'}`}>
                <GraduationCap className="h-6 w-6" />
              </div>
              <div>
                <span className="font-bold text-slate-900 block text-sm">{t('Education & Student Loans')}</span>
                <span className="text-xs text-slate-500 line-clamp-2 mt-0.5">
                  {t('CSIS 100% interest subsidy, NSFDC, NBCFDC, CGFSEL up to ₹7.5L collateral-free.')}
                </span>
                <span className="inline-block mt-2 text-[11px] font-semibold text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded">
                  {t('6 Verified Schemes')}
                </span>
              </div>
            </div>
            {purposeType === 'EDUCATION' && (
              <CheckCircle2 className="h-5 w-5 text-emerald-600 absolute top-3 right-3" />
            )}
          </button>

          <button
            type="button"
            onClick={() => handlePurposeChange('BUSINESS')}
            className={`p-4 rounded-xl border-2 text-left transition-all relative ${
              purposeType === 'BUSINESS'
                ? 'border-teal-600 bg-teal-50/70 shadow-md ring-2 ring-teal-500/20'
                : 'border-slate-200 hover:border-slate-300 bg-white'
            }`}
          >
            <div className="flex items-start gap-3">
              <div className={`p-2.5 rounded-lg ${purposeType === 'BUSINESS' ? 'bg-teal-600 text-white' : 'bg-slate-100 text-slate-600'}`}>
                <Building2 className="h-6 w-6" />
              </div>
              <div>
                <span className="font-bold text-slate-900 block text-sm">{t('Business & Enterprise Setup')}</span>
                <span className="text-xs text-slate-500 line-clamp-2 mt-0.5">
                  {t('PMEGP up to 35% margin grant, Stand-Up India up to ₹1 Cr, State CMEGP/NEEDS.')}
                </span>
                <span className="inline-block mt-2 text-[11px] font-semibold text-teal-700 bg-teal-100 px-2 py-0.5 rounded">
                  {t('12 Verified Schemes')}
                </span>
              </div>
            </div>
            {purposeType === 'BUSINESS' && (
              <CheckCircle2 className="h-5 w-5 text-teal-600 absolute top-3 right-3" />
            )}
          </button>

          <button
            type="button"
            onClick={() => handlePurposeChange('SELF_EMPLOYMENT')}
            className={`p-4 rounded-xl border-2 text-left transition-all relative ${
              purposeType === 'SELF_EMPLOYMENT'
                ? 'border-amber-600 bg-amber-50/70 shadow-md ring-2 ring-amber-500/20'
                : 'border-slate-200 hover:border-slate-300 bg-white'
            }`}
          >
            <div className="flex items-start gap-3">
              <div className={`p-2.5 rounded-lg ${purposeType === 'SELF_EMPLOYMENT' ? 'bg-amber-600 text-white' : 'bg-slate-100 text-slate-600'}`}>
                <Hammer className="h-6 w-6" />
              </div>
              <div>
                <span className="font-bold text-slate-900 block text-sm">{t('Self-Employment & Artisans')}</span>
                <span className="text-xs text-slate-500 line-clamp-2 mt-0.5">
                  {t('PM SVANidhi 7% subvention, PM Vishwakarma toolkit grant & ₹3L concessional credit.')}
                </span>
                <span className="inline-block mt-2 text-[11px] font-semibold text-amber-700 bg-amber-100 px-2 py-0.5 rounded">
                  {t('5 Verified Schemes')}
                </span>
              </div>
            </div>
            {purposeType === 'SELF_EMPLOYMENT' && (
              <CheckCircle2 className="h-5 w-5 text-amber-600 absolute top-3 right-3" />
            )}
          </button>
        </div>
      </div>

      {/* Main Questionnaire Card */}
      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden mb-8">
        {/* Step Tabs Header */}
        <div className="flex border-b border-slate-200 bg-slate-50/50">
          <button
            type="button"
            onClick={() => setStep(1)}
            className={`flex-1 py-4 px-4 text-center font-semibold text-sm flex items-center justify-center gap-2 border-b-2 transition-colors ${
              step === 1
                ? 'border-emerald-600 text-emerald-700 bg-white'
                : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            <span className={`w-6 h-6 rounded-full flex items-center justify-center text-xs ${
              step === 1 ? 'bg-emerald-600 text-white' : 'bg-slate-200 text-slate-600'
            }`}>1</span>
            {t('Applicant Profile & Demographics')}
          </button>
          <button
            type="button"
            onClick={() => setStep(2)}
            className={`flex-1 py-4 px-4 text-center font-semibold text-sm flex items-center justify-center gap-2 border-b-2 transition-colors ${
              step === 2
                ? 'border-emerald-600 text-emerald-700 bg-white'
                : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            <span className={`w-6 h-6 rounded-full flex items-center justify-center text-xs ${
              step === 2 ? 'bg-emerald-600 text-white' : 'bg-slate-200 text-slate-600'
            }`}>2</span>
            {purposeType === 'EDUCATION' ? t('Academic & Financial Details') : t('Enterprise & Financial Quantum')}
          </button>
          <button
            type="button"
            onClick={() => setStep(3)}
            className={`flex-1 py-4 px-4 text-center font-semibold text-sm flex items-center justify-center gap-2 border-b-2 transition-colors ${
              step === 3
                ? 'border-emerald-600 text-emerald-700 bg-white'
                : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            <span className={`w-6 h-6 rounded-full flex items-center justify-center text-xs ${
              step === 3 ? 'bg-emerald-600 text-white' : 'bg-slate-200 text-slate-600'
            }`}>3</span>
            {t('Review & Unlock Documents')}
          </button>
        </div>

        <div className="p-6 md:p-8">
          {/* STEP 1: Applicant Profile Questions */}
          {step === 1 && (
            <div className="space-y-6">
              <div className="border-b border-slate-100 pb-4 mb-4">
                <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                  <User className="h-5 w-5 text-emerald-600" />
                  {t('Applicant Eligibility Profile')}
                </h2>
                <p className="text-xs text-slate-500 mt-0.5">
                  {t('These core parameters determine statutory quotas, interest subventions, and eligibility bands.')}
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {step1Questions.map((q) => {
                  // Check dependency
                  if (q.depends_on) {
                    const depVal = formData[q.depends_on];
                    if (q.dependency_value !== undefined && depVal !== q.dependency_value) {
                      return null;
                    }
                  }

                  if (q.type === 'state_select') {
                    return (
                      <div key={q.id}>
                        <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                          {t(q.label)} {q.required && <span className="text-rose-500">*</span>}
                        </label>
                        <select
                          value={formData.location_state || formData.state || 'Maharashtra'}
                          onChange={(e) => handleChange('location_state', e.target.value)}
                          className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 bg-white text-slate-900 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 text-sm font-medium"
                        >
                          {statesList.map(s => {
                            const sName = typeof s === 'string' ? s : (s.name || s);
                            return (
                              <option key={sName} value={sName}>{t(sName)}</option>
                            );
                          })}
                        </select>
                      </div>
                    );
                  }

                  if (q.type === 'district_select') {
                    return (
                      <div key={q.id}>
                        <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                          {t(q.label)} {q.required && <span className="text-rose-500">*</span>}
                        </label>
                        <select
                          value={formData.location_district || formData.district || ''}
                          onChange={(e) => handleChange('location_district', e.target.value)}
                          disabled={loadingDistricts || districtsList.length === 0}
                          className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 bg-white text-slate-900 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 text-sm font-medium disabled:bg-slate-100"
                        >
                          {districtsList.map(d => (
                            <option key={d} value={d}>{t(d)}</option>
                          ))}
                        </select>
                      </div>
                    );
                  }

                  if (q.type === 'select') {
                    return (
                      <div key={q.id} className={q.options.length > 4 ? "md:col-span-2" : ""}>
                        <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                          {t(q.label)} {q.required && <span className="text-rose-500">*</span>}
                        </label>
                        <select
                          value={formData[q.id] || q.default || ''}
                          onChange={(e) => handleChange(q.id, e.target.value)}
                          className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 bg-white text-slate-900 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 text-sm font-medium"
                        >
                          {q.options.map(opt => (
                            <option key={opt.value} value={opt.value}>{t(opt.label)}</option>
                          ))}
                        </select>
                        {q.help_text && <p className="text-[11px] text-slate-500 mt-1">{t(q.help_text)}</p>}
                      </div>
                    );
                  }

                  if (q.type === 'boolean') {
                    return (
                      <div key={q.id} className="md:col-span-2 flex items-center justify-between p-3.5 rounded-xl bg-slate-50 border border-slate-200">
                        <div>
                          <label className="font-semibold text-slate-900 text-sm block">{t(q.label)}</label>
                          {q.help_text && <p className="text-xs text-slate-500 mt-0.5">{t(q.help_text)}</p>}
                        </div>
                        <input
                          type="checkbox"
                          checked={Boolean(formData[q.id])}
                          onChange={(e) => handleChange(q.id, e.target.checked)}
                          className="h-5 w-5 text-emerald-600 rounded border-slate-300 focus:ring-emerald-500"
                        />
                      </div>
                    );
                  }

                  return (
                    <div key={q.id}>
                      <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                        {t(q.label)} {q.required && <span className="text-rose-500">*</span>}
                      </label>
                      <input
                        type={q.type || 'text'}
                        min={q.min}
                        max={q.max}
                        value={formData[q.id] !== undefined ? formData[q.id] : (q.default || '')}
                        onChange={(e) => handleChange(q.id, q.type === 'number' ? Number(e.target.value) : e.target.value)}
                        className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-slate-900 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 text-sm font-medium"
                      />
                      {q.help_text && <p className="text-[11px] text-slate-500 mt-1">{t(q.help_text)}</p>}
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* STEP 2: Track Specific Questions (Academic / Financial Quantum) */}
          {step === 2 && (
            <div className="space-y-6">
              <div className="border-b border-slate-100 pb-4 mb-4">
                <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                  <DollarSign className="h-5 w-5 text-emerald-600" />
                  {purposeType === 'EDUCATION' ? t('Course & Loan Amount Breakdown') : t('Project Financial Structure')}
                </h2>
                <p className="text-xs text-slate-500 mt-0.5">
                  {purposeType === 'EDUCATION'
                    ? t('Enter institutional fee structure to compute the full interest subsidy and required loan amount.')
                    : t('Enter estimated project investment, promoter contribution, and required bank loan.')}
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {step2Questions.map((q) => {
                  if (q.depends_on) {
                    const depVal = formData[q.depends_on];
                    if (q.dependency_value !== undefined && depVal !== q.dependency_value) {
                      return null;
                    }
                  }

                  if (q.type === 'state_select') {
                    return (
                      <div key={q.id}>
                        <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                          {t(q.label)} {q.required && <span className="text-rose-500">*</span>}
                        </label>
                        <select
                          value={formData.location_state || formData.state || 'Maharashtra'}
                          onChange={(e) => handleChange('location_state', e.target.value)}
                          className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 bg-white text-slate-900 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 text-sm font-medium"
                        >
                          {statesList.map(s => {
                            const sName = typeof s === 'string' ? s : (s.name || s);
                            return (
                              <option key={sName} value={sName}>{t(sName)}</option>
                            );
                          })}
                        </select>
                      </div>
                    );
                  }

                  if (q.type === 'district_select') {
                    return (
                      <div key={q.id}>
                        <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                          {t(q.label)} {q.required && <span className="text-rose-500">*</span>}
                        </label>
                        <select
                          value={formData.location_district || formData.district || ''}
                          onChange={(e) => handleChange('location_district', e.target.value)}
                          disabled={loadingDistricts || districtsList.length === 0}
                          className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 bg-white text-slate-900 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 text-sm font-medium disabled:bg-slate-100"
                        >
                          {districtsList.map(d => (
                            <option key={d} value={d}>{t(d)}</option>
                          ))}
                        </select>
                      </div>
                    );
                  }

                  if (q.type === 'select') {
                    return (
                      <div key={q.id} className={q.options.length > 4 ? "md:col-span-2" : ""}>
                        <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                          {t(q.label)} {q.required && <span className="text-rose-500">*</span>}
                        </label>
                        <select
                          value={formData[q.id] || q.default || ''}
                          onChange={(e) => handleChange(q.id, e.target.value)}
                          className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 bg-white text-slate-900 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 text-sm font-medium"
                        >
                          {q.options.map(opt => (
                            <option key={opt.value} value={opt.value}>{t(opt.label)}</option>
                          ))}
                        </select>
                        {q.help_text && <p className="text-[11px] text-slate-500 mt-1">{t(q.help_text)}</p>}
                      </div>
                    );
                  }

                  if (q.type === 'boolean') {
                    return (
                      <div key={q.id} className="md:col-span-2 flex items-center justify-between p-3.5 rounded-xl bg-slate-50 border border-slate-200">
                        <div>
                          <label className="font-semibold text-slate-900 text-sm block">{t(q.label)}</label>
                          {q.help_text && <p className="text-xs text-slate-500 mt-0.5">{t(q.help_text)}</p>}
                        </div>
                        <input
                          type="checkbox"
                          checked={Boolean(formData[q.id])}
                          onChange={(e) => handleChange(q.id, e.target.checked)}
                          className="h-5 w-5 text-emerald-600 rounded border-slate-300 focus:ring-emerald-500"
                        />
                      </div>
                    );
                  }

                  return (
                    <div key={q.id}>
                      <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                        {t(q.label)} {q.required && <span className="text-rose-500">*</span>}
                      </label>
                      <input
                        type={q.type || 'text'}
                        min={q.min}
                        max={q.max}
                        value={formData[q.id] !== undefined ? formData[q.id] : (q.default || '')}
                        onChange={(e) => handleChange(q.id, q.type === 'number' ? Number(e.target.value) : e.target.value)}
                        className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-slate-900 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 text-sm font-medium"
                      />
                      {q.help_text && <p className="text-[11px] text-slate-500 mt-1">{t(q.help_text)}</p>}
                    </div>
                  );
                })}
              </div>

              {/* Live Financial Assistance Highlight Box */}
              <div className="bg-emerald-50/80 border border-emerald-200 rounded-xl p-4 mt-6">
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-emerald-600 text-white">
                    <Sparkles className="h-5 w-5" />
                  </div>
                  <div>
                    <h4 className="font-bold text-emerald-950 text-sm">
                      {purposeType === 'EDUCATION' ? t('Education Loan & 100% Subsidy Calculation') : t('Target Loan Quantum Sync')}
                    </h4>
                    <p className="text-xs text-emerald-800 mt-0.5">
                      {t('Single source of truth loan quantum:')} <strong>₹{(formData.required_loan_amount || formData.loanAmount || 0).toLocaleString('en-IN')}</strong>.
                      {purposeType === 'EDUCATION' && formData.annual_family_income <= 450000 && (
                        <span> {t('100% full interest subsidy applicable under CSIS during study tenure + 1 year!')}</span>
                      )}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* STEP 3: Review & Explicit Profile Confirmation */}
          {step === 3 && (
            <div className="space-y-6">
              <div className="border-b border-slate-100 pb-4 mb-4">
                <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                  <ShieldCheck className="h-5 w-5 text-emerald-600" />
                  {t('Review & Confirm Profile')}
                </h2>
                <p className="text-xs text-slate-500 mt-0.5">
                  {t('Confirm your details below. Once confirmed, you will proceed to the Document Verification Assistant.')}
                </p>
              </div>

              {/* Review Summary Grid */}
              <div className="bg-slate-50 rounded-xl p-5 border border-slate-200 space-y-4">
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4 text-sm">
                  <div>
                    <span className="text-xs text-slate-500 block">{t('Selected Track:')}</span>
                    <span className="font-bold text-slate-900 capitalize">{t(purposeType)}</span>
                  </div>
                  <div>
                    <span className="text-xs text-slate-500 block">{t('Social Category:')}</span>
                    <span className="font-bold text-slate-900">{t(formData.category || formData.social_category || 'General')}</span>
                  </div>
                  <div>
                    <span className="text-xs text-slate-500 block">{t('Annual Family Income:')}</span>
                    <span className="font-bold text-slate-900">₹{Number(formData.annual_family_income || 0).toLocaleString('en-IN')}</span>
                  </div>
                  <div>
                    <span className="text-xs text-slate-500 block">{t('Required Loan Amount:')}</span>
                    <span className="font-bold text-emerald-700 text-base">₹{Number(formData.required_loan_amount || formData.loanAmount || 0).toLocaleString('en-IN')}</span>
                  </div>
                  <div>
                    <span className="text-xs text-slate-500 block">{t('Resident Location:')}</span>
                    <span className="font-bold text-slate-900">{t(formData.location_district || formData.district)}, {t(formData.location_state || formData.state)}</span>
                  </div>
                  <div>
                    <span className="text-xs text-slate-500 block">
                      {purposeType === 'EDUCATION' ? t('Target Course:') : t('Enterprise Activity:')}
                    </span>
                    <span className="font-bold text-slate-900 truncate block">
                      {t(purposeType === 'EDUCATION' ? formData.course_type : formData.business_type)}
                    </span>
                  </div>
                </div>
              </div>

              {/* Next Step Document Readiness Banner */}
              <div className="bg-blue-50 border border-blue-200 rounded-xl p-4 flex items-start gap-3">
                <FileCheck className="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0" />
                <div className="text-xs text-blue-900">
                  <span className="font-bold block text-sm">{t('Next Step: Document Assistant Verification')}</span>
                  <span>
                    {purposeType === 'EDUCATION'
                      ? t('You will verify your 10th & 12th marksheets, Admission Offer Letter, Institutional Fee Schedule, and Income Certificate.')
                      : t('You will verify your Detailed Project Report (DPR), PAN Card, Income Certificate, and Caste Certificate.')}
                  </span>
                </div>
              </div>
            </div>
          )}

          {/* Action Navigation Buttons */}
          <div className="flex items-center justify-between pt-6 border-t border-slate-100 mt-8">
            <button
              type="button"
              onClick={handleBack}
              disabled={step === 1}
              className={`px-5 py-2.5 rounded-xl font-semibold text-sm flex items-center gap-2 transition-all ${
                step === 1
                  ? 'text-slate-300 cursor-not-allowed'
                  : 'text-slate-700 hover:bg-slate-100 border border-slate-200'
              }`}
            >
              <ArrowLeft className="h-4 w-4" />
              {t('Previous')}
            </button>

            <button
              type="button"
              onClick={handleNext}
              className="px-6 py-2.5 rounded-xl font-semibold text-sm bg-gradient-to-r from-emerald-600 to-teal-600 text-white hover:from-emerald-700 hover:to-teal-700 shadow-md shadow-emerald-500/20 flex items-center gap-2 transition-all"
            >
              {step === 3 ? (
                <>
                  <CheckCircle2 className="h-4 w-4" />
                  {t('Confirm & Proceed to Document Assistant')}
                </>
              ) : (
                <>
                  {t('Next Step')}
                  <ArrowRight className="h-4 w-4" />
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
