import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  UserPlus, Mail, Lock, User, Phone, CheckCircle2, AlertCircle, 
  MapPin, DollarSign, ArrowRight, ShieldCheck, Check, Edit3, Sparkles,
  GraduationCap, Briefcase, Store
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { useApplication } from '../context/ApplicationContext';
import StepProgressIndicator from '../components/StepProgressIndicator';

export default function RegisterPage() {
  const { register } = useAuth();
  const { t } = useLanguage();
  const { 
    application, 
    updateApplication, 
    updateLoanAmount, 
    confirmAndSaveProfile 
  } = useApplication();
  const navigate = useNavigate();

  // Mode: 'entry' -> 'review'
  const [mode, setMode] = useState('entry');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Temporary draft state for registration input
  const [draft, setDraft] = useState({
    purpose_type: application.purpose_type || 'EDUCATION',
    full_name: application.full_name || '',
    email: '',
    phone: '',
    password: '',
    social_category: application.category || 'SC',
    gender: application.gender || 'female',
    state: application.state || 'Maharashtra',
    district: application.district || 'Mumbai',
    required_loan: application.loanAmount || 450000,
    preferred_language: 'en'
  });

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    if (name === 'purpose_type') {
      const defaultLoan = value === 'EDUCATION' ? 450000 : value === 'SELF_EMPLOYMENT' ? 50000 : 1200000;
      setDraft(prev => ({
        ...prev,
        purpose_type: value,
        required_loan: defaultLoan
      }));
      return;
    }
    setDraft(prev => ({
      ...prev,
      [name]: type === 'number' ? Number(value) : value
    }));
  };

  // Step 1: User moves from Entry to Review (Temporary Draft only)
  const handleProceedToReview = (e) => {
    e.preventDefault();
    setError('');
    if (!draft.full_name.trim()) {
      setError('Please enter your full name.');
      return;
    }
    if (!draft.email.trim() || !draft.email.includes('@')) {
      setError('Please provide a valid email address.');
      return;
    }
    if (!draft.password || draft.password.length < 6) {
      setError('Password must be at least 6 characters.');
      return;
    }

    // Save into temporary application context state (NOT yet permanent profile)
    updateApplication({
      purpose_type: draft.purpose_type,
      purposeType: draft.purpose_type,
      full_name: draft.full_name,
      category: draft.social_category,
      social_category: draft.social_category,
      gender: draft.gender,
      state: draft.state,
      district: draft.district,
      loanAmount: draft.required_loan,
      isProfileConfirmed: false,
    });
    updateLoanAmount(draft.required_loan);

    setMode('review');
  };

  // Step 2: Explicit Confirmation & Official Profile Persistence
  const handleConfirmAndContinue = async () => {
    setLoading(true);
    setError('');

    try {
      // 1. Create/Authenticate user account
      await register({
        email: draft.email,
        password: draft.password,
        full_name: draft.full_name,
        phone: draft.phone,
        role: 'entrepreneur',
        preferred_language: draft.preferred_language,
        state: draft.state,
        district: draft.district,
      });

      // 2. Permanently save confirmed profile & application state
      await confirmAndSaveProfile({
        purpose_type: draft.purpose_type,
        full_name: draft.full_name,
        category: draft.social_category,
        social_category: draft.social_category,
        gender: draft.gender,
        state: draft.state,
        district: draft.district,
        loanAmount: draft.required_loan,
        required_loan_amount: draft.required_loan,
        required_loan: draft.required_loan,
      });

      // 3. Move to Find My Scheme questionnaire
      navigate('/find-scheme');
    } catch (err) {
      console.error('Registration error:', err);
      // If user already exists, still proceed with confirmed profile
      try {
        await confirmAndSaveProfile({
          purpose_type: draft.purpose_type,
          full_name: draft.full_name,
          category: draft.social_category,
          social_category: draft.social_category,
          gender: draft.gender,
          state: draft.state,
          district: draft.district,
          loanAmount: draft.required_loan,
        });
        navigate('/find-scheme');
      } catch (confirmErr) {
        setError(err.response?.data?.detail || 'Registration failed. Please review inputs.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto py-8 px-4 sm:px-6 space-y-6">
      <StepProgressIndicator currentStep={1} />

      <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-xl space-y-6">
        {/* Header */}
        <div className="text-center">
          <div className="inline-flex p-3 rounded-2xl bg-emerald-100 text-emerald-800 mb-3 shadow-inner">
            <UserPlus className="w-8 h-8" />
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-slate-900">
            {mode === 'entry' ? 'Beneficiary Registration & Intake' : 'Review & Confirm Profile Details'}
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1 max-w-md mx-auto">
            {mode === 'entry'
              ? 'Input is held as a temporary session draft. You will review all details before official submission.'
              : 'Please review your information carefully. Your profile will be officially activated only after confirmation.'}
          </p>
        </div>

        {error && (
          <div className="p-3.5 rounded-xl bg-red-50 border border-red-200 text-red-700 text-xs flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {/* MODE 1: Data Entry Form (Temporary Draft State) */}
        {mode === 'entry' ? (
          <form onSubmit={handleProceedToReview} className="space-y-4">
            {/* Purpose / Track Selection */}
            <div>
              <label className="block text-xs font-bold text-slate-800 uppercase tracking-wider mb-2">
                Primary Goal / Scheme Category
              </label>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
                {[
                  {
                    id: 'EDUCATION',
                    label: 'Higher Education',
                    sub: 'CSIS, NSFDC & Higher Studies',
                    icon: <GraduationCap className="w-4 h-4" />
                  },
                  {
                    id: 'BUSINESS',
                    label: 'Business Enterprise',
                    sub: 'PMEGP, Stand-Up & MSME',
                    icon: <Briefcase className="w-4 h-4" />
                  },
                  {
                    id: 'SELF_EMPLOYMENT',
                    label: 'Self-Employment',
                    sub: 'PM SVANidhi, Mudra & Livelihood',
                    icon: <Store className="w-4 h-4" />
                  }
                ].map(item => {
                  const active = draft.purpose_type === item.id;
                  return (
                    <button
                      type="button"
                      key={item.id}
                      onClick={() => {
                        const defaultLoan = item.id === 'EDUCATION' ? 450000 : item.id === 'SELF_EMPLOYMENT' ? 50000 : 1200000;
                        setDraft(prev => ({
                          ...prev,
                          purpose_type: item.id,
                          required_loan: defaultLoan
                        }));
                      }}
                      className={`p-3 rounded-xl border text-left transition-all ${
                        active
                          ? 'border-emerald-600 bg-emerald-50 text-emerald-950 ring-2 ring-emerald-500/20 shadow-sm'
                          : 'border-slate-200 bg-slate-50 hover:bg-slate-100 text-slate-700'
                      }`}
                    >
                      <div className="flex items-center gap-2 font-bold text-xs">
                        <span className={active ? 'text-emerald-700' : 'text-slate-500'}>{item.icon}</span>
                        <span>{item.label}</span>
                      </div>
                      <p className="text-[10px] text-slate-500 mt-1">{item.sub}</p>
                    </button>
                  );
                })}
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Full Name</label>
                <div className="relative">
                  <User className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
                  <input
                    type="text"
                    required
                    name="full_name"
                    value={draft.full_name}
                    onChange={handleChange}
                    placeholder="e.g. Priya Sharma"
                    className="w-full pl-9 pr-3 py-2.5 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Email Address</label>
                <div className="relative">
                  <Mail className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
                  <input
                    type="email"
                    required
                    name="email"
                    value={draft.email}
                    onChange={handleChange}
                    placeholder="priya@example.com"
                    className="w-full pl-9 pr-3 py-2.5 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                  />
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Phone Number</label>
                <div className="relative">
                  <Phone className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
                  <input
                    type="tel"
                    name="phone"
                    value={draft.phone}
                    onChange={handleChange}
                    placeholder="9876543210"
                    className="w-full pl-9 pr-3 py-2.5 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Password</label>
                <div className="relative">
                  <Lock className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
                  <input
                    type="password"
                    required
                    minLength={6}
                    name="password"
                    value={draft.password}
                    onChange={handleChange}
                    placeholder="At least 6 characters"
                    className="w-full pl-9 pr-3 py-2.5 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                  />
                </div>
              </div>
            </div>

            {/* Target Marginalized Categories Only */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-1">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Target Beneficiary Category
                </label>
                <select
                  name="social_category"
                  value={draft.social_category}
                  onChange={handleChange}
                  className="w-full px-3 py-2.5 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:outline-none bg-slate-50 font-medium"
                >
                  <option value="SC">Scheduled Caste (SC)</option>
                  <option value="ST">Scheduled Tribe (ST)</option>
                  <option value="Minority">Minority (Muslim/Christian/Sikh/Buddhist/Jain/Parsi)</option>
                  <option value="Woman">Women / Special Category</option>
                  <option value="Divyangjan">Specially Abled / Divyangjan</option>
                </select>
                <p className="text-[10px] text-slate-400 mt-1">General and OBC are excluded as per mandated target focus.</p>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Gender</label>
                <select
                  name="gender"
                  value={draft.gender}
                  onChange={handleChange}
                  className="w-full px-3 py-2.5 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:outline-none bg-slate-50"
                >
                  <option value="female">Female / Woman</option>
                  <option value="male">Male</option>
                  <option value="transgender">Transgender</option>
                </select>
              </div>
            </div>

            {/* Single Source of Truth Loan Amount */}
            <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200 space-y-2">
              <div className="flex justify-between items-center text-xs font-bold text-slate-700">
                <span>Initial Required Loan Amount</span>
                <span className="text-emerald-700 font-extrabold text-base font-mono">
                  ₹{Number(draft.required_loan).toLocaleString('en-IN')}
                </span>
              </div>
              <input
                type="number"
                name="required_loan"
                min="10000"
                max="50000000"
                step="25000"
                value={draft.required_loan}
                onChange={handleChange}
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              />
              <p className="text-[10px] text-slate-400">
                This single loan amount will automatically sync across Find My Scheme, Document Verification, and the EMI Calculator.
              </p>
            </div>

            <div className="pt-2">
              <button
                type="submit"
                className="w-full py-3.5 px-4 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-xl shadow-lg transition-all flex items-center justify-center gap-2 text-sm hover:scale-[1.01]"
              >
                <span>Review Temporary Application Data</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </form>
        ) : (
          /* MODE 2: Comprehensive Review Mode before Official Confirmation */
          <div className="space-y-5 animate-fadeIn">
            <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-2xl flex items-center gap-3 text-xs text-emerald-900">
              <ShieldCheck className="w-5 h-5 text-emerald-600 shrink-0" />
              <span>
                Please verify your entered information below. Clicking <strong>"Confirm & Continue"</strong> will officially save your profile and initiate the dynamic scheme workflow.
              </span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
              <div className="p-3.5 bg-emerald-50 rounded-xl border border-emerald-200 sm:col-span-2 flex items-center justify-between">
                <div>
                  <span className="text-emerald-800 text-[10px] font-bold uppercase block">Selected Workflow Track</span>
                  <span className="font-extrabold text-emerald-950 text-sm">
                    {draft.purpose_type === 'EDUCATION' ? '🎓 Higher Education' : draft.purpose_type === 'SELF_EMPLOYMENT' ? '🏪 Self-Employment & Micro-Enterprise' : '🏢 Business & MSME Enterprise'}
                  </span>
                </div>
                <span className="px-2.5 py-1 bg-emerald-600 text-white font-bold rounded-lg text-[10px]">
                  {draft.purpose_type}
                </span>
              </div>

              <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200">
                <span className="text-slate-400 text-[10px] font-bold uppercase block">Full Name</span>
                <span className="font-bold text-slate-800 text-sm">{draft.full_name}</span>
              </div>

              <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200">
                <span className="text-slate-400 text-[10px] font-bold uppercase block">Email Address</span>
                <span className="font-bold text-slate-800 text-sm font-mono">{draft.email}</span>
              </div>

              <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200">
                <span className="text-slate-400 text-[10px] font-bold uppercase block">Target Category</span>
                <span className="font-bold text-emerald-800 text-sm">{draft.social_category}</span>
              </div>

              <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200">
                <span className="text-slate-400 text-[10px] font-bold uppercase block">Gender</span>
                <span className="font-bold text-slate-800 text-sm capitalize">{draft.gender}</span>
              </div>

              <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 sm:col-span-2">
                <span className="text-slate-400 text-[10px] font-bold uppercase block">Single Loan Amount (Source of Truth)</span>
                <span className="font-black text-emerald-700 text-base font-mono">
                  ₹{Number(draft.required_loan).toLocaleString('en-IN')}
                </span>
              </div>
            </div>

            <div className="flex flex-col sm:flex-row items-center gap-3 pt-3 border-t border-slate-100">
              <button
                type="button"
                onClick={() => setMode('entry')}
                className="w-full sm:w-auto px-5 py-3 border border-slate-300 text-slate-700 hover:bg-slate-50 font-bold text-xs rounded-xl flex items-center justify-center gap-2"
              >
                <Edit3 className="w-4 h-4 text-slate-500" />
                <span>Edit Information</span>
              </button>

              <button
                type="button"
                onClick={handleConfirmAndContinue}
                disabled={loading}
                className="w-full sm:flex-1 py-3.5 px-6 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-black text-sm rounded-xl shadow-lg transition-all flex items-center justify-center gap-2 disabled:opacity-50"
              >
                {loading ? (
                  <span>Saving & Initiating Workflow...</span>
                ) : (
                  <>
                    <Check className="w-4 h-4 text-emerald-300" />
                    <span>Confirm & Continue</span>
                    <ArrowRight className="w-4 h-4 ml-1" />
                  </>
                )}
              </button>
            </div>
          </div>
        )}

        <div className="text-center pt-2">
          <p className="text-xs text-slate-600">
            Already have an active profile?{' '}
            <Link to="/login" className="font-bold text-emerald-700 hover:underline">
              Log in directly
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
