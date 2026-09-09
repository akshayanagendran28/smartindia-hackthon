import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  Building2, Users, FileCheck, ShieldCheck, TrendingUp, 
  Settings, ArrowRight, BarChart3, Plus, Sparkles 
} from 'lucide-react';
import api from '../../services/api';

export default function AdminDashboard() {
  const [stats, setStats] = useState({
    total_schemes: 9,
    total_partners: 13,
    total_beneficiaries: 12450,
    total_applications: 3820,
    subsidy_disbursed_cr: 142.5
  });
  const [schemes, setSchemes] = useState([]);

  useEffect(() => {
    api.get('/schemes')
      .then(res => setSchemes(res.data || []))
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="space-y-8 max-w-7xl mx-auto py-4">
      {/* Admin Top Banner */}
      <div className="bg-slate-900 text-white rounded-2xl p-6 sm:p-8 shadow-xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <span className="px-3 py-1 rounded-full text-xs font-bold bg-amber-500/20 text-amber-400 border border-amber-500/30">
            Nodal Administrator Console &bull; SIH26092
          </span>
          <h1 className="text-2xl sm:text-3xl font-black mt-2">Scheme Sathi Governance & Rule Control</h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Manage scheme versions, gazette rule engines, partner bank authorizations & beneficiary pipelines.
          </p>
        </div>

        <div className="flex gap-3">
          <Link
            to="/admin/schemes"
            className="px-4 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs rounded-xl flex items-center gap-1.5 shadow"
          >
            <Plus className="w-4 h-4" />
            <span>Add / Edit Scheme</span>
          </Link>
          <Link
            to="/admin/rules"
            className="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 border border-slate-700 text-white font-semibold text-xs rounded-xl"
          >
            Configure Rules
          </Link>
        </div>
      </div>

      {/* Admin KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
          <span className="text-xs font-bold text-slate-400 uppercase">Active Schemes</span>
          <h3 className="text-3xl font-black text-slate-900 mt-1">{schemes.length || stats.total_schemes}</h3>
          <span className="text-[11px] text-emerald-600 font-semibold mt-1 block">Central & State Gazetted</span>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
          <span className="text-xs font-bold text-slate-400 uppercase">Registered Beneficiaries</span>
          <h3 className="text-3xl font-black text-slate-900 mt-1">12,450+</h3>
          <span className="text-[11px] text-teal-600 font-semibold mt-1 block">78% Marginalized / Women</span>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
          <span className="text-xs font-bold text-slate-400 uppercase">Partner Bank Desks</span>
          <h3 className="text-3xl font-black text-slate-900 mt-1">{stats.total_partners}</h3>
          <span className="text-[11px] text-indigo-600 font-semibold mt-1 block">OpenStreetMap Synced</span>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
          <span className="text-xs font-bold text-slate-400 uppercase">Estimated Subsidy Value</span>
          <h3 className="text-3xl font-black text-emerald-700 mt-1">₹142.5 Cr</h3>
          <span className="text-[11px] text-slate-500 font-semibold mt-1 block">Matched & Tracked</span>
        </div>
      </div>

      {/* Management Quick Links */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
        <Link to="/admin/schemes" className="p-6 bg-white rounded-2xl border border-slate-200 hover:border-emerald-500 shadow-sm transition-all group">
          <div className="p-3 rounded-xl bg-emerald-50 text-emerald-700 w-fit mb-4 group-hover:scale-105 transition-transform">
            <Building2 className="w-6 h-6" />
          </div>
          <h3 className="font-extrabold text-slate-900 text-base">Scheme Management & Versioning</h3>
          <p className="text-xs text-slate-500 mt-1">Create schemes, version revisions (v1.0 to v2.0), update subsidy slabs and ceilings.</p>
        </Link>

        <Link to="/admin/rules" className="p-6 bg-white rounded-2xl border border-slate-200 hover:border-emerald-500 shadow-sm transition-all group">
          <div className="p-3 rounded-xl bg-blue-50 text-blue-700 w-fit mb-4 group-hover:scale-105 transition-transform">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <h3 className="font-extrabold text-slate-900 text-base">Deterministic Rule Engine Editor</h3>
          <p className="text-xs text-slate-500 mt-1">Define demographic criteria conditions, required document rules, and SHAP weights.</p>
        </Link>

        <Link to="/admin/analytics" className="p-6 bg-white rounded-2xl border border-slate-200 hover:border-emerald-500 shadow-sm transition-all group">
          <div className="p-3 rounded-xl bg-purple-50 text-purple-700 w-fit mb-4 group-hover:scale-105 transition-transform">
            <BarChart3 className="w-6 h-6" />
          </div>
          <h3 className="font-extrabold text-slate-900 text-base">Impact Analytics & Conversion</h3>
          <p className="text-xs text-slate-500 mt-1">Demographics distribution (SC/ST %, Women %), conversion funnel, state-wise heatmaps.</p>
        </Link>
      </div>
    </div>
  );
}
