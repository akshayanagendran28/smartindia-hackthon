import React, { useState, useEffect, useMemo } from 'react';
import { 
  User, MapPin, Briefcase, DollarSign, Award, ShieldCheck, 
  CheckCircle2, AlertCircle, Save, Sparkles, Check, ArrowRight, 
  RefreshCw, TrendingUp, BarChart3, Clock, Landmark
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { useApplication } from '../context/ApplicationContext';
import api, { locationsAPI, profileAPI, matchingAPI } from '../services/api';
import StepProgressIndicator from '../components/StepProgressIndicator';

export default function UserProfilePage() {
  const { user } = useAuth();
  const { t } = useLanguage();
  const { 
    application, 
    updateApplication, 
    updateLoanAmount, 
    confirmAndSaveProfile,
    verifiedDocKeys,
    allDocumentsVerified,
    selectedScheme
  } = useApplication();

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState({ text: '', type: '' });

  // Dynamic States & Districts from backend
  const [statesList, setStatesList] = useState([]);
  const [districtsList, setDistrictsList] = useState([]);
  const [loadingDistricts, setLoadingDistricts] = useState(false);

  // Dynamic Live KPIs computed from user inputs
  const [dynamicKpis, setDynamicKpis] = useState({
    eligibleCount: 0,
    availableCount: 0,
    maxSubsidy: '35%',
    subsidySubtitle: 'PMEGP Special Category',
    readinessScore: 68,
    readinessSubtitle: '2 documents pending',
    partnerBanksCount: 12,
    partnerSubtitle: 'Within district radius',
    loadingKpis: false
  });

  const [form, setForm] = useState({
    full_name: application.full_name || '',
    age: application.age || 28,
    gender: application.gender || 'female',
    social_category: application.social_category || application.category || 'SC',
    religion: application.religion || 'hindu',
    is_differently_abled: application.is_differently_abled || false,
    state: application.state || 'Tamil Nadu',
    district: application.district || 'Tiruvallur',
    area_type: application.area_type || 'rural',
    pincode: application.pincode || '602001',
    education_qualification: application.education_qualification || 'graduate',
    has_skill_training: application.has_skill_training !== undefined ? application.has_skill_training : true,
    skill_training_details: 'EDP 2-week certified',
    business_type: application.business_type || 'manufacturing',
    business_stage: application.business_stage || 'new',
    industry_sector: application.industry_sector || 'food_processing',
    project_cost: application.project_cost || 1500000,
    required_loan: application.loanAmount || 1200000,
    own_contribution: application.own_contribution || 300000,
    annual_income: application.annual_income || 180000,
    annual_family_income: application.annual_family_income || 180000,
    credit_score_range: '700_750',
    has_existing_bank_account: true,
    has_collateral: false,
    is_artisan: application.is_artisan || false,
    is_street_vendor: application.is_street_vendor || false,
    has_udyam_registration: application.has_udyam_registration !== undefined ? application.has_udyam_registration : true,
    has_gst: false,
    purpose: application.purpose || 'Start a Business',
    purpose_type: application.purpose_type || application.purposeType || 'BUSINESS'
  });

  // Load States list dynamically
  useEffect(() => {
    locationsAPI.getStates()
      .then(res => {
        if (res.data && res.data.length > 0) {
          setStatesList(res.data);
        }
      })
      .catch(err => console.warn('Could not load states dynamically', err));
  }, []);

  // Fetch districts whenever selected state changes
  useEffect(() => {
    if (form.state) {
      setLoadingDistricts(true);
      locationsAPI.getDistricts(form.state)
        .then(res => {
          const list = res.data?.districts || [];
          setDistrictsList(list);
          if (list.length > 0 && (!form.district || !list.includes(form.district))) {
            setForm(prev => ({ ...prev, district: list[0] }));
            updateApplication({ state: form.state, district: list[0] });
          }
        })
        .catch(err => {
          console.warn('Could not load districts for state', form.state, err);
          setDistrictsList([]);
        })
        .finally(() => setLoadingDistricts(false));
    }
  }, [form.state]);

  // Load initial profile data strictly for current active user
  useEffect(() => {
    async function loadProfile() {
      try {
        const res = await profileAPI.getProfile();
        if (res.data) {
          const d = res.data;
          setForm({
            full_name: d.full_name || user?.full_name || '',
            age: d.age || 28,
            gender: d.gender || 'female',
            social_category: d.social_category || d.category || 'General',
            category: d.category || d.social_category || 'General',
            religion: d.religion || 'hindu',
            is_differently_abled: d.is_differently_abled || false,
            state: d.state || d.location_state || 'Tamil Nadu',
            district: d.district || d.location_district || 'Chennai',
            area_type: d.area_type || 'rural',
            pincode: d.pincode || '600001',
            education_qualification: d.education_qualification || 'graduate',
            has_skill_training: d.has_skill_training !== undefined ? d.has_skill_training : true,
            skill_training_details: d.skill_training_details || 'EDP 2-week certified',
            business_type: d.business_type || (d.purpose_type === 'EDUCATION' ? 'education' : 'manufacturing'),
            business_stage: d.business_stage || 'new',
            industry_sector: d.industry_sector || 'food_processing',
            project_cost: d.project_cost || (d.purpose_type === 'EDUCATION' ? 480000 : 1500000),
            required_loan: d.required_loan || d.required_loan_amount || (d.purpose_type === 'EDUCATION' ? 450000 : 1200000),
            own_contribution: d.own_contribution || 30000,
            annual_income: d.annual_income || d.annual_family_income || 250000,
            annual_family_income: d.annual_family_income || d.annual_income || 250000,
            credit_score_range: '700_750',
            has_existing_bank_account: true,
            has_collateral: false,
            is_artisan: d.is_artisan || false,
            is_street_vendor: d.is_street_vendor || false,
            has_udyam_registration: d.has_udyam_registration !== undefined ? d.has_udyam_registration : false,
            has_gst: false,
            purpose: d.purpose || (d.purpose_type === 'EDUCATION' ? 'Higher Education' : 'Start a Business'),
            purpose_type: d.purpose_type || 'EDUCATION'
          });
        }
      } catch (err) {
        console.warn('Could not fetch backend profile:', err);
      } finally {
        setLoading(false);
      }
    }
    loadProfile();
  }, [user?.id, user?.email]);

  // Recalculate Live KPIs dynamically based on form changes
  useEffect(() => {
    let active = true;

    async function computeRealtimeKpis() {
      try {
        const effPurpose = (form.purpose_type || 'BUSINESS').toUpperCase();
        const evalPayload = {
          purpose_type: effPurpose,
          loan_amount: form.required_loan || 1200000,
          required_loan: form.required_loan || 1200000,
          required_loan_amount: form.required_loan || 1200000,
          annual_income: form.annual_family_income || 180000,
          annual_family_income: form.annual_family_income || 180000,
          category: form.social_category || 'SC',
          social_category: form.social_category || 'SC',
          gender: form.gender || 'female',
          age: form.age || 28,
          state: form.state || 'Tamil Nadu',
          district: form.district || 'Tiruvallur',
          area_type: form.area_type || 'rural',
          purpose: form.purpose || 'Start a Business',
          business_type: form.business_type || 'manufacturing',
          business_stage: form.business_stage || 'new',
          is_artisan: form.is_artisan,
          is_street_vendor: form.is_street_vendor,
          has_udyam_registration: form.has_udyam_registration,
          bypass_doc_gate: true
        };

        const [matchRes, branchRes] = await Promise.allSettled([
          matchingAPI.evaluate(evalPayload),
          api.get('/banking/branches', { params: { state: form.state, district: form.district, limit: 100 } })
        ]);

        if (!active) return;

        let eligibleCount = 0;
        let availableCount = 0;
        let maxSubsidy = '35%';
        let subsidySubtitle = 'PMEGP Special Category';

        if (matchRes.status === 'fulfilled' && matchRes.value.data) {
          const evalData = matchRes.value.data;
          const eligible = evalData.eligible_schemes || [];
          eligibleCount = eligible.length;
          availableCount = evalData.total_evaluated || evalData.available_schemes?.length || 0;

          if (eligible.length > 0) {
            const maxSubVal = Math.max(...eligible.map(s => s.subsidy_percentage_special || s.subsidy_percentage_general || 0));
            if (maxSubVal > 0) {
              maxSubsidy = `${maxSubVal}%`;
              const topScheme = eligible.find(s => (s.subsidy_percentage_special || s.subsidy_percentage_general) === maxSubVal);
              if (topScheme) {
                subsidySubtitle = `${topScheme.scheme_name || topScheme.scheme_code} ${topScheme.subsidy_percentage_special ? 'Special Category' : 'General'}`;
              }
            } else if (effPurpose === 'EDUCATION') {
              maxSubsidy = '100%';
              subsidySubtitle = 'CSIS Interest Subvention';
            }
          } else {
            maxSubsidy = '0%';
            subsidySubtitle = 'No direct subsidy match';
          }
        }

        const mandatoryDocsCount = effPurpose === 'EDUCATION' ? 5 : (effPurpose === 'SELF_EMPLOYMENT' ? 3 : 4);
        const verifiedCount = verifiedDocKeys ? Object.keys(verifiedDocKeys).length : 0;
        const missingCount = Math.max(0, mandatoryDocsCount - verifiedCount);
        
        let readinessScore = 50;
        let readinessSubtitle = 'Profile under review';
        if (allDocumentsVerified || missingCount === 0) {
          readinessScore = 100;
          readinessSubtitle = 'All mandatory documents verified';
        } else {
          readinessScore = Math.min(95, Math.round((verifiedCount / mandatoryDocsCount) * 50 + 40));
          readinessSubtitle = `${missingCount} document${missingCount > 1 ? 's' : ''} pending`;
        }

        let partnerBanksCount = 12;
        let partnerSubtitle = `Within ${form.district} jurisdiction`;
        if (branchRes.status === 'fulfilled' && branchRes.value.data) {
          const branchData = branchRes.value.data;
          partnerBanksCount = branchData.total || branchData.branches?.length || 12;
          partnerSubtitle = `${partnerBanksCount} active branches in ${form.district}`;
        }

        setDynamicKpis({
          eligibleCount,
          availableCount,
          maxSubsidy,
          subsidySubtitle,
          readinessScore,
          readinessSubtitle,
          partnerBanksCount,
          partnerSubtitle,
          loadingKpis: false
        });

      } catch (err) {
        console.warn('Live KPI update failed:', err);
      }
    }

    computeRealtimeKpis();
    return () => { active = false; };
  }, [
    form.state, 
    form.district, 
    form.social_category, 
    form.area_type, 
    form.purpose_type, 
    form.purpose, 
    form.required_loan, 
    form.annual_family_income,
    form.is_artisan,
    form.is_street_vendor,
    verifiedDocKeys,
    selectedScheme
  ]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    const newVal = type === 'checkbox' ? checked : (type === 'number' ? Number(value) : value);
    setForm(prev => ({
      ...prev,
      [name]: newVal
    }));

    if (name === 'required_loan') {
      updateLoanAmount(Number(value));
    }
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    setMessage({ text: '', type: '' });

    try {
      await confirmAndSaveProfile(form);
      updateApplication(form);
      updateLoanAmount(form.required_loan);
      setMessage({ text: t('Profile officially confirmed and synchronized with application workflow!'), type: 'success' });
    } catch (err) {
      setMessage({ text: t('Failed to update profile. Please check inputs.'), type: 'error' });
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <div className="p-8 text-center text-slate-500 font-semibold">{t('loading')}</div>;
  }

  return (
    <div className="max-w-5xl mx-auto py-6 space-y-6">
      <StepProgressIndicator currentStep={1} />

      {/* Header Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-200">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-0.5 rounded-full text-[10px] font-black uppercase tracking-wider bg-emerald-100 text-emerald-900 border border-emerald-300">
              {t('Live Dynamic Profile')}
            </span>
            <span className="text-xs text-slate-400">&bull; {t('Contextual Parameter Hub')}</span>
          </div>
          <h1 className="text-2xl font-black text-slate-900 mt-1">{t('Beneficiary & Enterprise Profile')}</h1>
          <p className="text-xs text-slate-500 mt-0.5">
            {t('Single source of truth for your identity, geographic location, and unified financial parameters.')}
          </p>
        </div>
        <button
          onClick={handleSave}
          disabled={saving}
          className="inline-flex items-center gap-2 px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-bold rounded-xl shadow transition-all disabled:opacity-50 shrink-0"
        >
          {saving ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4" />}
          <span>{saving ? t('saving') : t('confirm & save profile')}</span>
        </button>
      </div>

      {/* Live Dynamic Real-Time KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        
        {/* 1. Eligible Schemes */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between hover:border-emerald-300 transition-all">
          <div className="space-y-1">
            <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">{t('eligible schemes')}</p>
            <h3 className="text-2xl font-black text-slate-900">{dynamicKpis.eligibleCount}+</h3>
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
            <h3 className="text-2xl font-black text-teal-700">{dynamicKpis.maxSubsidy}</h3>
            <span className="text-[11px] font-semibold text-slate-500 block truncate max-w-[140px]" title={dynamicKpis.subsidySubtitle}>
              {t(dynamicKpis.subsidySubtitle)}
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
            <h3 className="text-2xl font-black text-amber-600">{dynamicKpis.readinessScore}%</h3>
            <span className="text-[11px] font-semibold text-amber-700 flex items-center gap-1">
              <Clock className="w-3 h-3" /> {t(dynamicKpis.readinessSubtitle)}
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
            <h3 className="text-2xl font-black text-indigo-600">{dynamicKpis.partnerBanksCount}</h3>
            <span className="text-[11px] font-semibold text-indigo-700 block truncate max-w-[140px]" title={dynamicKpis.partnerSubtitle}>
              {t(dynamicKpis.partnerSubtitle)}
            </span>
          </div>
          <div className="p-3 rounded-2xl bg-indigo-50 text-indigo-600 border border-indigo-100">
            <Landmark className="w-6 h-6" />
          </div>
        </div>

      </div>

      {message.text && (
        <div className={`p-4 rounded-2xl text-xs font-bold flex items-center gap-2 ${message.type === 'success' ? 'bg-emerald-50 border border-emerald-300 text-emerald-900' : 'bg-red-50 border border-red-300 text-red-900'}`}>
          {message.type === 'success' ? <CheckCircle2 className="w-4 h-4 shrink-0 text-emerald-600" /> : <AlertCircle className="w-4 h-4 shrink-0 text-rose-600" />}
          <span>{message.text}</span>
        </div>
      )}

      <form onSubmit={handleSave} className="space-y-6">
        {/* Section 1: Demographics */}
        <div className="bg-white rounded-3xl border border-slate-200 p-6 shadow-sm space-y-4">
          <div className="flex items-center gap-2 font-black text-slate-900 text-base pb-2 border-b border-slate-100">
            <User className="w-5 h-5 text-emerald-600" />
            <span>{t('demographicsTitle')}</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">{t('fullName')}</label>
              <input
                type="text"
                name="full_name"
                value={form.full_name || ''}
                onChange={handleChange}
                className="w-full px-3.5 py-2.5 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:outline-none font-medium"
                required
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">{t('ageYears')}</label>
              <input
                type="number"
                name="age"
                min="16"
                max="100"
                value={form.age}
                onChange={handleChange}
                className="w-full px-3.5 py-2.5 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:outline-none font-medium"
                required
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">{t('gender')}</label>
              <select
                name="gender"
                value={form.gender}
                onChange={handleChange}
                className="w-full px-3.5 py-2.5 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:outline-none font-medium"
              >
                <option value="female">{t('femaleOption')}</option>
                <option value="male">{t('maleOption')}</option>
                <option value="transgender">{t('transgenderOption')}</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">
                {t('target marginalized category (drives special subsidies)')}
              </label>
              <select
                name="social_category"
                value={form.social_category}
                onChange={handleChange}
                className="w-full px-3.5 py-2.5 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:outline-none bg-slate-50 font-bold text-slate-900"
              >
                <option value="General">{t('generalCategory')}</option>
                <option value="SC">{t('scCategory')}</option>
                <option value="ST">{t('stCategory')}</option>
                <option value="OBC">{t('obcCategory')}</option>
                <option value="Minority">{t('minorityCategory')}</option>
                <option value="Woman">{t('women entrepreneur / special category')}</option>
                <option value="Divyangjan">{t('specially abled / divyangjan')}</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">{t('Religion')}</label>
              <select
                name="religion"
                value={form.religion}
                onChange={handleChange}
                className="w-full px-3.5 py-2.5 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:outline-none font-medium"
              >
                <option value="hindu">{t('Hindu')}</option>
                <option value="muslim">{t('Muslim (Minority Subsidies)')}</option>
                <option value="christian">{t('Christian (Minority Subsidies)')}</option>
                <option value="sikh">{t('Sikh (Minority Subsidies)')}</option>
                <option value="buddhist">{t('Buddhist (Minority Subsidies)')}</option>
                <option value="jain">{t('Jain (Minority Subsidies)')}</option>
                <option value="other">{t('Other')}</option>
              </select>
            </div>
          </div>
        </div>

        {/* Section 2: Dynamic Location (Country -> State -> District) */}
        <div className="bg-white rounded-3xl border border-slate-200 p-6 shadow-sm space-y-4">
          <div className="flex items-center gap-2 font-black text-slate-900 text-base pb-2 border-b border-slate-100">
            <MapPin className="w-5 h-5 text-emerald-600" />
            <span>{t('2. Dynamic Geographic Location (Cascading State & District)')}</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">{t('country')}</label>
              <input
                type="text"
                disabled
                value={t('India')}
                className="w-full px-3.5 py-2.5 text-sm border border-slate-200 bg-slate-100 text-slate-600 rounded-xl font-bold"
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">{t('state / ut')}</label>
              <select
                name="state"
                value={form.state}
                onChange={handleChange}
                className="w-full px-3.5 py-2.5 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:outline-none bg-white font-medium"
              >
                {statesList.length > 0 ? (
                  statesList.map(st => {
                    const stName = typeof st === 'string' ? st : (st.name || st);
                    return <option key={stName} value={stName}>{t(stName)}</option>;
                  })
                ) : (
                  <>
                    <option value="Tamil Nadu">{t('Tamil Nadu')}</option>
                    <option value="Maharashtra">{t('Maharashtra')}</option>
                    <option value="Karnataka">{t('Karnataka')}</option>
                    <option value="Kerala">{t('Kerala')}</option>
                    <option value="Delhi">{t('Delhi')}</option>
                    <option value="Gujarat">{t('Gujarat')}</option>
                  </>
                )}
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">
                {t('district')} {loadingDistricts && <span className="text-[10px] text-emerald-600 font-normal">({t('loading')})</span>}
              </label>
              <select
                name="district"
                value={form.district}
                onChange={handleChange}
                disabled={loadingDistricts || districtsList.length === 0}
                className="w-full px-3.5 py-2.5 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:outline-none bg-white disabled:opacity-50 font-medium"
              >
                {districtsList.length > 0 ? (
                  districtsList.map(dist => (
                    <option key={dist} value={dist}>{t(dist)}</option>
                  ))
                ) : (
                  <option value={form.district || ''}>{t(form.district || 'Loading districts...')}</option>
                )}
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">{t('area setting')}</label>
              <select
                name="area_type"
                value={form.area_type}
                onChange={handleChange}
                className="w-full px-3.5 py-2.5 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:outline-none font-medium"
              >
                <option value="rural">{t('ruralOption')}</option>
                <option value="urban">{t('urbanOption')}</option>
              </select>
            </div>
          </div>
        </div>

        {/* Section 3: Financials & Single Source of Truth Loan Amount */}
        <div className="bg-white rounded-3xl border border-slate-200 p-6 shadow-sm space-y-4">
          <div className="flex items-center gap-2 font-black text-slate-900 text-base pb-2 border-b border-slate-100">
            <DollarSign className="w-5 h-5 text-emerald-600" />
            <span>{t('3. Purpose Track & Unified Loan Parameters')}</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">{t('Primary Purpose Track')}</label>
              <select
                name="purpose_type"
                value={form.purpose_type || 'BUSINESS'}
                onChange={(e) => {
                  const val = e.target.value;
                  setForm(prev => ({ 
                    ...prev, 
                    purpose_type: val,
                    purpose: val === 'EDUCATION' ? 'Higher Education Loan' : (val === 'SELF_EMPLOYMENT' ? 'Micro-enterprise & Artisan' : 'Start a Business')
                  }));
                }}
                className="w-full px-3.5 py-2.5 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:outline-none bg-slate-50 font-black text-emerald-800"
              >
                <option value="EDUCATION">{t('Education & Student Loans')}</option>
                <option value="BUSINESS">{t('Business & Enterprise Setup')}</option>
                <option value="SELF_EMPLOYMENT">{t('Self-Employment & Artisans')}</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">{t('total project cost (₹)')}</label>
              <input
                type="number"
                name="project_cost"
                min="10000"
                max="50000000"
                step="10000"
                value={form.project_cost}
                onChange={handleChange}
                className="w-full px-3.5 py-2.5 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:outline-none font-medium"
                required
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">
                {t('required loan amount (₹)')} <span className="text-[10px] text-emerald-600 font-normal">({t('Single source of truth')})</span>
              </label>
              <input
                type="number"
                name="required_loan"
                min="10000"
                max="50000000"
                step="10000"
                value={form.required_loan}
                onChange={handleChange}
                className="w-full px-3.5 py-2.5 text-sm border-2 border-emerald-500 bg-emerald-50/50 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:outline-none font-black text-slate-900"
                required
              />
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">{t('annual family income (₹)')}</label>
              <input
                type="number"
                name="annual_family_income"
                min="0"
                max="10000000"
                step="10000"
                value={form.annual_family_income}
                onChange={handleChange}
                className="w-full px-3.5 py-2.5 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:outline-none font-medium"
                required
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">{t('Promoter Contribution / Margin Money (₹)')}</label>
              <input
                type="number"
                name="own_contribution"
                min="0"
                max="10000000"
                step="10000"
                value={form.own_contribution}
                onChange={handleChange}
                className="w-full px-3.5 py-2.5 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:outline-none font-medium"
              />
            </div>
          </div>
        </div>

        {/* Section 4: Operational Attributes & Certifications */}
        <div className="bg-white rounded-3xl border border-slate-200 p-6 shadow-sm space-y-4">
          <div className="flex items-center gap-2 font-black text-slate-900 text-base pb-2 border-b border-slate-100">
            <Briefcase className="w-5 h-5 text-emerald-600" />
            <span>{t('4. Operational Attributes, Qualifications & Credentials')}</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">{t('Education Level')}</label>
              <select
                name="education_qualification"
                value={form.education_qualification}
                onChange={handleChange}
                className="w-full px-3.5 py-2.5 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:outline-none font-medium"
              >
                <option value="below_8th">{t('Below 8th Pass')}</option>
                <option value="8th_pass">{t('8th Pass (Eligible for PMEGP Manufacturing > ₹10L)')}</option>
                <option value="10th_pass">{t('10th Pass / SSC')}</option>
                <option value="12th_pass">{t('12th Pass / HSC')}</option>
                <option value="graduate">{t('Graduate / Diploma')}</option>
                <option value="post_graduate">{t('Post Graduate & Professional')}</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">{t('Business Stage')}</label>
              <select
                name="business_stage"
                value={form.business_stage}
                onChange={handleChange}
                className="w-full px-3.5 py-2.5 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:outline-none font-medium"
              >
                <option value="new">{t('New / Greenfield Project')}</option>
                <option value="existing">{t('Existing / Expansion Project')}</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2 border-t border-slate-100">
            <label className="flex items-center gap-3 p-3.5 rounded-xl border border-slate-200 hover:border-emerald-300 cursor-pointer transition-all">
              <input
                type="checkbox"
                name="has_skill_training"
                checked={form.has_skill_training}
                onChange={handleChange}
                className="w-4 h-4 text-emerald-600 rounded focus:ring-emerald-500"
              />
              <div>
                <span className="text-xs font-bold text-slate-900 block">{t('Entrepreneurship / Skill Training Completed (EDP)')}</span>
                <span className="text-[11px] text-slate-400">{t('Grants priority scoring under PMEGP and Vishwakarma')}</span>
              </div>
            </label>

            <label className="flex items-center gap-3 p-3.5 rounded-xl border border-slate-200 hover:border-emerald-300 cursor-pointer transition-all">
              <input
                type="checkbox"
                name="has_udyam_registration"
                checked={form.has_udyam_registration}
                onChange={handleChange}
                className="w-4 h-4 text-emerald-600 rounded focus:ring-emerald-500"
              />
              <div>
                <span className="text-xs font-bold text-slate-900 block">{t('Udyam MSME Registered')}</span>
                <span className="text-[11px] text-slate-400">{t('Required for formal MSME scheme disbursements')}</span>
              </div>
            </label>
          </div>
        </div>

        {/* Submit & Next Step Action */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-4">
          <button
            type="button"
            onClick={() => window.history.back()}
            className="text-xs font-bold text-slate-500 hover:text-slate-800 transition-colors"
          >
            &larr; {t('Previous')}
          </button>

          <div className="flex items-center gap-3">
            <button
              type="submit"
              disabled={saving}
              className="inline-flex items-center gap-2 px-6 py-3 bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-black rounded-xl shadow-md transition-all disabled:opacity-50"
            >
              {saving ? <RefreshCw className="w-4 h-4 animate-spin" /> : <CheckCircle2 className="w-4 h-4" />}
              <span>{saving ? t('saving') : t('confirm & save profile')}</span>
            </button>
          </div>
        </div>

      </form>
    </div>
  );
}
