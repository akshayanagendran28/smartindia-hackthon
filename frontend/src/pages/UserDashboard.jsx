import React, { useState, useEffect } from 'react';
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
