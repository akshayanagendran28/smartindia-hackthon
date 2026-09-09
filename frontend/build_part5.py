import os

BASE_DIR = r"C:\Users\aksha\.gemini\antigravity\scratch\scheme-sathi\frontend\src"
ADMIN_DIR = os.path.join(BASE_DIR, "pages", "admin")
os.makedirs(ADMIN_DIR, exist_ok=True)

# 18. AdminDashboard.jsx
ADMIN_DASHBOARD = '''import React, { useState, useEffect } from 'react';
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
          <p className="text-xs text-slate-500 mt-1">Create schemes, version revisions (v1.0 -> v2.0), update subsidy slabs and ceilings.</p>
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
'''

# 19. AdminSchemeManagement.jsx
ADMIN_SCHEME_MANAGEMENT = '''import React, { useState, useEffect } from 'react';
import { Building2, Plus, Edit3, Trash2, CheckCircle2, AlertCircle } from 'lucide-react';
import api from '../../services/api';

export default function AdminSchemeManagement() {
  const [schemes, setSchemes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [form, setForm] = useState({
    name: '',
    code: '',
    ministry: 'Ministry of MSME',
    target_category: 'SC/ST/Women',
    max_loan_amount: 5000000,
    description: '',
    repayment_period_months: 84
  });

  useEffect(() => {
    loadSchemes();
  }, []);

  const loadSchemes = () => {
    api.get('/schemes')
      .then(res => setSchemes(res.data || []))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      await api.post('/schemes', form);
      setShowModal(false);
      loadSchemes();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="max-w-6xl mx-auto py-8 px-4 space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-black text-slate-900">Scheme Master Management</h1>
          <p className="text-xs text-slate-500">Add, edit, or upgrade gazetted government loan programs</p>
        </div>

        <button
          onClick={() => setShowModal(true)}
          className="px-4 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs rounded-xl flex items-center gap-1.5 shadow"
        >
          <Plus className="w-4 h-4" />
          <span>Add New Government Scheme</span>
        </button>
      </div>

      <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full text-xs text-left">
            <thead className="bg-slate-50 text-slate-700 border-b border-slate-200 uppercase font-bold text-[10px]">
              <tr>
                <th className="px-4 py-3">Code / Name</th>
                <th className="px-4 py-3">Ministry</th>
                <th className="px-4 py-3">Target Category</th>
                <th className="px-4 py-3">Max Sanction</th>
                <th className="px-4 py-3">Version</th>
                <th className="px-4 py-3">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {schemes.map((s) => (
                <tr key={s.id} className="hover:bg-slate-50">
                  <td className="px-4 py-3">
                    <strong className="font-bold text-slate-900 block">{s.name}</strong>
                    <span className="text-[10px] font-mono text-slate-400">{s.code}</span>
                  </td>
                  <td className="px-4 py-3 text-slate-600">{s.ministry}</td>
                  <td className="px-4 py-3 font-semibold text-emerald-800">{s.target_category || 'All'}</td>
                  <td className="px-4 py-3 font-bold text-slate-900">₹{(s.max_loan_amount / 100000).toLocaleString('en-IN')} L</td>
                  <td className="px-4 py-3 font-mono font-bold text-slate-600">v{s.version || '1.0'}</td>
                  <td className="px-4 py-3">
                    <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800">
                      Active
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-slate-950/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl space-y-4">
            <h3 className="font-extrabold text-slate-900 text-lg">Add New Government Assistance Program</h3>
            <form onSubmit={handleCreate} className="space-y-3 text-xs">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Scheme Name</label>
                <input
                  type="text"
                  required
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                  placeholder="e.g. State Mahila Udyam Scheme"
                  className="w-full p-2 border border-slate-300 rounded-lg"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Scheme Code</label>
                  <input
                    type="text"
                    required
                    value={form.code}
                    onChange={(e) => setForm({ ...form, code: e.target.value })}
                    placeholder="e.g. STATE-MAHILA"
                    className="w-full p-2 border border-slate-300 rounded-lg font-mono uppercase"
                  />
                </div>

                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Max Loan Amount (₹)</label>
                  <input
                    type="number"
                    value={form.max_loan_amount}
                    onChange={(e) => setForm({ ...form, max_loan_amount: Number(e.target.value) })}
                    className="w-full p-2 border border-slate-300 rounded-lg"
                  />
                </div>
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">Description</label>
                <textarea
                  rows="3"
                  value={form.description}
                  onChange={(e) => setForm({ ...form, description: e.target.value })}
                  placeholder="Scheme details and gazetted subsidy terms..."
                  className="w-full p-2 border border-slate-300 rounded-lg"
                />
              </div>

              <div className="flex gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="flex-1 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold rounded-lg"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 py-2 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-lg"
                >
                  Save Scheme
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
'''

# 20. AdminRuleManagement.jsx
ADMIN_RULE_MANAGEMENT = '''import React, { useState } from 'react';
import { ShieldCheck, Plus, Sliders, CheckCircle2 } from 'lucide-react';

export default function AdminRuleManagement() {
  const [rules, setRules] = useState([
    { id: 1, scheme: 'PMEGP', name: 'Demographic Target Rule', condition: "user.social_category in ['SC','ST','OBC','Minority'] or user.gender == 'female'", weight: 30 },
    { id: 2, scheme: 'PMEGP', name: 'Manufacturing Ceiling Rule', condition: "user.business_type == 'manufacturing' and user.project_cost <= 5000000", weight: 25 },
    { id: 3, scheme: 'STANDUP-IND', name: 'Greenfield SC/ST/Woman Rule', condition: "(user.social_category in ['SC','ST'] or user.gender == 'female') and user.required_loan >= 1000000", weight: 35 },
    { id: 4, scheme: 'SVANIDHI', name: 'Street Vendor Certificate Rule', condition: "user.is_street_vendor == True and user.required_loan <= 50000", weight: 40 }
  ]);

  return (
    <div className="max-w-6xl mx-auto py-8 px-4 space-y-6">
      <div>
        <h1 className="text-2xl font-black text-slate-900">Deterministic Rule Engine Builder</h1>
        <p className="text-xs text-slate-500">Directly inspect and customize mathematical conditions for gazette eligibility</p>
      </div>

      <div className="bg-white rounded-2xl border border-slate-200 divide-y divide-slate-100 shadow-sm">
        {rules.map((rule) => (
          <div key={rule.id} className="p-5 flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <span className="font-mono text-xs font-bold text-emerald-800 bg-emerald-100 px-2 py-0.5 rounded">
                  {rule.scheme}
                </span>
                <span className="font-bold text-slate-900 text-sm">{rule.name}</span>
              </div>
              <p className="font-mono text-xs bg-slate-50 p-2 rounded-lg text-slate-700 border border-slate-100">
                {rule.condition}
              </p>
            </div>

            <div className="shrink-0 text-right">
              <span className="text-[10px] uppercase font-bold text-slate-400 block">Rule Weight</span>
              <span className="font-black text-emerald-700 text-lg">+{rule.weight}%</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
'''

# 21. AdminPartnerManagement.jsx
ADMIN_PARTNER_MANAGEMENT = '''import React, { useState, useEffect } from 'react';
import { MapPin, Plus, Phone, Building2 } from 'lucide-react';
import api from '../../services/api';

export default function AdminPartnerManagement() {
  const [partners, setPartners] = useState([]);

  useEffect(() => {
    api.get('/partners')
      .then(res => setPartners(res.data || []))
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="max-w-6xl mx-auto py-8 px-4 space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-black text-slate-900">Partner Bank & CSC Directory</h1>
          <p className="text-xs text-slate-500">Authorized lending institutions linked to OpenStreetMap geolocation</p>
        </div>
      </div>

      <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full text-xs text-left">
            <thead className="bg-slate-50 text-slate-700 border-b border-slate-200 uppercase font-bold text-[10px]">
              <tr>
                <th className="px-4 py-3">Partner Name</th>
                <th className="px-4 py-3">Type</th>
                <th className="px-4 py-3">City / Address</th>
                <th className="px-4 py-3">Coordinates (Lat, Lng)</th>
                <th className="px-4 py-3">Phone</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {partners.map((p) => (
                <tr key={p.id} className="hover:bg-slate-50">
                  <td className="px-4 py-3 font-bold text-slate-900">{p.name}</td>
                  <td className="px-4 py-3 uppercase text-[10px] font-bold text-emerald-700">{p.partner_type}</td>
                  <td className="px-4 py-3 text-slate-600">{p.address}, {p.city}</td>
                  <td className="px-4 py-3 font-mono text-[11px] text-slate-500">{p.latitude}, {p.longitude}</td>
                  <td className="px-4 py-3 text-slate-700">{p.phone}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
'''

# 22. AdminUserManagement.jsx
ADMIN_USER_MANAGEMENT = '''import React from 'react';
import { Users, UserCheck, ShieldCheck } from 'lucide-react';

export default function AdminUserManagement() {
  const users = [
    { name: 'Priya Sharma', email: 'priya@example.com', category: 'SC (Woman)', location: 'Mumbai, Maharashtra', readiness: '85%' },
    { name: 'Rahul Gupta', email: 'rahul@example.com', category: 'OBC (Street Vendor)', location: 'Delhi, NCT', readiness: '95%' },
    { name: 'Ananya Roy', email: 'ananya@example.com', category: 'General (Woman)', location: 'Bengaluru, Karnataka', readiness: '70%' },
    { name: 'Karthik Raja', email: 'karthik@example.com', category: 'Minority (Artisan)', location: 'Chennai, Tamil Nadu', readiness: '90%' }
  ];

  return (
    <div className="max-w-6xl mx-auto py-8 px-4 space-y-6">
      <div>
        <h1 className="text-2xl font-black text-slate-900">Beneficiary Management</h1>
        <p className="text-xs text-slate-500">Registered entrepreneurs, demographic audit logs, and loan applications</p>
      </div>

      <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full text-xs text-left">
            <thead className="bg-slate-50 text-slate-700 border-b border-slate-200 uppercase font-bold text-[10px]">
              <tr>
                <th className="px-4 py-3">Beneficiary Name</th>
                <th className="px-4 py-3">Email</th>
                <th className="px-4 py-3">Social Category</th>
                <th className="px-4 py-3">State / City</th>
                <th className="px-4 py-3">Readiness Score</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {users.map((u, idx) => (
                <tr key={idx} className="hover:bg-slate-50">
                  <td className="px-4 py-3 font-bold text-slate-900">{u.name}</td>
                  <td className="px-4 py-3 text-slate-500">{u.email}</td>
                  <td className="px-4 py-3 font-semibold text-emerald-800">{u.category}</td>
                  <td className="px-4 py-3 text-slate-600">{u.location}</td>
                  <td className="px-4 py-3 font-black text-emerald-700">{u.readiness}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
'''

# 23. AdminAnalyticsPage.jsx
ADMIN_ANALYTICS_PAGE = '''import React from 'react';
import { BarChart3, TrendingUp, Users, PieChart as PieIcon, Award } from 'lucide-react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, PieChart, Pie, Cell } from 'recharts';

export default function AdminAnalyticsPage() {
  const demographicData = [
    { name: 'SC / ST Founders', value: 42, fill: '#10b981' },
    { name: 'Women Entrepreneurs', value: 36, fill: '#06b6d4' },
    { name: 'Minority Communities', value: 14, fill: '#f59e0b' },
    { name: 'General / Others', value: 8, fill: '#64748b' }
  ];

  const schemePopularity = [
    { scheme: 'PMEGP', applications: 1840 },
    { scheme: 'StandUp India', applications: 920 },
    { scheme: 'Mudra Kishore', applications: 1250 },
    { scheme: 'PM SVANidhi', applications: 2100 },
    { scheme: 'Vishwakarma', applications: 1100 }
  ];

  return (
    <div className="max-w-6xl mx-auto py-8 px-4 space-y-8">
      <div>
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold mb-2">
          <BarChart3 className="w-3.5 h-3.5" />
          <span>SIH26092 Impact Dashboard</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-black text-slate-900">National Inclusion & Scheme Analytics</h1>
        <p className="text-xs sm:text-sm text-slate-500 mt-1">
          Tracking financial empowerment across marginalized cohorts, rural districts, and nodal bank sanction funnels.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left Demographics Pie Chart */}
        <div className="lg:col-span-5 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
          <h2 className="text-base font-bold text-slate-900 pb-2 border-b border-slate-100">
            Marginalized Demographics Reach
          </h2>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={demographicData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} label={(e) => `${e.value}%`}>
                  {demographicData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.fill} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="grid grid-cols-2 gap-2 text-xs">
            {demographicData.map((d, i) => (
              <div key={i} className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-full" style={{ backgroundColor: d.fill }}></span>
                <span className="text-slate-700 font-medium">{d.name}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Right Scheme Popularity Bar Chart */}
        <div className="lg:col-span-7 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
          <h2 className="text-base font-bold text-slate-900 pb-2 border-b border-slate-100">
            Applications Evaluated by Scheme
          </h2>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={schemePopularity}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="scheme" tick={{ fontSize: 11 }} />
                <YAxis tick={{ fontSize: 11 }} />
                <Tooltip />
                <Bar dataKey="applications" fill="#10b981" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <p className="text-xs text-slate-500 text-center">
            PM SVANidhi and PMEGP constitute &gt;55% of all AI-driven scheme matching queries.
          </p>
        </div>
      </div>
    </div>
  );
}
'''

with open(os.path.join(ADMIN_DIR, "AdminDashboard.jsx"), "w", encoding="utf-8") as f:
    f.write(ADMIN_DASHBOARD)

with open(os.path.join(ADMIN_DIR, "AdminSchemeManagement.jsx"), "w", encoding="utf-8") as f:
    f.write(ADMIN_SCHEME_MANAGEMENT)

with open(os.path.join(ADMIN_DIR, "AdminRuleManagement.jsx"), "w", encoding="utf-8") as f:
    f.write(ADMIN_RULE_MANAGEMENT)

with open(os.path.join(ADMIN_DIR, "AdminPartnerManagement.jsx"), "w", encoding="utf-8") as f:
    f.write(ADMIN_PARTNER_MANAGEMENT)

with open(os.path.join(ADMIN_DIR, "AdminUserManagement.jsx"), "w", encoding="utf-8") as f:
    f.write(ADMIN_USER_MANAGEMENT)

with open(os.path.join(ADMIN_DIR, "AdminAnalyticsPage.jsx"), "w", encoding="utf-8") as f:
    f.write(ADMIN_ANALYTICS_PAGE)

print("Part 5 Admin pages generated successfully!")
