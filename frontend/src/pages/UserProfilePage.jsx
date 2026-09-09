import React, { useState, useEffect } from 'react';
import { 
  User, MapPin, Briefcase, DollarSign, Award, ShieldCheck, 
  CheckCircle2, AlertCircle, Save, Sparkles 
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import api from '../services/api';

export default function UserProfilePage() {
  const { user } = useAuth();
  const { t } = useLanguage();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState({ text: '', type: '' });

  const [form, setForm] = useState({
    full_name: '',
    age: 28,
    gender: 'female',
    social_category: 'SC',
    religion: 'hindu',
    is_differently_abled: false,
    state: 'Maharashtra',
    district: 'Mumbai Suburban',
    area_type: 'urban',
    pincode: '400050',
    education_qualification: 'graduate',
    has_skill_training: true,
    skill_training_details: 'EDP 2-week certified',
    business_type: 'manufacturing',
    business_stage: 'new',
    industry_sector: 'food_processing',
    project_cost: 1500000,
    required_loan: 1200000,
    own_contribution: 150000,
    annual_income: 180000,
    credit_score_range: '700_750',
    has_existing_bank_account: true,
    has_collateral: false,
    is_artisan: false,
    is_street_vendor: false,
    has_udyam_registration: true,
    has_gst: false
  });

  useEffect(() => {
    api.get('/profile/me')
      .then(res => {
        if (res.data) {
          setForm(prev => ({ ...prev, ...res.data }));
        }
      })
      .catch(err => console.log('Profile loading notice:', err))
      .finally(() => setLoading(false));
  }, []);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setForm(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : (type === 'number' ? Number(value) : value)
    }));
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    setMessage({ text: '', type: '' });
    try {
      await api.put('/profile/me', form);
      setMessage({ text: 'Profile saved successfully! Deterministic eligibility updated.', type: 'success' });
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
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-200">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-900">Beneficiary & Enterprise Profile</h1>
          <p className="text-xs text-slate-500 mt-0.5">
            This information directly feeds the legal gazette rule engine for 100% accurate scheme recommendations.
          </p>
        </div>
        <button
          onClick={handleSave}
          disabled={saving}
          className="inline-flex items-center gap-2 px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-bold rounded-xl shadow transition-all disabled:opacity-50"
        >
          <Save className="w-4 h-4" />
          <span>{saving ? 'Saving...' : 'Save & Sync Eligibility'}</span>
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

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Social Category</label>
              <select
                name="social_category"
                value={form.social_category}
                onChange={handleChange}
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              >
                <option value="SC">Scheduled Caste (SC)</option>
                <option value="ST">Scheduled Tribe (ST)</option>
                <option value="OBC">Other Backward Class (OBC)</option>
                <option value="Minority">Minority (Muslim/Christian/Sikh/Buddhist/Jain/Parsi)</option>
                <option value="General">General / Unreserved</option>
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

            <div className="flex items-center gap-2 pt-6">
              <input
                type="checkbox"
                id="is_differently_abled"
                name="is_differently_abled"
                checked={form.is_differently_abled}
                onChange={handleChange}
                className="w-4 h-4 text-emerald-600 rounded border-slate-300 focus:ring-emerald-500"
              />
              <label htmlFor="is_differently_abled" className="text-xs font-semibold text-slate-700 cursor-pointer">
                Specially Abled (PwD &gt; 40%)
              </label>
            </div>
          </div>
        </div>

        {/* Section 2: Location */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
          <div className="flex items-center gap-2 font-bold text-slate-900 text-base pb-2 border-b border-slate-100">
            <MapPin className="w-5 h-5 text-emerald-600" />
            <span>2. Location & Habitat</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">State / UT</label>
              <input
                type="text"
                name="state"
                value={form.state}
                onChange={handleChange}
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">District</label>
              <input
                type="text"
                name="district"
                value={form.district}
                onChange={handleChange}
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Area Classification</label>
              <select
                name="area_type"
                value={form.area_type}
                onChange={handleChange}
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              >
                <option value="rural">Rural (Eligible for 35% PMEGP Subsidy)</option>
                <option value="urban">Urban (Eligible for 25% PMEGP Subsidy)</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Pincode</label>
              <input
                type="text"
                name="pincode"
                value={form.pincode}
                onChange={handleChange}
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              />
            </div>
          </div>
        </div>

        {/* Section 3: Enterprise & Project Details */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
          <div className="flex items-center gap-2 font-bold text-slate-900 text-base pb-2 border-b border-slate-100">
            <Briefcase className="w-5 h-5 text-emerald-600" />
            <span>3. Enterprise & Project Financials</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Business Type</label>
              <select
                name="business_type"
                value={form.business_type}
                onChange={handleChange}
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              >
                <option value="manufacturing">Manufacturing (Limit up to ₹50L)</option>
                <option value="service">Service Unit (Limit up to ₹20L)</option>
                <option value="trading">Trading / Retail</option>
                <option value="street_vendor">Street Vendor / Hawkers</option>
                <option value="artisan">Artisan / Traditional Craft</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Stage of Business</label>
              <select
                name="business_stage"
                value={form.business_stage}
                onChange={handleChange}
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              >
                <option value="new">New Enterprise (Greenfield)</option>
                <option value="expansion">Expansion / Modernization</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Education Level</label>
              <select
                name="education_qualification"
                value={form.education_qualification}
                onChange={handleChange}
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              >
                <option value="graduate">Graduate / Post-Graduate</option>
                <option value="12th">12th Standard Passed</option>
                <option value="8th">8th Standard Passed</option>
                <option value="below_8th">Below 8th Standard / Literate</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Total Project Cost (₹)</label>
              <input
                type="number"
                name="project_cost"
                value={form.project_cost}
                onChange={handleChange}
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Required Loan (₹)</label>
              <input
                type="number"
                name="required_loan"
                value={form.required_loan}
                onChange={handleChange}
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Own Contribution / Margin (₹)</label>
              <input
                type="number"
                name="own_contribution"
                value={form.own_contribution}
                onChange={handleChange}
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              />
            </div>
          </div>

          <div className="flex flex-wrap gap-6 pt-2">
            <label className="inline-flex items-center gap-2 text-xs font-semibold text-slate-700 cursor-pointer">
              <input
                type="checkbox"
                name="has_skill_training"
                checked={form.has_skill_training}
                onChange={handleChange}
                className="w-4 h-4 text-emerald-600 rounded"
              />
              <span>Has EDP / Skill Certification</span>
            </label>

            <label className="inline-flex items-center gap-2 text-xs font-semibold text-slate-700 cursor-pointer">
              <input
                type="checkbox"
                name="has_udyam_registration"
                checked={form.has_udyam_registration}
                onChange={handleChange}
                className="w-4 h-4 text-emerald-600 rounded"
              />
              <span>Has Udyam MSME Registration</span>
            </label>

            <label className="inline-flex items-center gap-2 text-xs font-semibold text-slate-700 cursor-pointer">
              <input
                type="checkbox"
                name="is_street_vendor"
                checked={form.is_street_vendor}
                onChange={handleChange}
                className="w-4 h-4 text-emerald-600 rounded"
              />
              <span>Street Vendor / Vending Certificate</span>
            </label>

            <label className="inline-flex items-center gap-2 text-xs font-semibold text-slate-700 cursor-pointer">
              <input
                type="checkbox"
                name="is_artisan"
                checked={form.is_artisan}
                onChange={handleChange}
                className="w-4 h-4 text-emerald-600 rounded"
              />
              <span>Traditional Artisan / Craftsman (Vishwakarma)</span>
            </label>
          </div>
        </div>

        <div className="flex justify-end gap-3 pt-2">
          <button
            type="submit"
            disabled={saving}
            className="px-6 py-3 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-xl shadow-md transition-all flex items-center gap-2 text-sm"
          >
            <Sparkles className="w-4 h-4" />
            <span>{saving ? 'Updating...' : 'Save & Evaluate Eligible Schemes'}</span>
          </button>
        </div>
      </form>
    </div>
  );
}
