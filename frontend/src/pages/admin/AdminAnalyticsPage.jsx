import React, { useState, useEffect } from 'react';
import { 
  BarChart3, TrendingUp, Users, PieChart as PieIcon, 
  Award, ShieldCheck, RefreshCw, CheckCircle2, DollarSign,
  Activity, Landmark, Layers
} from 'lucide-react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, PieChart, Pie, Cell } from 'recharts';
import api from '../../services/api';

export default function AdminAnalyticsPage() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  const loadAnalytics = async () => {
    try {
      setLoading(true);
      const res = await api.get('/admin/dashboard');
      setStats(res.data);
    } catch (err) {
      console.error('Failed to load analytics data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAnalytics();
  }, []);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-4 font-sans">
        <RefreshCw className="w-8 h-8 text-emerald-600 animate-spin" />
        <p className="text-sm font-bold text-slate-600">Loading live national inclusion analytics...</p>
      </div>
    );
  }

  const s = stats || {
    total_customers: 0,
    active_schemes: 0,
    total_applications: 0,
    loans_approved: 0,
    funds_released: 0,
    subsidy_disbursed_text: 'Data not available',
    users_by_state: [],
    demographics_distribution: [],
    scheme_popularity: [],
    purposes_breakdown: []
  };

  return (
    <div className="max-w-7xl mx-auto py-6 px-4 space-y-8 font-sans text-slate-900">
      
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold mb-2">
            <BarChart3 className="w-3.5 h-3.5" />
            <span>SIH26092 National Impact Dashboard</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-slate-900">National Inclusion &amp; Scheme Analytics</h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            Real-time telemetry on financial empowerment across marginalized cohorts, rural districts, and nodal bank sanction funnels.
          </p>
        </div>

        <button
          onClick={loadAnalytics}
          className="px-4 py-2 bg-white border border-slate-200 hover:bg-slate-50 rounded-xl text-xs font-bold text-slate-700 shadow-sm flex items-center gap-2 self-start md:self-auto cursor-pointer"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Refresh Analytics</span>
        </button>
      </div>

      {/* Top Metric Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-3xl border border-slate-200 shadow-sm space-y-1">
          <span className="text-[10px] font-black uppercase tracking-wider text-slate-400">Total Beneficiaries</span>
          <h3 className="text-2xl sm:text-3xl font-black text-slate-900">{s.total_customers}</h3>
          <span className="text-[10px] font-bold text-emerald-600 block">Verified Citizen Profiles</span>
        </div>

        <div className="bg-white p-5 rounded-3xl border border-slate-200 shadow-sm space-y-1">
          <span className="text-[10px] font-black uppercase tracking-wider text-slate-400">Applications Filed</span>
          <h3 className="text-2xl sm:text-3xl font-black text-indigo-900">{s.total_applications}</h3>
          <span className="text-[10px] font-bold text-indigo-600 block">Across Active Tracks</span>
        </div>

        <div className="bg-white p-5 rounded-3xl border border-slate-200 shadow-sm space-y-1">
          <span className="text-[10px] font-black uppercase tracking-wider text-slate-400">Loans Sanctioned</span>
          <h3 className="text-2xl sm:text-3xl font-black text-emerald-600">{s.loans_approved}</h3>
          <span className="text-[10px] font-bold text-emerald-700 block">Bank Desk Approvals</span>
        </div>

        <div className="bg-slate-900 text-white p-5 rounded-3xl border border-slate-800 shadow-sm space-y-1">
          <span className="text-[10px] font-black uppercase tracking-wider text-emerald-400">Disbursed Subsidy</span>
          <h3 className="text-xl sm:text-2xl font-black text-emerald-400 truncate">{s.subsidy_disbursed_text}</h3>
          <span className="text-[10px] text-slate-400 block truncate">{s.estimated_subsidy_basis}</span>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Real Demographic Inclusion Breakdown */}
        <div className="lg:col-span-6 bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="font-black text-slate-900 text-base">Affirmative Demographic Distribution</h3>
              <p className="text-xs text-slate-500">Live share of marginalized founders &amp; student cohorts</p>
            </div>
            <span className="p-2 rounded-xl bg-emerald-50 text-emerald-800">
              <PieIcon className="w-4 h-4" />
            </span>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={s.demographics_distribution}
                  cx="50%"
                  cy="50%"
                  outerRadius={85}
                  innerRadius={50}
                  paddingAngle={4}
                  dataKey="value"
                  nameKey="name"
                >
                  {s.demographics_distribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.fill || '#10b981'} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderRadius: '12px', border: 'none', color: '#fff', fontSize: '12px' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="grid grid-cols-2 gap-2 pt-2 border-t border-slate-100 text-xs">
            {s.demographics_distribution.map((d, i) => (
              <div key={i} className="flex items-center justify-between p-2 rounded-xl bg-slate-50">
                <div className="flex items-center gap-1.5 truncate">
                  <span className="w-2.5 h-2.5 rounded-full shrink-0" style={{ backgroundColor: d.fill }} />
                  <span className="font-semibold text-slate-700 truncate">{d.name}</span>
                </div>
                <span className="font-mono font-black text-slate-900 ml-1">{d.value}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Real Scheme Popularity Bar Chart */}
        <div className="lg:col-span-6 bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="font-black text-slate-900 text-base">Application Demand by Scheme</h3>
              <p className="text-xs text-slate-500">Number of submitted dossiers per program</p>
            </div>
            <span className="p-2 rounded-xl bg-indigo-50 text-indigo-800">
              <BarChart3 className="w-4 h-4" />
            </span>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={s.scheme_popularity} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#f1f5f9" />
                <XAxis type="number" allowDecimals={false} tick={{ fontSize: 11, fill: '#64748b' }} />
                <YAxis type="category" dataKey="scheme" width={110} tick={{ fontSize: 11, fill: '#64748b', fontWeight: 600 }} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderRadius: '12px', border: 'none', color: '#fff', fontSize: '12px' }} />
                <Bar dataKey="applications" name="Applications" fill="#10b981" radius={[0, 8, 8, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="p-3 rounded-2xl bg-slate-50 text-xs text-slate-600 border border-slate-100 flex items-center justify-between">
            <span>Total Active Master Schemes: <strong>{s.active_schemes}</strong></span>
            <span className="font-mono font-black text-emerald-700">100% Deterministic Rule Engine Match</span>
          </div>
        </div>

      </div>

      {/* State Geographic Cohorts */}
      <div className="bg-white p-6 sm:p-8 rounded-3xl border border-slate-200 shadow-sm space-y-4">
        <div>
          <h3 className="font-black text-slate-900 text-base">State-Wise Beneficiary Penetration</h3>
          <p className="text-xs text-slate-500">Geographic footprint of citizen registrations across Indian states &amp; UTs</p>
        </div>

        <div className="h-64 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={s.users_by_state}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
              <XAxis dataKey="state" tick={{ fontSize: 11, fill: '#64748b' }} />
              <YAxis allowDecimals={false} tick={{ fontSize: 11, fill: '#64748b' }} />
              <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderRadius: '12px', border: 'none', color: '#fff', fontSize: '12px' }} />
              <Bar dataKey="count" name="Beneficiaries" fill="#6366f1" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

    </div>
  );
}
