import React, { useState, useEffect } from 'react';
import { 
  User, MapPin, Briefcase, DollarSign, Award, ShieldCheck, 
  CheckCircle2, AlertCircle, Save, Sparkles, Check, ArrowRight, RefreshCw 
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { useApplication } from '../context/ApplicationContext';
import { locationsAPI, profileAPI } from '../services/api';
import StepProgressIndicator from '../components/StepProgressIndicator';

export default function UserProfilePage() {
  const { user } = useAuth();
  const { t } = useLanguage();
  const { 
    application, 
    updateApplication, 
    updateLoanAmount, 
    confirmAndSaveProfile 
  } = useApplication();

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState({ text: '', type: '' });

  // Dynamic States & Districts from backend
  const [statesList, setStatesList] = useState([]);
  const [districtsList, setDistrictsList] = useState([]);
  const [loadingDistricts, setLoadingDistricts] = useState(false);

  const [form, setForm] = useState({
    full_name: application.full_name || '',
    age: application.age || 28,
    gender: application.gender || 'female',
    social_category: application.category || 'SC',
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
    purpose: application.purpose || 'Start a Business'
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
          }
        })
        .catch(err => {
          console.warn('Could not load districts for state', form.state, err);
          setDistrictsList([]);
        })
        .finally(() => setLoadingDistricts(false));
    }
  }, [form.state]);

  // Load initial backend profile if available
  useEffect(() => {
    profileAPI.getProfile()
      .then(res => {
        if (res.data) {
          setForm(prev => ({
            ...prev,
            ...res.data,
            // Clean up legacy categories if any
            social_category: (res.data.social_category && res.data.social_category !== 'General' && res.data.social_category !== 'OBC') ? res.data.social_category : prev.social_category,
            required_loan: res.data.required_loan_amount || res.data.required_loan || prev.required_loan,
          }));
        }
      })
      .catch(err => console.log('Profile loading notice:', err))
      .finally(() => setLoading(false));
  }, []);

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
      setMessage({ text: 'Profile officially confirmed and synchronized with application workflow!', type: 'success' });
    } catch (err) {
      setMessage({ text: 'Failed to update profile. Please check inputs.', type: 'error' });
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <div className="p-8 text-center text-slate-500">Loading your profile data...</div>;
  }

  return (
    <div className="max-w-4xl mx-auto py-6 space-y-6">
      <StepProgressIndicator currentStep={1} />

      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-200">
        <div>
          <h1 className="text-2xl font-black text-slate-900">Beneficiary & Enterprise Profile</h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Single source of truth for your identity, location, and financial parameters.
          </p>
        </div>
        <button
          onClick={handleSave}
          disabled={saving}
          className="inline-flex items-center gap-2 px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-bold rounded-xl shadow transition-all disabled:opacity-50"
        >
          <Save className="w-4 h-4" />
          <span>{saving ? 'Saving...' : 'Confirm & Save Profile'}</span>
        </button>
      </div>

      {message.text && (
        <div className={`p-4 rounded-xl text-xs font-medium flex items-center gap-2 ${message.type === 'success' ? 'bg-emerald-50 border border-emerald-200 text-emerald-800' : 'bg-red-50 border border-red-200 text-red-700'}`}>
          {message.type === 'success' ? <CheckCircle2 className="w-4 h-4 shrink-0" /> : <AlertCircle className="w-4 h-4 shrink-0" />}
          <span>{message.text}</span>
        </div>
      )}

      <form onSubmit={handleSave} className="space-y-6">
        {/* Section 1: Demographics */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
          <div className="flex items-center gap-2 font-bold text-slate-900 text-base pb-2 border-b border-slate-100">
            <User className="w-5 h-5 text-emerald-600" />
            <span>1. Personal & Demographic Details</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Full Name</label>
              <input
                type="text"
                name="full_name"
                value={form.full_name || ''}
                onChange={handleChange}
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Age (Years)</label>
              <input
                type="number"
                name="age"
                min="16"
                max="100"
                value={form.age}
                onChange={handleChange}
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Gender</label>
              <select
                name="gender"
                value={form.gender}
                onChange={handleChange}
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              >
                <option value="female">Female / Woman</option>
                <option value="male">Male</option>
                <option value="transgender">Transgender</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Target Marginalized Category
              </label>
              <select
                name="social_category"
                value={form.social_category}
                onChange={handleChange}
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none bg-slate-50 font-medium"
              >
                <option value="SC">Scheduled Caste (SC)</option>
                <option value="ST">Scheduled Tribe (ST)</option>
                <option value="Minority">Minority (Muslim/Christian/Sikh/Buddhist/Jain/Parsi)</option>
                <option value="Woman">Women / Special Category</option>
                <option value="Divyangjan">Specially Abled / Divyangjan</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Religion</label>
              <select
                name="religion"
                value={form.religion}
                onChange={handleChange}
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              >
                <option value="hindu">Hindu</option>
                <option value="muslim">Muslim</option>
                <option value="christian">Christian</option>
                <option value="sikh">Sikh</option>
                <option value="buddhist">Buddhist</option>
                <option value="jain">Jain</option>
                <option value="other">Other</option>
              </select>
            </div>
          </div>
        </div>

        {/* Section 2: Dynamic Location (Country -> State -> District) */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
          <div className="flex items-center gap-2 font-bold text-slate-900 text-base pb-2 border-b border-slate-100">
            <MapPin className="w-5 h-5 text-emerald-600" />
            <span>2. Dynamic Geographic Location</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Country</label>
              <input
                type="text"
                disabled
                value="India"
                className="w-full px-3 py-2 text-sm border border-slate-200 bg-slate-100 text-slate-600 rounded-lg"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">State / Union Territory</label>
              <select
                name="state"
                value={form.state}
                onChange={handleChange}
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none bg-white"
              >
                {statesList.length > 0 ? (
                  statesList.map(st => (
                    <option key={st} value={st}>{st}</option>
                  ))
                ) : (
                  <>
                    <option value="Tamil Nadu">Tamil Nadu</option>
                    <option value="Maharashtra">Maharashtra</option>
                    <option value="Karnataka">Karnataka</option>
                    <option value="Kerala">Kerala</option>
                    <option value="Delhi">Delhi</option>
                    <option value="Gujarat">Gujarat</option>
                  </>
                )}
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                District {loadingDistricts && <span className="text-[10px] text-emerald-600">(Loading...)</span>}
              </label>
              <select
                name="district"
                value={form.district}
                onChange={handleChange}
                disabled={loadingDistricts || districtsList.length === 0}
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none bg-white disabled:opacity-50"
              >
                {districtsList.length > 0 ? (
                  districtsList.map(dist => (
                    <option key={dist} value={dist}>{dist}</option>
                  ))
                ) : (
                  <option value="">No districts available</option>
                )}
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Area Setting</label>
              <select
                name="area_type"
                value={form.area_type}
                onChange={handleChange}
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              >
                <option value="rural">Rural (35% Subsidy Quota)</option>
                <option value="urban">Urban (25% Subsidy Quota)</option>
              </select>
            </div>
          </div>
        </div>

        {/* Section 3: Financials & Single Loan Amount */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
          <div className="flex items-center gap-2 font-bold text-slate-900 text-base pb-2 border-b border-slate-100">
            <DollarSign className="w-5 h-5 text-emerald-600" />
            <span>3. Enterprise & Loan Parameters</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Primary Purpose</label>
              <select
                name="purpose"
                value={form.purpose}
                onChange={handleChange}
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              >
                <option value="Start a Business">Start a Business (Greenfield)</option>
                <option value="Expand Existing Business">Expand Existing Business</option>
                <option value="Higher Education">Higher Education Loan</option>
                <option value="Traditional Craft">Traditional Craft / PM Vishwakarma</option>
                <option value="Street Vending">Street Vending / PM SVANidhi</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Total Project Cost (₹)</label>
              <input
                type="number"
                name="project_cost"
                value={form.project_cost}
                onChange={handleChange}
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none font-mono"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Required Loan Amount (₹)</label>
              <input
                type="number"
                name="required_loan"
                value={form.required_loan}
                onChange={handleChange}
                className="w-full px-3 py-2 text-sm border border-emerald-500 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none font-mono font-bold text-emerald-800 bg-emerald-50/50"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-1">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Annual Family Income (₹)</label>
              <input
                type="number"
                name="annual_family_income"
                value={form.annual_family_income}
                onChange={handleChange}
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none font-mono"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Promoter Margin / Own Contribution (₹)</label>
              <input
                type="number"
                name="own_contribution"
                value={form.own_contribution}
                onChange={handleChange}
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none font-mono"
              />
            </div>
          </div>
        </div>

        <div className="flex justify-end gap-3 pt-2">
          <button
            type="submit"
            disabled={saving}
            className="px-6 py-3 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-xl shadow-md transition-all flex items-center gap-2 text-sm"
          >
            <Sparkles className="w-4 h-4" />
            <span>{saving ? 'Updating...' : 'Confirm & Save Profile'}</span>
          </button>
        </div>
      </form>
    </div>
  );
}
