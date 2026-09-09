import os

BASE_DIR = r"C:\Users\aksha\.gemini\antigravity\scratch\scheme-sathi\frontend\src"
PAGES_DIR = os.path.join(BASE_DIR, "pages")
ADMIN_DIR = os.path.join(PAGES_DIR, "admin")
os.makedirs(PAGES_DIR, exist_ok=True)
os.makedirs(ADMIN_DIR, exist_ok=True)

# 1. LandingPage.jsx
LANDING_PAGE = '''import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  Sparkles, Award, ShieldCheck, TrendingUp, CheckCircle, ArrowRight,
  Calculator, MapPin, FileCheck, MessageSquare, Users, Building2,
  ChevronRight, Compass, DollarSign, Target, Star, HelpCircle
} from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';

export default function LandingPage() {
  const { t, language } = useLanguage();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [featuredSchemes, setFeaturedSchemes] = useState([]);
  const [stats, setStats] = useState({ total_schemes: 9, total_partners: 13, max_subsidy: "35%", active_beneficiaries: "12,450+" });
  const [quickForm, setQuickForm] = useState({
    social_category: 'SC',
    gender: 'female',
    required_loan: 500000,
    business_type: 'manufacturing'
  });

  useEffect(() => {
    // Fetch real schemes from backend
    api.get('/schemes')
      .then(res => {
        if (res.data && res.data.length > 0) {
          setFeaturedSchemes(res.data.slice(0, 6));
        }
      })
      .catch(err => console.log('Could not load schemes', err));
  }, []);

  const handleQuickCheck = (e) => {
    e.preventDefault();
    navigate('/find-scheme', { state: { initialForm: quickForm } });
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans">
      {/* SIH 2026 Header Banner */}
      <div className="bg-gradient-to-r from-orange-600 via-amber-600 to-emerald-700 text-white py-2 px-4 text-center text-xs md:text-sm font-medium tracking-wide shadow-sm flex items-center justify-center gap-2">
        <span className="bg-white/20 px-2 py-0.5 rounded text-[11px] font-bold uppercase tracking-wider">SIH 2026</span>
        <span>Problem Statement ID: SIH26092 &bull; AI-Driven Scheme Matching for Marginalized Entrepreneurs</span>
      </div>

      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-b from-emerald-950 via-slate-900 to-slate-950 text-white pt-16 pb-24 px-4 sm:px-6 lg:px-8">
        <div className="absolute inset-0 opacity-10 bg-[radial-gradient(#10b981_1px,transparent_1px)] [background-size:16px_16px]"></div>
        
        <div className="max-w-7xl mx-auto relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          <div className="lg:col-span-7 space-y-6 text-center lg:text-left">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-sm font-medium">
              <Sparkles className="w-4 h-4" />
              <span>100% Deterministic Rule Engine + SHAP-Style AI Ranking</span>
            </div>
            
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight leading-tight">
              Empowering Every <br />
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-emerald-400 via-teal-300 to-amber-300">
                Marginalized Entrepreneur
              </span> <br />
              with Govt Schemes
            </h1>
            
            <p className="text-lg sm:text-xl text-slate-300 max-w-2xl leading-relaxed">
              Find, evaluate, and apply for verified Central & State financial assistance schemes with guaranteed eligibility explanations, OCR document checking, and local bank partner routing.
            </p>

            {/* Quick CTAs */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start pt-2">
              <Link
                to="/find-scheme"
                className="inline-flex items-center justify-center gap-2 px-8 py-4 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-lg shadow-lg shadow-emerald-500/25 transition-all transform hover:-translate-y-0.5"
              >
                <Compass className="w-5 h-5" />
                <span>{t('find_my_scheme')}</span>
                <ArrowRight className="w-5 h-5" />
              </Link>
              <Link
                to="/chat"
                className="inline-flex items-center justify-center gap-2 px-6 py-4 rounded-xl bg-slate-800 hover:bg-slate-700 border border-slate-700 text-white font-semibold text-base transition-all"
              >
                <MessageSquare className="w-5 h-5 text-emerald-400" />
                <span>{t('chat_assistant')}</span>
              </Link>
            </div>

            {/* Target Marginalized Cohorts */}
            <div className="pt-6 border-t border-slate-800/80">
              <p className="text-xs uppercase tracking-wider text-slate-400 font-semibold mb-3">Tailored For Vulnerable Groups:</p>
              <div className="flex flex-wrap gap-2 justify-center lg:justify-start">
                {['SC / ST Founders', 'Women Entrepreneurs', 'Minority Communities', 'Street Vendors', 'Traditional Artisans', 'Differently Abled'].map((group, idx) => (
                  <span key={idx} className="px-3 py-1 rounded-full text-xs font-medium bg-slate-800/80 border border-slate-700 text-slate-300">
                    {group}
                  </span>
                ))}
              </div>
            </div>
          </div>

          {/* Quick Eligibility Evaluator Card */}
          <div className="lg:col-span-5">
            <div className="bg-white/10 backdrop-blur-md border border-white/15 rounded-2xl p-6 sm:p-8 shadow-2xl text-slate-100">
              <div className="flex items-center justify-between mb-5">
                <div className="flex items-center gap-2">
                  <div className="p-2 bg-emerald-500/20 text-emerald-400 rounded-lg">
                    <Target className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="font-bold text-white text-lg">Instant Eligibility Check</h3>
                    <p className="text-xs text-slate-300">Discover your best match in 30 seconds</p>
                  </div>
                </div>
                <span className="text-xs font-semibold px-2.5 py-1 bg-emerald-500/20 text-emerald-300 rounded-full border border-emerald-500/30">Live AI</span>
              </div>

              <form onSubmit={handleQuickCheck} className="space-y-4">
                <div>
                  <label className="block text-xs font-medium text-slate-200 mb-1">Your Social Category</label>
                  <select
                    value={quickForm.social_category}
                    onChange={(e) => setQuickForm({ ...quickForm, social_category: e.target.value })}
                    className="w-full bg-slate-900/90 border border-slate-700 rounded-lg px-3 py-2.5 text-sm text-white focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                  >
                    <option value="SC">Scheduled Caste (SC)</option>
                    <option value="ST">Scheduled Tribe (ST)</option>
                    <option value="OBC">Other Backward Class (OBC)</option>
                    <option value="Minority">Minority Community</option>
                    <option value="General">General Category</option>
                  </select>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-medium text-slate-200 mb-1">Gender</label>
                    <select
                      value={quickForm.gender}
                      onChange={(e) => setQuickForm({ ...quickForm, gender: e.target.value })}
                      className="w-full bg-slate-900/90 border border-slate-700 rounded-lg px-3 py-2.5 text-sm text-white focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                    >
                      <option value="female">Woman / Female</option>
                      <option value="male">Male</option>
                      <option value="transgender">Transgender</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-xs font-medium text-slate-200 mb-1">Business Type</label>
                    <select
                      value={quickForm.business_type}
                      onChange={(e) => setQuickForm({ ...quickForm, business_type: e.target.value })}
                      className="w-full bg-slate-900/90 border border-slate-700 rounded-lg px-3 py-2.5 text-sm text-white focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                    >
                      <option value="manufacturing">Manufacturing</option>
                      <option value="service">Service Unit</option>
                      <option value="trading">Trading / Retail</option>
                      <option value="street_vendor">Street Vending</option>
                      <option value="artisan">Artisan / Handicraft</option>
                    </select>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-xs font-medium text-slate-200 mb-1">
                    <span>Required Loan Amount</span>
                    <span className="text-emerald-400 font-bold">₹{(quickForm.required_loan / 100000).toFixed(1)} Lakh</span>
                  </div>
                  <input
                    type="range"
                    min="10000"
                    max="10000000"
                    step="10000"
                    value={quickForm.required_loan}
                    onChange={(e) => setQuickForm({ ...quickForm, required_loan: Number(e.target.value) })}
                    className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-emerald-500"
                  />
                  <div className="flex justify-between text-[10px] text-slate-400 mt-1">
                    <span>₹10,000 (SVANidhi)</span>
                    <span>₹50 Lakh (PMEGP)</span>
                    <span>₹10 Cr (StandUp)</span>
                  </div>
                </div>

                <button
                  type="submit"
                  className="w-full py-3 px-4 bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 text-slate-950 font-bold rounded-lg shadow-md transition-all flex items-center justify-center gap-2 text-sm mt-2"
                >
                  <Sparkles className="w-4 h-4" />
                  <span>Analyze Matching Schemes</span>
                </button>
              </form>
            </div>
          </div>
        </div>
      </section>

      {/* Trust & Impact Stats */}
      <section className="bg-white border-y border-slate-200 py-8 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
            <div className="p-4 rounded-xl bg-slate-50 border border-slate-100">
              <div className="text-3xl font-extrabold text-emerald-700">9+</div>
              <div className="text-xs sm:text-sm font-medium text-slate-600 mt-1">Verified Govt Schemes</div>
            </div>
            <div className="p-4 rounded-xl bg-slate-50 border border-slate-100">
              <div className="text-3xl font-extrabold text-teal-700">Up to 35%</div>
              <div className="text-xs sm:text-sm font-medium text-slate-600 mt-1">Capital Subsidy (PMEGP)</div>
            </div>
            <div className="p-4 rounded-xl bg-slate-50 border border-slate-100">
              <div className="text-3xl font-extrabold text-amber-600">6</div>
              <div className="text-xs sm:text-sm font-medium text-slate-600 mt-1">Indian Regional Languages</div>
            </div>
            <div className="p-4 rounded-xl bg-slate-50 border border-slate-100">
              <div className="text-3xl font-extrabold text-blue-700">100%</div>
              <div className="text-xs sm:text-sm font-medium text-slate-600 mt-1">Deterministic Rule Integrity</div>
            </div>
          </div>
        </div>
      </section>

      {/* 4-Step Solution Architecture */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="text-center max-w-3xl mx-auto mb-14">
          <h2 className="text-xs uppercase tracking-widest font-bold text-emerald-700 mb-2">Architectural Workflow</h2>
          <p className="text-3xl font-extrabold text-slate-900">How Scheme Sathi Works</p>
          <p className="text-slate-600 mt-3">From raw applicant profile to sanctioned government subsidy in 4 transparent stages.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {[
            {
              step: "01",
              title: "Profile & Need Analysis",
              desc: "Captures demographics (SC/ST/Woman/Minority), project cost, location, and trade.",
              icon: <Users className="w-6 h-6 text-emerald-600" />,
              color: "bg-emerald-50 border-emerald-200"
            },
            {
              step: "02",
              title: "Deterministic Rule Engine",
              desc: "Evaluates exact legal gazette rules (age, ceiling, margin) without LLM hallucinations.",
              icon: <ShieldCheck className="w-6 h-6 text-blue-600" />,
              color: "bg-blue-50 border-blue-200"
            },
            {
              step: "03",
              title: "SHAP-Style Ranking",
              desc: "Calculates multi-factor compatibility scores and provides crystal-clear explainability.",
              icon: <TrendingUp className="w-6 h-6 text-amber-600" />,
              color: "bg-amber-50 border-amber-200"
            },
            {
              step: "04",
              title: "OCR & Partner Routing",
              desc: "Verifies Aadhaar/Caste certificates & routes to nearest authorized Bank or CSC center.",
              icon: <MapPin className="w-6 h-6 text-purple-600" />,
              color: "bg-purple-50 border-purple-200"
            }
          ].map((item, idx) => (
            <div key={idx} className={`p-6 rounded-2xl border ${item.color} shadow-sm relative group hover:shadow-md transition-all`}>
              <div className="text-4xl font-black text-slate-200 absolute top-4 right-4">{item.step}</div>
              <div className="w-12 h-12 rounded-xl bg-white shadow-sm flex items-center justify-center mb-4">
                {item.icon}
              </div>
              <h3 className="font-bold text-slate-900 text-lg mb-2">{item.title}</h3>
              <p className="text-slate-600 text-sm leading-relaxed">{item.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Featured Verified Government Schemes */}
      <section className="py-16 bg-slate-100 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="flex flex-col md:flex-row md:items-end justify-between mb-10">
            <div>
              <span className="text-xs uppercase tracking-wider font-bold text-emerald-700">Verified Database</span>
              <h2 className="text-3xl font-extrabold text-slate-900 mt-1">Featured Government Schemes</h2>
              <p className="text-slate-600 text-sm mt-1">Official Central & State assistance programs with verified rules and subsidy rates.</p>
            </div>
            <Link to="/results" className="mt-4 md:mt-0 inline-flex items-center gap-1.5 text-sm font-bold text-emerald-700 hover:text-emerald-800">
              <span>View All 9+ Schemes</span>
              <ChevronRight className="w-4 h-4" />
            </Link>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {featuredSchemes.length > 0 ? (
              featuredSchemes.map((scheme) => (
                <div key={scheme.id} className="bg-white rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition-all p-6 flex flex-col justify-between">
                  <div>
                    <div className="flex items-center justify-between mb-3">
                      <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 uppercase tracking-wide">
                        {scheme.target_category || 'Marginalized'}
                      </span>
                      <span className="text-xs font-semibold text-slate-500">{scheme.code}</span>
                    </div>
                    <h3 className="font-bold text-slate-900 text-lg line-clamp-1">{scheme.name}</h3>
                    <p className="text-xs text-slate-500 font-medium mt-0.5">{scheme.ministry}</p>
                    <p className="text-slate-600 text-xs mt-3 line-clamp-2 leading-relaxed">{scheme.description}</p>
                  </div>

                  <div className="mt-6 pt-4 border-t border-slate-100 space-y-2 text-xs">
                    <div className="flex justify-between">
                      <span className="text-slate-500">Max Loan Amount:</span>
                      <span className="font-bold text-slate-900">₹{(scheme.max_loan_amount / 100000).toLocaleString('en-IN')} Lakh</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-500">Capital Subsidy:</span>
                      <span className="font-bold text-emerald-700">
                        {scheme.subsidy_details?.special_rural || scheme.subsidy_details?.special || scheme.subsidy_details?.general_rural || 'Low Interest'}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-500">Repayment Period:</span>
                      <span className="font-medium text-slate-700">{scheme.repayment_period_months} Months</span>
                    </div>

                    <div className="pt-3 flex gap-2">
                      <Link
                        to={`/scheme/${scheme.id}`}
                        className="flex-1 py-2 text-center rounded-lg bg-emerald-50 hover:bg-emerald-100 text-emerald-800 font-bold text-xs transition-colors"
                      >
                        Details & Rules
                      </Link>
                      <Link
                        to="/find-scheme"
                        className="py-2 px-3 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs transition-colors flex items-center justify-center"
                        title="Check Eligibility"
                      >
                        <CheckCircle className="w-4 h-4" />
                      </Link>
                    </div>
                  </div>
                </div>
              ))
            ) : (
              [
                { name: 'PMEGP (Prime Minister Employment Generation Programme)', code: 'PMEGP', ministry: 'Ministry of MSME', max: '₹50 Lakh', sub: 'Up to 35%' },
                { name: 'Stand-Up India Scheme', code: 'STANDUP-IND', ministry: 'Ministry of Finance', max: '₹1 Crore', sub: 'Bank Guarantee' },
                { name: 'PM SVANidhi (Street Vendors)', code: 'SVANIDHI', ministry: 'Ministry of Housing & Urban Affairs', max: '₹50,000', sub: '7% Interest Subsidy' }
              ].map((s, idx) => (
                <div key={idx} className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
                  <div className="text-xs font-bold text-emerald-800 bg-emerald-100 px-2.5 py-1 rounded-full inline-block mb-3">{s.code}</div>
                  <h3 className="font-bold text-slate-900 text-lg">{s.name}</h3>
                  <p className="text-xs text-slate-500">{s.ministry}</p>
                  <div className="mt-4 pt-4 border-t border-slate-100 text-xs space-y-2">
                    <div className="flex justify-between"><span>Max Loan:</span><span className="font-bold">{s.max}</span></div>
                    <div className="flex justify-between"><span>Subsidy:</span><span className="font-bold text-emerald-700">{s.sub}</span></div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </section>

      {/* Feature Pillars */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="p-6 rounded-2xl bg-white border border-slate-200 shadow-sm">
            <div className="p-3 bg-emerald-100 text-emerald-800 rounded-xl w-fit mb-4">
              <FileCheck className="w-6 h-6" />
            </div>
            <h3 className="font-bold text-slate-900 text-base mb-1">OCR Document Assistant</h3>
            <p className="text-slate-600 text-xs leading-relaxed">
              Upload Aadhaar, Caste Certificate & Income Proof with instant mismatch detection against profile.
            </p>
            <Link to="/documents" className="mt-4 inline-flex items-center gap-1 text-xs font-bold text-emerald-700 hover:text-emerald-800">
              <span>Scan Documents</span>
              <ChevronRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="p-6 rounded-2xl bg-white border border-slate-200 shadow-sm">
            <div className="p-3 bg-teal-100 text-teal-800 rounded-xl w-fit mb-4">
              <MapPin className="w-6 h-6" />
            </div>
            <h3 className="font-bold text-slate-900 text-base mb-1">Partner Bank Locator</h3>
            <p className="text-slate-600 text-xs leading-relaxed">
              OpenStreetMap powered dual-factor locator ranking banks by geographic distance & scheme compatibility.
            </p>
            <Link to="/partners" className="mt-4 inline-flex items-center gap-1 text-xs font-bold text-teal-700 hover:text-teal-800">
              <span>Find Nearest Bank</span>
              <ChevronRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="p-6 rounded-2xl bg-white border border-slate-200 shadow-sm">
            <div className="p-3 bg-amber-100 text-amber-800 rounded-xl w-fit mb-4">
              <Calculator className="w-6 h-6" />
            </div>
            <h3 className="font-bold text-slate-900 text-base mb-1">EMI & Subsidy Simulator</h3>
            <p className="text-slate-600 text-xs leading-relaxed">
              Interactive financial calculator modeling moratoriums, margin contributions, and net interest savings.
            </p>
            <Link to="/calculator" className="mt-4 inline-flex items-center gap-1 text-xs font-bold text-amber-700 hover:text-amber-800">
              <span>Calculate Loan EMI</span>
              <ChevronRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="p-6 rounded-2xl bg-white border border-slate-200 shadow-sm">
            <div className="p-3 bg-indigo-100 text-indigo-800 rounded-xl w-fit mb-4">
              <MessageSquare className="w-6 h-6" />
            </div>
            <h3 className="font-bold text-slate-900 text-base mb-1">6-Language AI Assistant</h3>
            <p className="text-slate-600 text-xs leading-relaxed">
              Ask scheme questions in English, Hindi, Tamil, Telugu, Kannada, or Malayalam with zero hallucinations.
            </p>
            <Link to="/chat" className="mt-4 inline-flex items-center gap-1 text-xs font-bold text-indigo-700 hover:text-indigo-800">
              <span>Chat with Sathi</span>
              <ChevronRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>
      </section>

      {/* Call to Action Bar */}
      <section className="bg-gradient-to-r from-emerald-800 to-teal-900 text-white py-12 px-4 sm:px-6 lg:px-8 text-center">
        <div className="max-w-4xl mx-auto space-y-4">
          <h2 className="text-2xl sm:text-3xl font-extrabold">Ready to Discover Your Eligible Govt Scheme?</h2>
          <p className="text-slate-200 text-sm max-w-xl mx-auto">
            Join thousands of marginalized entrepreneurs taking their dreams forward with subsidized capital and zero-hassle paperwork.
          </p>
          <div className="pt-2">
            <Link
              to="/find-scheme"
              className="inline-flex items-center gap-2 px-8 py-3.5 rounded-xl bg-white text-emerald-950 font-bold text-base hover:bg-slate-100 shadow-lg transition-all"
            >
              <Sparkles className="w-5 h-5 text-emerald-600" />
              <span>Start Free Scheme Assessment</span>
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
'''

# 2. LoginPage.jsx
LOGIN_PAGE = '''import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { Lock, Mail, ShieldCheck, ArrowRight, UserCheck, AlertCircle } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';

export default function LoginPage() {
  const { login } = useAuth();
  const { t } = useLanguage();
  const navigate = useNavigate();
  const location = useLocation();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const from = location.state?.from?.pathname || '/dashboard';

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const res = await login(email, password);
      if (res.user?.role === 'admin') {
        navigate('/admin');
      } else {
        navigate(from, { replace: true });
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Invalid email or password. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const fillDemo = (role) => {
    if (role === 'entrepreneur') {
      setEmail('priya@example.com');
      setPassword('password123');
    } else if (role === 'vendor') {
      setEmail('rahul@example.com');
      setPassword('password123');
    } else if (role === 'admin') {
      setEmail('admin@schemesathi.gov.in');
      setPassword('admin123');
    }
  };

  return (
    <div className="min-h-[85vh] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 bg-slate-50">
      <div className="max-w-md w-full space-y-8 bg-white p-8 rounded-2xl shadow-xl border border-slate-200">
        <div className="text-center">
          <div className="inline-flex p-3 rounded-2xl bg-emerald-100 text-emerald-800 mb-3">
            <ShieldCheck className="w-8 h-8" />
          </div>
          <h2 className="text-2xl font-extrabold text-slate-900">{t('login')} to Scheme Sathi</h2>
          <p className="text-xs text-slate-500 mt-1">Access your personalized eligibility profile & applications</p>
        </div>

        {error && (
          <div className="p-3.5 rounded-xl bg-red-50 border border-red-200 text-red-700 text-xs flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {/* Demo Fast-Fill Bar */}
        <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 text-xs">
          <span className="font-semibold text-slate-700 block mb-1.5">Quick Demo Login:</span>
          <div className="flex gap-2">
            <button
              type="button"
              onClick={() => fillDemo('entrepreneur')}
              className="flex-1 py-1 px-2 bg-white border border-slate-300 rounded text-[11px] font-medium text-slate-700 hover:bg-emerald-50 hover:border-emerald-300"
            >
              Woman Founder
            </button>
            <button
              type="button"
              onClick={() => fillDemo('vendor')}
              className="flex-1 py-1 px-2 bg-white border border-slate-300 rounded text-[11px] font-medium text-slate-700 hover:bg-emerald-50 hover:border-emerald-300"
            >
              Street Vendor
            </button>
            <button
              type="button"
              onClick={() => fillDemo('admin')}
              className="flex-1 py-1 px-2 bg-white border border-slate-300 rounded text-[11px] font-medium text-slate-700 hover:bg-emerald-50 hover:border-emerald-300"
            >
              Admin Portal
            </button>
          </div>
        </div>

        <form className="mt-6 space-y-4" onSubmit={handleSubmit}>
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Email Address</label>
            <div className="relative">
              <Mail className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="name@example.com"
                className="w-full pl-9 pr-3 py-2.5 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
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
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full pl-9 pr-3 py-2.5 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 px-4 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-lg shadow-md transition-all flex items-center justify-center gap-2 text-sm disabled:opacity-50"
          >
            {loading ? <span>Authenticating...</span> : (
              <>
                <span>Sign In</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </form>

        <div className="text-center pt-2">
          <p className="text-xs text-slate-600">
            Don't have an account?{' '}
            <Link to="/register" className="font-bold text-emerald-700 hover:underline">
              Create Entrepreneur Profile
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
'''

# 3. RegisterPage.jsx
REGISTER_PAGE = '''import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { UserPlus, Mail, Lock, User, Phone, CheckCircle, AlertCircle } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';

export default function RegisterPage() {
  const { register } = useAuth();
  const { t } = useLanguage();
  const navigate = useNavigate();

  const [form, setForm] = useState({
    email: '',
    password: '',
    full_name: '',
    phone: '',
    role: 'entrepreneur',
    preferred_language: 'en'
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await register(form);
      navigate('/find-scheme');
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed. Email may already be in use.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[85vh] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 bg-slate-50">
      <div className="max-w-md w-full space-y-6 bg-white p-8 rounded-2xl shadow-xl border border-slate-200">
        <div className="text-center">
          <div className="inline-flex p-3 rounded-2xl bg-emerald-100 text-emerald-800 mb-3">
            <UserPlus className="w-8 h-8" />
          </div>
          <h2 className="text-2xl font-extrabold text-slate-900">{t('register')} on Scheme Sathi</h2>
          <p className="text-xs text-slate-500 mt-1">Unlock AI scheme matching for your venture</p>
        </div>

        {error && (
          <div className="p-3.5 rounded-xl bg-red-50 border border-red-200 text-red-700 text-xs flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <form className="space-y-4" onSubmit={handleSubmit}>
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Full Name</label>
            <div className="relative">
              <User className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              <input
                type="text"
                required
                value={form.full_name}
                onChange={(e) => setForm({ ...form, full_name: e.target.value })}
                placeholder="e.g. Priya Sharma"
                className="w-full pl-9 pr-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
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
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
                placeholder="priya@example.com"
                className="w-full pl-9 pr-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Phone Number</label>
              <div className="relative">
                <Phone className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
                <input
                  type="tel"
                  value={form.phone}
                  onChange={(e) => setForm({ ...form, phone: e.target.value })}
                  placeholder="9876543210"
                  className="w-full pl-9 pr-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Preferred Language</label>
              <select
                value={form.preferred_language}
                onChange={(e) => setForm({ ...form, preferred_language: e.target.value })}
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              >
                <option value="en">English</option>
                <option value="hi">हिंदी (Hindi)</option>
                <option value="ta">தமிழ் (Tamil)</option>
                <option value="te">తెలుగు (Telugu)</option>
                <option value="kn">ಕನ್ನಡ (Kannada)</option>
                <option value="ml">മലയാളം (Malayalam)</option>
              </select>
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
                value={form.password}
                onChange={(e) => setForm({ ...form, password: e.target.value })}
                placeholder="At least 6 characters"
                className="w-full pl-9 pr-3 py-2 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 px-4 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-lg shadow-md transition-all flex items-center justify-center gap-2 text-sm disabled:opacity-50"
          >
            {loading ? 'Creating Account...' : 'Register & Start Scheme Finder'}
          </button>
        </form>

        <div className="text-center pt-2">
          <p className="text-xs text-slate-600">
            Already have an account?{' '}
            <Link to="/login" className="font-bold text-emerald-700 hover:underline">
              Log in here
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
'''

with open(os.path.join(PAGES_DIR, "LandingPage.jsx"), "w", encoding="utf-8") as f:
    f.write(LANDING_PAGE)

with open(os.path.join(PAGES_DIR, "LoginPage.jsx"), "w", encoding="utf-8") as f:
    f.write(LOGIN_PAGE)

with open(os.path.join(PAGES_DIR, "RegisterPage.jsx"), "w", encoding="utf-8") as f:
    f.write(REGISTER_PAGE)

print("Generated LandingPage, LoginPage, RegisterPage successfully.")
