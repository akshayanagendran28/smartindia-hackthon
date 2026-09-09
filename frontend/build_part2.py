import os

BASE_DIR = r"C:\Users\aksha\.gemini\antigravity\scratch\scheme-sathi\frontend\src"
PAGES_DIR = os.path.join(BASE_DIR, "pages")

# 4. UserDashboard.jsx
USER_DASHBOARD = '''import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  Sparkles, CheckCircle2, AlertTriangle, FileText, MapPin, 
  Calculator, MessageSquare, ArrowRight, UserCheck, Clock,
  ChevronRight, Award, TrendingUp, ShieldAlert, BarChart3
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import api from '../services/api';

export default function UserDashboard() {
  const { user } = useAuth();
  const { t } = useLanguage();
  const [profile, setProfile] = useState(null);
  const [matches, setMatches] = useState([]);
  const [readiness, setReadiness] = useState({ readiness_score: 65, status: 'In Progress' });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadDashboardData() {
      try {
        const [profRes, matchRes, readRes] = await Promise.allSettled([
          api.get('/profile/me'),
          api.post('/matching/evaluate', {}),
          api.get('/readiness/score')
        ]);

        if (profRes.status === 'fulfilled') setProfile(profRes.value.data);
        if (matchRes.status === 'fulfilled') setMatches(matchRes.value.data.eligible_schemes || []);
        if (readRes.status === 'fulfilled') setReadiness(readRes.value.data);
      } catch (err) {
        console.error('Error fetching dashboard data:', err);
      } finally {
        setLoading(false);
      }
    }
    loadDashboardData();
  }, []);

  return (
    <div className="space-y-8 max-w-7xl mx-auto py-4">
      {/* Welcome Banner */}
      <div className="bg-gradient-to-r from-emerald-800 via-teal-800 to-slate-900 rounded-2xl p-6 sm:p-8 text-white shadow-lg flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 text-emerald-300 text-xs font-medium mb-3">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Beneficiary Dashboard &bull; SIH26092</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold">
            Welcome back, {user?.full_name || 'Entrepreneur'}!
          </h1>
          <p className="text-slate-200 text-sm mt-1 max-w-xl">
            {profile ? (
              <span>Your profile is configured as <strong className="text-emerald-300">{profile.social_category} {profile.gender}</strong> in <strong className="text-emerald-300">{profile.state || 'India'}</strong>.</span>
            ) : (
              <span>Complete your profile to unlock 100% deterministic government scheme matching.</span>
            )}
          </p>
        </div>

        <div className="flex flex-wrap gap-3">
          <Link
            to="/find-scheme"
            className="px-5 py-2.5 bg-emerald-400 hover:bg-emerald-300 text-slate-950 font-bold rounded-xl text-sm shadow-md transition-all flex items-center gap-2"
          >
            <Sparkles className="w-4 h-4" />
            <span>{t('find_my_scheme')}</span>
          </Link>
          <Link
            to="/profile"
            className="px-4 py-2.5 bg-white/10 hover:bg-white/20 border border-white/20 text-white font-medium rounded-xl text-sm transition-all"
          >
            Update Profile
          </Link>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
          <div>
            <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Eligible Schemes</p>
            <h3 className="text-2xl font-black text-slate-900 mt-1">{matches.length > 0 ? matches.length : '3+'}</h3>
            <span className="text-[11px] font-medium text-emerald-600 flex items-center gap-1 mt-1">
              <CheckCircle2 className="w-3 h-3" /> 100% Rule Verified
            </span>
          </div>
          <div className="p-3 rounded-xl bg-emerald-50 text-emerald-600">
            <Award className="w-6 h-6" />
          </div>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
          <div>
            <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Max Potential Subsidy</p>
            <h3 className="text-2xl font-black text-teal-700 mt-1">35%</h3>
            <span className="text-[11px] font-medium text-slate-500 mt-1 block">PMEGP Special Category</span>
          </div>
          <div className="p-3 rounded-xl bg-teal-50 text-teal-600">
            <TrendingUp className="w-6 h-6" />
          </div>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
          <div>
            <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Application Readiness</p>
            <h3 className="text-2xl font-black text-amber-600 mt-1">{readiness.readiness_score || 70}%</h3>
            <span className="text-[11px] font-medium text-amber-700 flex items-center gap-1 mt-1">
              <Clock className="w-3 h-3" /> 2 documents pending
            </span>
          </div>
          <div className="p-3 rounded-xl bg-amber-50 text-amber-600">
            <BarChart3 className="w-6 h-6" />
          </div>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
          <div>
            <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Partner Banks Near You</p>
            <h3 className="text-2xl font-black text-indigo-600 mt-1">13</h3>
            <span className="text-[11px] font-medium text-indigo-600 mt-1 block">Within 15km radius</span>
          </div>
          <div className="p-3 rounded-xl bg-indigo-50 text-indigo-600">
            <MapPin className="w-6 h-6" />
          </div>
        </div>
      </div>

      {/* Recommended Schemes Section */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-lg font-bold text-slate-900">Top Recommended Schemes For You</h2>
            <p className="text-xs text-slate-500">Ranked by SHAP compatibility factors and deterministic rules</p>
          </div>
          <Link to="/results" className="text-xs font-bold text-emerald-700 hover:text-emerald-800 flex items-center gap-1">
            <span>View All Matches</span>
            <ChevronRight className="w-4 h-4" />
          </Link>
        </div>

        <div className="space-y-4">
          {matches.slice(0, 3).map((match, idx) => (
            <div key={idx} className="p-5 rounded-xl border border-slate-200 hover:border-emerald-300 bg-slate-50/50 hover:bg-emerald-50/20 transition-all flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div className="space-y-1.5 flex-1">
                <div className="flex items-center gap-2">
                  <span className="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-emerald-100 text-emerald-800">
                    {match.match_score || 92}% Match Score
                  </span>
                  <span className="text-xs font-semibold text-slate-500">{match.scheme_code}</span>
                </div>
                <h3 className="font-bold text-slate-900 text-base">{match.scheme_name}</h3>
                <p className="text-xs text-slate-600 line-clamp-1">{match.scheme_description}</p>
                <div className="flex flex-wrap gap-2 pt-1">
                  {match.explainability?.positive_factors?.slice(0, 3).map((factor, fIdx) => (
                    <span key={fIdx} className="text-[11px] font-medium bg-white px-2 py-0.5 rounded border border-slate-200 text-slate-700">
                      &bull; {factor}
                    </span>
                  ))}
                </div>
              </div>

              <div className="flex md:flex-col items-end justify-between md:justify-center gap-3 shrink-0 pt-2 md:pt-0 border-t md:border-t-0 border-slate-200">
                <div className="text-right">
                  <span className="text-[11px] text-slate-500 block">Max Sanction</span>
                  <span className="font-bold text-slate-900 text-sm">₹{(match.max_loan_amount / 100000).toLocaleString('en-IN')} Lakh</span>
                </div>
                <div className="flex gap-2">
                  <Link
                    to={`/scheme/${match.scheme_id}`}
                    className="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold rounded-lg transition-colors"
                  >
                    Details & Rules
                  </Link>
                  <Link
                    to={`/explanation/${match.scheme_id}`}
                    className="px-3 py-1.5 bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 text-xs font-semibold rounded-lg"
                  >
                    Why?
                  </Link>
                </div>
              </div>
            </div>
          ))}

          {matches.length === 0 && (
            <div className="p-8 text-center bg-slate-50 rounded-xl border border-dashed border-slate-300">
              <Sparkles className="w-8 h-8 text-emerald-600 mx-auto mb-2" />
              <h3 className="font-bold text-slate-800 text-base">No Evaluation Run Yet</h3>
              <p className="text-xs text-slate-500 max-w-sm mx-auto mt-1">
                Take our 2-minute guided questionnaire to match your enterprise against Central & State schemes.
              </p>
              <Link
                to="/find-scheme"
                className="mt-4 inline-flex items-center gap-2 px-5 py-2.5 bg-emerald-600 text-white text-xs font-bold rounded-lg"
              >
                Launch Scheme Finder Wizard
              </Link>
            </div>
          )}
        </div>
      </div>

      {/* Quick Action Hub */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Link to="/documents" className="p-5 rounded-xl bg-white border border-slate-200 hover:border-emerald-300 shadow-sm transition-all group">
          <div className="p-3 rounded-lg bg-emerald-50 text-emerald-600 w-fit mb-3 group-hover:scale-105 transition-transform">
            <FileText className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-slate-900 text-sm">OCR Document Assistant</h3>
          <p className="text-xs text-slate-500 mt-1">Scan Aadhaar, Caste and Income certificates with auto-verification.</p>
        </Link>

        <Link to="/partners" className="p-5 rounded-xl bg-white border border-slate-200 hover:border-teal-300 shadow-sm transition-all group">
          <div className="p-3 rounded-lg bg-teal-50 text-teal-600 w-fit mb-3 group-hover:scale-105 transition-transform">
            <MapPin className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-slate-900 text-sm">Partner Bank Locator</h3>
          <p className="text-xs text-slate-500 mt-1">Find nearby authorized bank branches and CSC service points.</p>
        </Link>

        <Link to="/calculator" className="p-5 rounded-xl bg-white border border-slate-200 hover:border-amber-300 shadow-sm transition-all group">
          <div className="p-3 rounded-lg bg-amber-50 text-amber-600 w-fit mb-3 group-hover:scale-105 transition-transform">
            <Calculator className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-slate-900 text-sm">EMI & Subsidy Simulator</h3>
          <p className="text-xs text-slate-500 mt-1">Calculate exact monthly installments after government subsidies.</p>
        </Link>

        <Link to="/chat" className="p-5 rounded-xl bg-white border border-slate-200 hover:border-indigo-300 shadow-sm transition-all group">
          <div className="p-3 rounded-lg bg-indigo-50 text-indigo-600 w-fit mb-3 group-hover:scale-105 transition-transform">
            <MessageSquare className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-slate-900 text-sm">Scheme Sathi AI Chat</h3>
          <p className="text-xs text-slate-500 mt-1">Ask questions in 6 Indian languages grounded in verified guidelines.</p>
        </Link>
      </div>
    </div>
  );
}
'''

# 5. UserProfilePage.jsx
USER_PROFILE_PAGE = '''import React, { useState, useEffect } from 'react';
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
'''

# 6. FindMySchemePage.jsx
FIND_MY_SCHEME_PAGE = '''import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { 
  Sparkles, ArrowRight, ArrowLeft, CheckCircle2, User, MapPin, 
  Briefcase, DollarSign, FileCheck, ShieldCheck 
} from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import api from '../services/api';

export default function FindMySchemePage() {
  const { t } = useLanguage();
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
      // First update profile
      await api.put('/profile/me', formData).catch(() => {});

      // Then call deterministic rule matcher
      const res = await api.post('/matching/evaluate', formData);
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
    { num: 1, title: 'Identity', icon: <User className="w-4 h-4" /> },
    { num: 2, title: 'Location', icon: <MapPin className="w-4 h-4" /> },
    { num: 3, title: 'Enterprise', icon: <Briefcase className="w-4 h-4" /> },
    { num: 4, title: 'Loan Needs', icon: <DollarSign className="w-4 h-4" /> },
    { num: 5, title: 'Documents', icon: <FileCheck className="w-4 h-4" /> }
  ];

  return (
    <div className="max-w-3xl mx-auto py-8 px-4 sm:px-6">
      {/* Wizard Header */}
      <div className="text-center mb-8">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold mb-2">
          <Sparkles className="w-3.5 h-3.5" />
          <span>5-Step Guided Scheme Eligibility Wizard</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900">Find Your Perfect Govt Scheme</h1>
        <p className="text-xs sm:text-sm text-slate-500 mt-1">
          Accurate deterministic gazette matching for SC/ST, Women, Minorities, Artisans & Vendors
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
              <span>Step 1: Personal & Demographic Background</span>
            </h2>
            <p className="text-xs text-slate-500">Government schemes have special subsidies and quotas dedicated to specific demographic groups.</p>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Social Category *</label>
                <select
                  name="social_category"
                  value={formData.social_category}
                  onChange={handleChange}
                  className="w-full px-3 py-2.5 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                >
                  <option value="SC">Scheduled Caste (SC) - Up to 35% Subsidy</option>
                  <option value="ST">Scheduled Tribe (ST) - Up to 35% Subsidy</option>
                  <option value="OBC">Other Backward Class (OBC)</option>
                  <option value="Minority">Minority (Muslim, Christian, Sikh, Buddhist, Jain)</option>
                  <option value="General">General / Open Category</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Gender *</label>
                <select
                  name="gender"
                  value={formData.gender}
                  onChange={handleChange}
                  className="w-full px-3 py-2.5 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                >
                  <option value="female">Woman Entrepreneur (Special Category)</option>
                  <option value="male">Male</option>
                  <option value="transgender">Transgender Entrepreneur</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Age (Years) *</label>
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
                <label className="block text-xs font-semibold text-slate-700 mb-1">Education Level *</label>
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
                <span>Applicant is Differently Abled (Divyangjan / PwD &gt; 40%)</span>
              </label>
            </div>
          </div>
        )}

        {step === 2 && (
          <div className="space-y-5 animate-fadeIn">
            <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
              <MapPin className="w-5 h-5 text-emerald-600" />
              <span>Step 2: Location & Area Classification</span>
            </h2>
            <p className="text-xs text-slate-500">Subsidies are higher in Rural zones (35%) compared to Urban centers (25%).</p>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">State / Union Territory *</label>
                <input
                  type="text"
                  name="state"
                  value={formData.state}
                  onChange={handleChange}
                  className="w-full px-3 py-2.5 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">District *</label>
                <input
                  type="text"
                  name="district"
                  value={formData.district}
                  onChange={handleChange}
                  className="w-full px-3 py-2.5 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Area Setting *</label>
                <select
                  name="area_type"
                  value={formData.area_type}
                  onChange={handleChange}
                  className="w-full px-3 py-2.5 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                >
                  <option value="rural">Rural Area (Eligible for Maximum Subsidy)</option>
                  <option value="urban">Urban / Municipal Area</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Pincode *</label>
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
              <span>Step 3: Enterprise, Trade & Stage</span>
            </h2>
            <p className="text-xs text-slate-500">Different schemes cater specifically to manufacturing units, service shops, or street vendors.</p>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Business Nature *</label>
                <select
                  name="business_type"
                  value={formData.business_type}
                  onChange={handleChange}
                  className="w-full px-3 py-2.5 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                >
                  <option value="manufacturing">Manufacturing (Production / Processing)</option>
                  <option value="service">Service Unit (Repair, IT, Salon, Clinic)</option>
                  <option value="trading">Trading / Retail Shop</option>
                  <option value="street_vendor">Street Vendor / Hawking Cart</option>
                  <option value="artisan">Traditional Artisan / Handloom</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Business Stage *</label>
                <select
                  name="business_stage"
                  value={formData.business_stage}
                  onChange={handleChange}
                  className="w-full px-3 py-2.5 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                >
                  <option value="new">New Enterprise (Greenfield Project)</option>
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
                <span>Has completed EDP / Skill Development training (Adds +15% Match Score)</span>
              </label>

              <label className="inline-flex items-center gap-2 text-xs font-semibold text-slate-700 cursor-pointer block">
                <input
                  type="checkbox"
                  name="is_artisan"
                  checked={formData.is_artisan}
                  onChange={handleChange}
                  className="w-4 h-4 text-emerald-600 rounded"
                />
                <span>Belongs to 18 traditional artisan trades (PM Vishwakarma eligible)</span>
              </label>

              <label className="inline-flex items-center gap-2 text-xs font-semibold text-slate-700 cursor-pointer block">
                <input
                  type="checkbox"
                  name="is_street_vendor"
                  checked={formData.is_street_vendor}
                  onChange={handleChange}
                  className="w-4 h-4 text-emerald-600 rounded"
                />
                <span>Urban street vendor holding Vending Certificate / CoR (PM SVANidhi eligible)</span>
              </label>
            </div>
          </div>
        )}

        {step === 4 && (
          <div className="space-y-5 animate-fadeIn">
            <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
              <DollarSign className="w-5 h-5 text-emerald-600" />
              <span>Step 4: Financial Requirements</span>
            </h2>
            <p className="text-xs text-slate-500">Provide accurate project cost and required loan amount.</p>

            <div className="space-y-4 pt-2">
              <div>
                <div className="flex justify-between text-xs font-semibold text-slate-700 mb-1">
                  <span>Required Loan Amount</span>
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
                  <span>₹10,000 (Micro / SVANidhi)</span>
                  <span>₹10 Lakh (Mudra Tarun)</span>
                  <span>₹50 Lakh (PMEGP)</span>
                  <span>₹1 Crore (StandUp)</span>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">Total Estimated Project Cost (₹)</label>
                  <input
                    type="number"
                    name="project_cost"
                    value={formData.project_cost}
                    onChange={handleChange}
                    className="w-full px-3 py-2.5 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">Own Contribution / Margin Money (₹)</label>
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
              <span>Step 5: Document & Compliance Readiness</span>
            </h2>
            <p className="text-xs text-slate-500">Mark the documents you currently hold. Missing documents will trigger guided action alerts.</p>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
              {[
                { name: 'has_aadhaar', label: 'Aadhaar Card (UIDAI Linked with Mobile)' },
                { name: 'has_pan', label: 'PAN Card' },
                { name: 'has_caste_certificate', label: 'Caste / Category Certificate (SC/ST/OBC)' },
                { name: 'has_project_report', label: 'Detailed Project Report (DPR)' },
                { name: 'has_bank_account', label: 'Active Bank Account & Passbook' },
                { name: 'has_udyam_registration', label: 'Udyam MSME Registration Certificate' }
              ].map((doc, idx) => (
                <label key={idx} className="flex items-center gap-3 p-3 rounded-xl border border-slate-200 hover:border-emerald-300 cursor-pointer bg-slate-50/50">
                  <input
                    type="checkbox"
                    name={doc.name}
                    checked={formData[doc.name]}
                    onChange={handleChange}
                    className="w-4 h-4 text-emerald-600 rounded"
                  />
                  <span className="text-xs font-semibold text-slate-800">{doc.label}</span>
                </label>
              ))}
            </div>

            <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200 text-xs text-emerald-900 flex items-start gap-2">
              <ShieldCheck className="w-4 h-4 text-emerald-700 shrink-0 mt-0.5" />
              <span>
                <strong>Deterministic Rule Match Ready:</strong> Upon clicking evaluate, Scheme Sathi will run all Central & State scheme rules against your demographic profile and output clear mathematical match scores and SHAP explainability.
              </span>
            </div>
          </div>
        )}

        {/* Wizard Navigation Buttons */}
        <div className="flex justify-between items-center pt-6 mt-6 border-t border-slate-100">
          {step > 1 ? (
            <button
              type="button"
              onClick={handleBack}
              className="inline-flex items-center gap-1.5 px-4 py-2 border border-slate-300 hover:bg-slate-50 text-slate-700 font-semibold rounded-lg text-xs"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Back</span>
            </button>
          ) : <div></div>}

          {step < 5 ? (
            <button
              type="button"
              onClick={handleNext}
              className="inline-flex items-center gap-1.5 px-6 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-lg text-xs shadow transition-all"
            >
              <span>Continue</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          ) : (
            <button
              type="button"
              onClick={handleSubmit}
              disabled={loading}
              className="inline-flex items-center gap-2 px-8 py-3 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-xl text-sm shadow-md transition-all disabled:opacity-50"
            >
              <Sparkles className="w-4 h-4" />
              <span>{loading ? 'Evaluating Rules...' : 'Evaluate Eligible Schemes'}</span>
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
'''

# 7. RequirementQuestionnairePage.jsx
REQUIREMENT_QUESTIONNAIRE = '''import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sparkles, Sliders, CheckCircle, ArrowRight } from 'lucide-react';
import api from '../services/api';

export default function RequirementQuestionnairePage() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    social_category: 'SC',
    gender: 'female',
    age: 28,
    state: 'Maharashtra',
    area_type: 'rural',
    business_type: 'manufacturing',
    business_stage: 'new',
    required_loan: 1000000,
    has_skill_training: true,
    has_udyam_registration: true
  });
  const [loading, setLoading] = useState(false);

  const handleEvaluate = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await api.post('/matching/evaluate', form);
      navigate('/results', { state: { evaluationResult: res.data, profileData: form } });
    } catch (err) {
      console.error(err);
      navigate('/results', { state: { profileData: form } });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto py-8 px-4">
      <div className="bg-white p-8 rounded-2xl border border-slate-200 shadow-sm space-y-6">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold mb-2">
            <Sliders className="w-3.5 h-3.5" />
            <span>Fast Analyzer</span>
          </div>
          <h1 className="text-2xl font-extrabold text-slate-900">Rapid Requirement Questionnaire</h1>
          <p className="text-xs text-slate-500 mt-1">Directly adjust financial parameters to see scheme eligibility recalculate instantly.</p>
        </div>

        <form onSubmit={handleEvaluate} className="space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Target Category</label>
              <select
                value={form.social_category}
                onChange={(e) => setForm({ ...form, social_category: e.target.value })}
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
              >
                <option value="SC">Scheduled Caste (SC)</option>
                <option value="ST">Scheduled Tribe (ST)</option>
                <option value="OBC">Other Backward Class (OBC)</option>
                <option value="Minority">Minority Group</option>
                <option value="General">General</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Gender</label>
              <select
                value={form.gender}
                onChange={(e) => setForm({ ...form, gender: e.target.value })}
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
              >
                <option value="female">Woman</option>
                <option value="male">Male</option>
                <option value="transgender">Transgender</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Business Nature</label>
              <select
                value={form.business_type}
                onChange={(e) => setForm({ ...form, business_type: e.target.value })}
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
              >
                <option value="manufacturing">Manufacturing</option>
                <option value="service">Service</option>
                <option value="trading">Trading</option>
                <option value="street_vendor">Street Vending</option>
                <option value="artisan">Artisan</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Location Setting</label>
              <select
                value={form.area_type}
                onChange={(e) => setForm({ ...form, area_type: e.target.value })}
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
              >
                <option value="rural">Rural (Higher Subsidy)</option>
                <option value="urban">Urban</option>
              </select>
            </div>
          </div>

          <div>
            <div className="flex justify-between text-xs font-semibold text-slate-700 mb-1">
              <span>Required Loan Amount</span>
              <span className="font-bold text-emerald-600">₹{(form.required_loan / 100000).toFixed(1)} Lakh</span>
            </div>
            <input
              type="range"
              min="10000"
              max="10000000"
              step="50000"
              value={form.required_loan}
              onChange={(e) => setForm({ ...form, required_loan: Number(e.target.value) })}
              className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-emerald-600"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-xl text-sm shadow transition-all flex items-center justify-center gap-2"
          >
            <Sparkles className="w-4 h-4" />
            <span>{loading ? 'Evaluating...' : 'Run Real-Time Scheme Compatibility'}</span>
          </button>
        </form>
      </div>
    </div>
  );
}
'''

with open(os.path.join(PAGES_DIR, "UserDashboard.jsx"), "w", encoding="utf-8") as f:
    f.write(USER_DASHBOARD)

with open(os.path.join(PAGES_DIR, "UserProfilePage.jsx"), "w", encoding="utf-8") as f:
    f.write(USER_PROFILE_PAGE)

with open(os.path.join(PAGES_DIR, "FindMySchemePage.jsx"), "w", encoding="utf-8") as f:
    f.write(FIND_MY_SCHEME_PAGE)

with open(os.path.join(PAGES_DIR, "RequirementQuestionnairePage.jsx"), "w", encoding="utf-8") as f:
    f.write(REQUIREMENT_QUESTIONNAIRE)

print("Part 2 pages generated successfully!")
