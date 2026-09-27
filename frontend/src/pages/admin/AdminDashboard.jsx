import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  Building2, Users, FileCheck, ShieldCheck, TrendingUp, 
  Settings, ArrowRight, BarChart3, Plus, Sparkles, 
  Clock, CheckCircle2, XCircle, AlertCircle, RefreshCw,
  Landmark, CreditCard, Send, Calendar, Eye, Activity,
  ExternalLink, Layers, PieChart as PieIcon, ChevronRight,
  DollarSign, FileText, Check, Search, Filter, ArrowUpRight,
  Phone, Mail, MapPin, AlertTriangle, ShieldAlert, Award
} from 'lucide-react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, PieChart, Pie, Cell } from 'recharts';
import api from '../../services/api';

export default function AdminDashboard() {
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [activeTab, setActiveTab] = useState('pipeline'); // 'pipeline', 'overview', 'audit'

  // Applications & Live Loan Pipeline States
  const [applications, setApplications] = useState([]);
  const [appsLoading, setAppsLoading] = useState(false);
  const [appSearch, setAppSearch] = useState('');
  const [stageFilter, setStageFilter] = useState('ALL'); // 'ALL', 1, 2, 3, 4, 5, 'REJECTED'
  const [advancingAppId, setAdvancingAppId] = useState(null);
  
  // Custom Status / Stage Modal
  const [modalApp, setModalApp] = useState(null);
  const [modalForm, setModalForm] = useState({
    target_stage: '',
    loan_status: '',
    fund_status: '',
    fund_amount: 0,
    remarks: '',
    appointment_date: '',
    appointment_time: '10:30 AM',
    appointment_venue: '',
    appointment_remarks: ''
  });
  const [savingModal, setSavingModal] = useState(false);
  const [toast, setToast] = useState(null);

  const showToast = (msg, type = 'success') => {
    setToast({ msg, type });
    setTimeout(() => setToast(null), 4000);
  };

  const fetchDashboardStats = async () => {
    try {
      setRefreshing(true);
      const res = await api.get('/admin/dashboard');
      setStats(res.data);
    } catch (err) {
      console.error('Failed to load dynamic admin stats:', err);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const fetchApplications = async () => {
    try {
      setAppsLoading(true);
      const params = {};
      if (appSearch) params.search = appSearch;
      if (stageFilter !== 'ALL' && stageFilter !== 'REJECTED') params.stage = Number(stageFilter);
      if (stageFilter === 'REJECTED') params.loan_status = 'REJECTED';

      const res = await api.get('/admin/applications', { params });
      setApplications(res.data.applications || []);
    } catch (err) {
      console.error('Failed to load applications pipeline:', err);
    } finally {
      setAppsLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardStats();
  }, []);

  useEffect(() => {
    fetchApplications();
  }, [appSearch, stageFilter]);

  // Handle 1-Click Advance to Next Stage
  const handleQuickAdvance = async (app) => {
    try {
      setAdvancingAppId(app.id);
      const res = await api.post(`/admin/applications/${app.id}/advance-stage`, {
        remarks: `Advanced to ${app.stage_info?.next_stage_name || 'next stage'} by Administrator.`
      });
      showToast(res.data.message || 'Loan application advanced to next stage successfully!');
      fetchApplications();
      fetchDashboardStats();
    } catch (err) {
      console.error('Failed to advance stage:', err);
      showToast('Failed to advance application stage.', 'error');
    } finally {
      setAdvancingAppId(null);
    }
  };

  const openStageModal = (app) => {
    setModalApp(app);
    setModalForm({
      target_stage: app.stage_info?.current_stage === 1 ? 'STAGE_2_UNDER_REVIEW' :
                    app.stage_info?.current_stage === 2 ? 'STAGE_3_SANCTIONED' :
                    app.stage_info?.current_stage === 3 ? 'STAGE_4_FUNDS_RELEASED' :
                    app.stage_info?.current_stage === 4 ? 'STAGE_5_COMPLETED' : 'STAGE_3_SANCTIONED',
      loan_status: app.loan_status || 'UNDER_REVIEW',
      fund_status: app.fund_status || 'PENDING',
      fund_amount: app.fund_amount || app.subsidy_amount || 0,
      remarks: '',
      appointment_date: app.appointment_date ? app.appointment_date.substring(0, 10) : '',
      appointment_time: app.appointment_time || '10:30 AM',
      appointment_venue: app.appointment_venue || `${app.partner_name || 'Lead District Bank'} Desk`,
      appointment_remarks: app.appointment_remarks || ''
    });
  };

  const handleSaveModalStage = async (e) => {
    e.preventDefault();
    if (!modalApp) return;

    try {
      setSavingModal(true);
      const res = await api.post(`/admin/applications/${modalApp.id}/advance-stage`, modalForm);
      showToast(res.data.message || 'Application updated successfully!');
      setModalApp(null);
      fetchApplications();
      fetchDashboardStats();
    } catch (err) {
      console.error('Failed to save stage update:', err);
      showToast('Error saving stage update.', 'error');
    } finally {
      setSavingModal(false);
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-4 font-sans">
        <RefreshCw className="w-8 h-8 text-emerald-600 animate-spin" />
        <p className="text-sm font-bold text-slate-600">Connecting to National Scheme Sathi Database...</p>
      </div>
    );
  }

  const s = stats || {
    total_customers: 0,
    active_schemes: 0,
    total_schemes: 0,
    total_applications: 0,
    pending_applications: 0,
    eligible_applications: 0,
    pending_invitations: 0,
    assigned_applications: 0,
    loans_under_review: 0,
    loans_approved: 0,
    loans_rejected: 0,
    funds_processing: 0,
    funds_released: 0,
    active_partners: 0,
    total_partners: 0,
    total_documents: 0,
    pending_documents: 0,
    subsidy_disbursed_text: 'Data not available',
    estimated_subsidy_basis: 'No subsidy data recorded yet',
    users_by_state: [],
    demographics_distribution: [],
    purposes_breakdown: [],
    scheme_popularity: [],
    recent_audit_logs: []
  };

  return (
    <div className="space-y-8 max-w-7xl mx-auto py-4 font-sans text-slate-900">
      
      {/* Toast Notification */}
      {toast && (
        <div className={`fixed top-5 right-5 z-50 px-4 py-3 rounded-2xl shadow-2xl border flex items-center gap-3 transition-all ${
          toast.type === 'success' ? 'bg-emerald-950 text-white border-emerald-600' : 'bg-rose-950 text-white border-rose-600'
        }`}>
          {toast.type === 'success' ? <CheckCircle2 className="w-5 h-5 text-emerald-400" /> : <AlertTriangle className="w-5 h-5 text-rose-400" />}
          <span className="text-xs sm:text-sm font-bold">{toast.msg}</span>
        </div>
      )}

      {/* Top Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white rounded-3xl p-6 sm:p-8 shadow-xl relative overflow-hidden border border-slate-800">
        <div className="absolute -right-10 -bottom-10 w-80 h-80 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />
        
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="space-y-2">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 text-xs font-black uppercase tracking-wider border border-emerald-500/30">
              <ShieldCheck className="w-3.5 h-3.5" /> Nodal Governance &amp; Loan Pipeline Console
            </div>
            <h1 className="text-2xl sm:text-3xl font-black tracking-tight text-white">
              Live Scheme Sathi Command Hub
            </h1>
            <p className="text-slate-300 text-xs sm:text-sm max-w-2xl">
              100% Real-time database metrics. Advance loan application stages, approve credit sanctions, disburse margin money subsidy, and notify beneficiaries.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <button
              onClick={() => { fetchDashboardStats(); fetchApplications(); }}
              disabled={refreshing}
              className="px-3.5 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold flex items-center gap-2 border border-slate-700 transition-all cursor-pointer"
              title="Refresh live metrics from database"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${refreshing ? 'animate-spin text-emerald-400' : ''}`} />
              <span>{refreshing ? 'Syncing...' : 'Sync Data'}</span>
            </button>
            <Link
              to="/admin/users"
              className="px-4 py-2.5 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs rounded-xl flex items-center gap-1.5 shadow-lg shadow-emerald-500/20 transition-all cursor-pointer"
            >
              <Users className="w-4 h-4" />
              <span>Manage Customers</span>
            </Link>
          </div>
        </div>
      </div>

      {/* Primary KPI Grid (100% Real DB Data) */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
        
        {/* Total Customers */}
        <div 
          onClick={() => navigate('/admin/users')}
          className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm hover:border-emerald-400 hover:shadow-md transition-all cursor-pointer group"
        >
          <div className="flex items-center justify-between text-slate-400 group-hover:text-emerald-600 transition-colors">
            <span className="text-[10px] font-black uppercase tracking-wider">Registered Beneficiaries</span>
            <Users className="w-4 h-4" />
          </div>
          <h3 className="text-2xl font-black text-slate-900 mt-2">{s.total_customers}</h3>
          <span className="text-[10px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded mt-1.5 inline-block">
            Verified in Database
          </span>
        </div>

        {/* Active Schemes */}
        <div 
          onClick={() => navigate('/admin/schemes')}
          className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm hover:border-emerald-400 hover:shadow-md transition-all cursor-pointer group"
        >
          <div className="flex items-center justify-between text-slate-400 group-hover:text-emerald-600 transition-colors">
            <span className="text-[10px] font-black uppercase tracking-wider">Active Schemes</span>
            <Building2 className="w-4 h-4" />
          </div>
          <h3 className="text-2xl font-black text-slate-900 mt-2">{s.active_schemes}</h3>
          <span className="text-[10px] font-semibold text-slate-500 mt-1.5 block">
            of {s.total_schemes} total in Master
          </span>
        </div>

        {/* Total Applications */}
        <div 
          onClick={() => { setActiveTab('pipeline'); }}
          className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm hover:border-indigo-400 hover:shadow-md transition-all cursor-pointer group"
        >
          <div className="flex items-center justify-between text-slate-400 group-hover:text-indigo-600 transition-colors">
            <span className="text-[10px] font-black uppercase tracking-wider">Applications</span>
            <FileText className="w-4 h-4" />
          </div>
          <h3 className="text-2xl font-black text-indigo-900 mt-2">{s.total_applications}</h3>
          <span className="text-[10px] font-bold text-indigo-700 bg-indigo-50 px-2 py-0.5 rounded mt-1.5 inline-block">
            {s.pending_applications} Pending Review
          </span>
        </div>

        {/* Channel Partners */}
        <div 
          onClick={() => navigate('/admin/partners')}
          className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm hover:border-emerald-400 hover:shadow-md transition-all cursor-pointer group"
        >
          <div className="flex items-center justify-between text-slate-400 group-hover:text-emerald-600 transition-colors">
            <span className="text-[10px] font-black uppercase tracking-wider">Partner Bank Desks</span>
            <Landmark className="w-4 h-4" />
          </div>
          <h3 className="text-2xl font-black text-slate-900 mt-2">{s.active_partners}</h3>
          <span className="text-[10px] font-semibold text-slate-500 mt-1.5 block">
            Authorized Desks &amp; Branches
          </span>
        </div>

        {/* Loans Under Review / Approved */}
        <div 
          onClick={() => { setActiveTab('pipeline'); }}
          className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm hover:border-emerald-400 hover:shadow-md transition-all cursor-pointer group"
        >
          <div className="flex items-center justify-between text-slate-400 group-hover:text-emerald-600 transition-colors">
            <span className="text-[10px] font-black uppercase tracking-wider">Loan Sanctions</span>
            <CreditCard className="w-4 h-4" />
          </div>
          <h3 className="text-2xl font-black text-emerald-600 mt-2">{s.loans_approved}</h3>
          <span className="text-[10px] font-bold text-amber-700 bg-amber-50 px-2 py-0.5 rounded mt-1.5 inline-block">
            {s.loans_under_review} Under Review
          </span>
        </div>

        {/* Subsidy Value */}
        <div className="bg-gradient-to-br from-emerald-900 to-slate-900 text-white p-4 rounded-2xl border border-emerald-800 shadow-sm">
          <div className="flex items-center justify-between text-emerald-300">
            <span className="text-[10px] font-black uppercase tracking-wider">Disbursed Subsidy</span>
            <DollarSign className="w-4 h-4" />
          </div>
          <h3 className="text-xl font-black text-emerald-400 mt-2 truncate">{s.subsidy_disbursed_text}</h3>
          <span className="text-[9px] text-emerald-200/80 mt-1.5 block line-clamp-1" title={s.estimated_subsidy_basis}>
            {s.estimated_subsidy_basis}
          </span>
        </div>

      </div>

      {/* Navigation Quick Filter Tabs */}
      <div className="flex items-center gap-3 border-b border-slate-200 pb-2 overflow-x-auto">
        <button
          onClick={() => setActiveTab('pipeline')}
          className={`px-4 py-2 rounded-xl text-xs font-black transition-all cursor-pointer flex items-center gap-2 ${
            activeTab === 'pipeline' ? 'bg-emerald-600 text-white shadow-md shadow-emerald-600/20' : 'text-slate-600 hover:bg-slate-100 font-bold'
          }`}
        >
          <CreditCard className="w-4 h-4" />
          <span>⚡ Live Loan Approvals &amp; Stage Pipeline ({applications.length})</span>
        </button>

        <button
          onClick={() => setActiveTab('overview')}
          className={`px-4 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer ${
            activeTab === 'overview' ? 'bg-slate-900 text-white shadow-sm' : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          Analytics &amp; Inclusion Breakdown
        </button>

        <button
          onClick={() => setActiveTab('audit')}
          className={`px-4 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer ${
            activeTab === 'audit' ? 'bg-slate-900 text-white shadow-sm' : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          Audit Trails &amp; Logs
        </button>
      </div>

      {/* TAB: LIVE LOAN APPROVALS & STAGE PIPELINE (NEW DYNAMIC INTERFACE) */}
      {activeTab === 'pipeline' && (
        <div className="space-y-6">
          
          {/* Top Operational Stage Filter Toolbar */}
          <div className="bg-white p-5 rounded-3xl border border-slate-200 shadow-sm space-y-4">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div>
                <h3 className="text-lg font-black text-slate-900">Official Loan Stage-by-Stage Approval Engine</h3>
                <p className="text-xs text-slate-500">
                  Inspect active applications, advance approval steps with 1-click, release subsidies, and dispatch live alerts to beneficiaries.
                </p>
              </div>

              <div className="relative w-full md:w-72">
                <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
                <input
                  type="text"
                  placeholder="Search applicant, app #, scheme..."
                  value={appSearch}
                  onChange={(e) => setAppSearch(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 rounded-xl border border-slate-200 text-xs font-semibold bg-slate-50 focus:bg-white focus:ring-2 focus:ring-emerald-500 outline-none"
                />
              </div>
            </div>

            {/* Stage Filter Pills */}
            <div className="flex items-center gap-2 overflow-x-auto pb-1 text-xs">
              <button
                onClick={() => setStageFilter('ALL')}
                className={`px-3.5 py-1.5 rounded-xl font-bold transition-all shrink-0 cursor-pointer ${
                  stageFilter === 'ALL' ? 'bg-slate-900 text-white' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                }`}
              >
                All Stages ({applications.length})
              </button>

              <button
                onClick={() => setStageFilter(1)}
                className={`px-3.5 py-1.5 rounded-xl font-bold transition-all shrink-0 cursor-pointer ${
                  stageFilter === 1 ? 'bg-indigo-600 text-white' : 'bg-indigo-50 text-indigo-800 hover:bg-indigo-100'
                }`}
              >
                Stage 1: Submitted &amp; KYC
              </button>

              <button
                onClick={() => setStageFilter(2)}
                className={`px-3.5 py-1.5 rounded-xl font-bold transition-all shrink-0 cursor-pointer ${
                  stageFilter === 2 ? 'bg-amber-600 text-white' : 'bg-amber-50 text-amber-800 hover:bg-amber-100'
                }`}
              >
                Stage 2: Bank Appraisal (Under Review)
              </button>

              <button
                onClick={() => setStageFilter(3)}
                className={`px-3.5 py-1.5 rounded-xl font-bold transition-all shrink-0 cursor-pointer ${
                  stageFilter === 3 ? 'bg-emerald-600 text-white' : 'bg-emerald-50 text-emerald-800 hover:bg-emerald-100'
                }`}
              >
                Stage 3: Sanction Approved
              </button>

              <button
                onClick={() => setStageFilter(4)}
                className={`px-3.5 py-1.5 rounded-xl font-bold transition-all shrink-0 cursor-pointer ${
                  stageFilter === 4 ? 'bg-teal-600 text-white' : 'bg-teal-50 text-teal-800 hover:bg-teal-100'
                }`}
              >
                Stage 4: Subsidy Released
              </button>

              <button
                onClick={() => setStageFilter(5)}
                className={`px-3.5 py-1.5 rounded-xl font-bold transition-all shrink-0 cursor-pointer ${
                  stageFilter === 5 ? 'bg-slate-800 text-white' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                }`}
              >
                Stage 5: Disbursed &amp; Completed
              </button>
            </div>
          </div>

          {/* Applications Cards List */}
          {appsLoading ? (
            <div className="p-16 text-center text-slate-400 bg-white rounded-3xl border border-slate-200 flex flex-col items-center justify-center gap-3">
              <RefreshCw className="w-8 h-8 animate-spin text-emerald-600" />
              <span className="text-xs font-bold">Querying live loan applications from database...</span>
            </div>
          ) : applications.length === 0 ? (
            <div className="p-12 text-center text-slate-500 bg-white rounded-3xl border border-slate-200 text-xs">
              No applications found matching the selected stage filter in database.
            </div>
          ) : (
            <div className="space-y-4">
              {applications.map((app) => {
                const currentStage = app.stage_info?.current_stage || 1;
                const nextLabel = app.stage_info?.next_action_label;
                const isAdvancing = advancingAppId === app.id;

                return (
                  <div 
                    key={app.id} 
                    className="bg-white rounded-3xl border-2 border-slate-200 hover:border-emerald-400 shadow-sm p-5 sm:p-6 space-y-5 transition-all"
                  >
                    {/* Header Row */}
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100">
                      <div className="flex flex-wrap items-center gap-2">
                        <span className="font-mono text-xs font-black px-2.5 py-1 rounded-xl bg-slate-900 text-white">
                          {app.application_number}
                        </span>
                        <span className="font-mono text-xs font-black px-2.5 py-1 rounded-xl bg-emerald-50 text-emerald-800 border border-emerald-200">
                          {app.scheme_code}
                        </span>
                        <span className="px-2.5 py-0.5 rounded-lg text-[10px] font-bold bg-indigo-50 text-indigo-800 border border-indigo-100">
                          {app.purpose_type || 'BUSINESS'}
                        </span>
                        <span className="px-2.5 py-0.5 rounded-lg text-[10px] font-black bg-amber-50 text-amber-900 border border-amber-200 uppercase">
                          {app.social_category || 'General'}
                        </span>
                      </div>

                      <div className="flex items-center gap-2">
                        <span className="text-[11px] text-slate-400 font-mono">
                          Applied: {app.created_at ? new Date(app.created_at).toLocaleDateString('en-IN') : 'Recently'}
                        </span>
                        <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-black uppercase tracking-wider ${
                          app.loan_status === 'APPROVED' || app.loan_status === 'SANCTIONED'
                            ? 'bg-emerald-100 text-emerald-800 border border-emerald-200'
                            : app.loan_status === 'UNDER_REVIEW'
                            ? 'bg-amber-100 text-amber-800 border border-amber-200'
                            : app.loan_status === 'REJECTED'
                            ? 'bg-rose-100 text-rose-800 border border-rose-200'
                            : 'bg-slate-100 text-slate-700'
                        }`}>
                          {app.loan_status}
                        </span>
                      </div>
                    </div>

                    {/* Main Content Grid: Borrower, Financials, Partner Branch */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-5 text-xs">
                      
                      {/* Borrower Information */}
                      <div className="space-y-1.5 p-3.5 rounded-2xl bg-slate-50 border border-slate-100">
                        <span className="text-[10px] font-black uppercase tracking-wider text-slate-400 block">Beneficiary Citizen</span>
                        <h4 className="font-black text-slate-900 text-sm">{app.customer_name}</h4>
                        <p className="text-slate-600 flex items-center gap-1.5">
                          <Mail className="w-3 h-3 text-slate-400" />
                          <span>{app.customer_email || 'No email provided'}</span>
                        </p>
                        {app.customer_mobile && (
                          <p className="text-slate-600 flex items-center gap-1.5 font-mono">
                            <Phone className="w-3 h-3 text-slate-400" />
                            <span>{app.customer_mobile}</span>
                          </p>
                        )}
                        <p className="text-slate-500 flex items-center gap-1.5">
                          <MapPin className="w-3 h-3 text-slate-400" />
                          <span>{app.district || 'District'}, {app.state || 'State'}</span>
                        </p>
                      </div>

                      {/* Loan & Scheme Financials */}
                      <div className="space-y-1.5 p-3.5 rounded-2xl bg-slate-50 border border-slate-100">
                        <span className="text-[10px] font-black uppercase tracking-wider text-slate-400 block">Scheme &amp; Financials</span>
                        <h4 className="font-black text-slate-900 text-sm truncate" title={app.scheme_name}>
                          {app.scheme_name}
                        </h4>
                        <div className="flex justify-between items-center pt-1">
                          <span className="text-slate-500">Loan Quantum:</span>
                          <span className="font-black text-slate-900 font-mono text-sm">₹{(app.loan_amount || 0).toLocaleString('en-IN')}</span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-slate-500">Govt Subsidy:</span>
                          <span className="font-black text-emerald-700 font-mono">₹{(app.fund_amount || app.subsidy_amount || 0).toLocaleString('en-IN')}</span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-slate-500">Tenure / Rate:</span>
                          <span className="font-bold text-slate-700">{app.tenure_months || 36} Mo @ {app.interest_rate || 8.5}%</span>
                        </div>
                      </div>

                      {/* Assigned Channel Partner Bank */}
                      <div className="space-y-1.5 p-3.5 rounded-2xl bg-slate-50 border border-slate-100">
                        <span className="text-[10px] font-black uppercase tracking-wider text-slate-400 block">Nodal Partner Desk</span>
                        <h4 className="font-black text-slate-900 text-sm truncate" title={app.partner_name || 'No partner'}>
                          {app.partner_name || 'Awaiting Partner Invitation'}
                        </h4>
                        {app.partner_branch && (
                          <p className="text-slate-600 flex items-center gap-1.5">
                            <Landmark className="w-3 h-3 text-slate-400" />
                            <span>{app.partner_branch}</span>
                          </p>
                        )}
                        <div className="flex justify-between items-center pt-1">
                          <span className="text-slate-500">Fund Status:</span>
                          <span className={`font-black uppercase text-[10px] px-2 py-0.5 rounded ${
                            app.fund_status === 'RELEASED' ? 'bg-emerald-100 text-emerald-800' : 'bg-slate-200 text-slate-700'
                          }`}>
                            {app.fund_status}
                          </span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-slate-500">Appointment:</span>
                          <span className="font-bold text-slate-700">{app.appointment_status}</span>
                        </div>
                      </div>

                    </div>

                    {/* Dynamic 5-Step Visual Stepper Bar */}
                    <div className="p-4 rounded-2xl bg-slate-900 text-white space-y-3">
                      <div className="flex items-center justify-between text-xs">
                        <span className="font-black uppercase tracking-wider text-emerald-400 text-[10px]">
                          Current Stage: {app.stage_info?.stage_name} (Stage {currentStage} of 5)
                        </span>
                        {app.stage_info?.next_stage_name && (
                          <span className="text-slate-300 text-[11px]">
                            Next: <strong>{app.stage_info.next_stage_name}</strong>
                          </span>
                        )}
                      </div>

                      <div className="grid grid-cols-2 sm:grid-cols-5 gap-2 text-[11px]">
                        
                        {/* Step 1 */}
                        <div className={`p-2.5 rounded-xl border flex items-center gap-2 ${
                          currentStage >= 1 ? 'bg-emerald-950/70 border-emerald-500/50 text-emerald-300' : 'bg-slate-800/50 border-slate-700 text-slate-400'
                        }`}>
                          <div className={`w-5 h-5 rounded-full flex items-center justify-center font-black text-[10px] shrink-0 ${
                            currentStage >= 1 ? 'bg-emerald-500 text-slate-950' : 'bg-slate-700 text-slate-300'
                          }`}>
                            {currentStage > 1 ? <Check className="w-3 h-3 stroke-[3]" /> : '1'}
                          </div>
                          <span className="font-bold truncate">1. Submitted</span>
                        </div>

                        {/* Step 2 */}
                        <div className={`p-2.5 rounded-xl border flex items-center gap-2 ${
                          currentStage >= 2 ? 'bg-emerald-950/70 border-emerald-500/50 text-emerald-300' : 'bg-slate-800/50 border-slate-700 text-slate-400'
                        }`}>
                          <div className={`w-5 h-5 rounded-full flex items-center justify-center font-black text-[10px] shrink-0 ${
                            currentStage >= 2 ? 'bg-emerald-500 text-slate-950' : 'bg-slate-700 text-slate-300'
                          }`}>
                            {currentStage > 2 ? <Check className="w-3 h-3 stroke-[3]" /> : '2'}
                          </div>
                          <span className="font-bold truncate">2. Bank Appraisal</span>
                        </div>

                        {/* Step 3 */}
                        <div className={`p-2.5 rounded-xl border flex items-center gap-2 ${
                          currentStage >= 3 ? 'bg-emerald-950/70 border-emerald-500/50 text-emerald-300' : 'bg-slate-800/50 border-slate-700 text-slate-400'
                        }`}>
                          <div className={`w-5 h-5 rounded-full flex items-center justify-center font-black text-[10px] shrink-0 ${
                            currentStage >= 3 ? 'bg-emerald-500 text-slate-950' : 'bg-slate-700 text-slate-300'
                          }`}>
                            {currentStage > 3 ? <Check className="w-3 h-3 stroke-[3]" /> : '3'}
                          </div>
                          <span className="font-bold truncate">3. Sanction Approved</span>
                        </div>

                        {/* Step 4 */}
                        <div className={`p-2.5 rounded-xl border flex items-center gap-2 ${
                          currentStage >= 4 ? 'bg-emerald-950/70 border-emerald-500/50 text-emerald-300' : 'bg-slate-800/50 border-slate-700 text-slate-400'
                        }`}>
                          <div className={`w-5 h-5 rounded-full flex items-center justify-center font-black text-[10px] shrink-0 ${
                            currentStage >= 4 ? 'bg-emerald-500 text-slate-950' : 'bg-slate-700 text-slate-300'
                          }`}>
                            {currentStage > 4 ? <Check className="w-3 h-3 stroke-[3]" /> : '4'}
                          </div>
                          <span className="font-bold truncate">4. Subsidy Escrow</span>
                        </div>

                        {/* Step 5 */}
                        <div className={`p-2.5 rounded-xl border flex items-center gap-2 col-span-2 sm:col-span-1 ${
                          currentStage >= 5 ? 'bg-emerald-950/70 border-emerald-500/50 text-emerald-300' : 'bg-slate-800/50 border-slate-700 text-slate-400'
                        }`}>
                          <div className={`w-5 h-5 rounded-full flex items-center justify-center font-black text-[10px] shrink-0 ${
                            currentStage >= 5 ? 'bg-emerald-500 text-slate-950' : 'bg-slate-700 text-slate-300'
                          }`}>
                            {currentStage >= 5 ? <Check className="w-3 h-3 stroke-[3]" /> : '5'}
                          </div>
                          <span className="font-bold truncate">5. Disbursed</span>
                        </div>

                      </div>
                    </div>

                    {/* Direct 1-Click Action Toolbar */}
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pt-1">
                      
                      {/* Left: Quick Dossier & Customer Link */}
                      <div className="flex items-center gap-2">
                        <Link
                          to="/admin/users"
                          className="px-3.5 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-xs flex items-center gap-1.5 transition-all"
                        >
                          <Users className="w-3.5 h-3.5" />
                          <span>Beneficiary Profile &amp; Docs</span>
                        </Link>

                        <button
                          onClick={() => openStageModal(app)}
                          className="px-3.5 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-xs flex items-center gap-1.5 transition-all cursor-pointer"
                          title="Open Custom Stage Dialog with Remarks &amp; Fund Controls"
                        >
                          <Settings className="w-3.5 h-3.5" />
                          <span>Custom Controls &amp; Remarks</span>
                        </button>
                      </div>

                      {/* Right: Primary 1-Click Stage Advancement */}
                      <div className="flex items-center gap-2">
                        {currentStage < 5 && nextLabel && (
                          <button
                            onClick={() => handleQuickAdvance(app)}
                            disabled={isAdvancing}
                            className="px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-black text-xs shadow-lg shadow-emerald-600/20 flex items-center gap-2 transition-all cursor-pointer"
                          >
                            {isAdvancing ? (
                              <RefreshCw className="w-4 h-4 animate-spin" />
                            ) : (
                              <Sparkles className="w-4 h-4" />
                            )}
                            <span>{nextLabel}</span>
                            <ArrowRight className="w-3.5 h-3.5" />
                          </button>
                        )}

                        {currentStage === 5 && (
                          <span className="px-4 py-2 rounded-xl bg-emerald-100 text-emerald-800 font-black text-xs flex items-center gap-1.5">
                            <CheckCircle2 className="w-4 h-4" />
                            <span>100% Fully Disbursed &amp; Completed</span>
                          </span>
                        )}
                      </div>

                    </div>

                  </div>
                );
              })}
            </div>
          )}

        </div>
      )}

      {/* TAB 2: OVERVIEW & REAL ANALYTICS */}
      {activeTab === 'overview' && (
        <div className="space-y-8">
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            
            {/* Real State-wise Beneficiary Distribution */}
            <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="font-black text-slate-900 text-base">State-Wise Beneficiary Cohorts</h3>
                  <p className="text-xs text-slate-500">Live geographic distribution of registered citizens</p>
                </div>
                <span className="text-[10px] font-bold bg-slate-100 px-2.5 py-1 rounded-lg text-slate-600">
                  {s.users_by_state.length} States Active
                </span>
              </div>

              <div className="h-64 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={s.users_by_state}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                    <XAxis dataKey="state" tick={{ fontSize: 11, fill: '#64748b' }} />
                    <YAxis allowDecimals={false} tick={{ fontSize: 11, fill: '#64748b' }} />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#0f172a', borderRadius: '12px', border: 'none', color: '#fff', fontSize: '12px' }}
                    />
                    <Bar dataKey="count" name="Registered Beneficiaries" fill="#10b981" radius={[8, 8, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Real Demographics Breakdown */}
            <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="font-black text-slate-900 text-base">Demographic Inclusion Profile</h3>
                  <p className="text-xs text-slate-500">Beneficiary classification by affirmative categories</p>
                </div>
                <span className="text-[10px] font-bold bg-emerald-100 text-emerald-800 px-2.5 py-1 rounded-lg">
                  Affirmative Action
                </span>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-12 items-center gap-4">
                <div className="sm:col-span-6 h-56 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie 
                        data={s.demographics_distribution} 
                        dataKey="value" 
                        nameKey="name" 
                        cx="50%" 
                        cy="50%" 
                        outerRadius={75}
                        innerRadius={45}
                        paddingAngle={4}
                      >
                        {s.demographics_distribution.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.fill || '#10b981'} />
                        ))}
                      </Pie>
                      <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderRadius: '12px', border: 'none', color: '#fff', fontSize: '12px' }} />
                    </PieChart>
                  </ResponsiveContainer>
                </div>

                <div className="sm:col-span-6 space-y-2 text-xs">
                  {s.demographics_distribution.map((d, i) => (
                    <div key={i} className="flex items-center justify-between p-2 rounded-xl bg-slate-50 border border-slate-100">
                      <div className="flex items-center gap-2">
                        <span className="w-3 h-3 rounded-full" style={{ backgroundColor: d.fill }} />
                        <span className="font-semibold text-slate-700">{d.name}</span>
                      </div>
                      <span className="font-mono font-black text-slate-900">{d.value}</span>
                    </div>
                  ))}
                </div>
              </div>

            </div>

          </div>

          {/* Scheme Popularity & Purposes */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
            
            <div className="lg:col-span-8 bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="font-black text-slate-900 text-base">Scheme Application Demand</h3>
                  <p className="text-xs text-slate-500">Live application count per government scheme program</p>
                </div>
                <Link to="/admin/schemes" className="text-xs font-bold text-emerald-600 hover:text-emerald-700 flex items-center gap-1">
                  <span>View All Master Schemes</span>
                  <ChevronRight className="w-3.5 h-3.5" />
                </Link>
              </div>

              <div className="h-60 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={s.scheme_popularity} layout="vertical">
                    <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#f1f5f9" />
                    <XAxis type="number" allowDecimals={false} tick={{ fontSize: 11, fill: '#64748b' }} />
                    <YAxis type="category" dataKey="scheme" width={110} tick={{ fontSize: 11, fill: '#64748b', fontWeight: 600 }} />
                    <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderRadius: '12px', border: 'none', color: '#fff', fontSize: '12px' }} />
                    <Bar dataKey="applications" name="Applications Submitted" fill="#6366f1" radius={[0, 8, 8, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Application Purpose Breakdown */}
            <div className="lg:col-span-4 bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-4">
              <div>
                <h3 className="font-black text-slate-900 text-base">Purpose Breakdown</h3>
                <p className="text-xs text-slate-500">Classification by citizen application track</p>
              </div>

              <div className="space-y-3">
                {s.purposes_breakdown.map((p, i) => (
                  <div key={i} className="p-3.5 rounded-2xl bg-slate-50 border border-slate-100 flex items-center justify-between">
                    <span className="font-bold text-xs text-slate-800">{p.purpose}</span>
                    <span className="px-2.5 py-1 rounded-lg bg-indigo-100 text-indigo-800 font-mono font-black text-xs">
                      {p.count} Dossiers
                    </span>
                  </div>
                ))}
              </div>
            </div>

          </div>

        </div>
      )}

      {/* TAB 3: AUDIT TRAILS & LOGS */}
      {activeTab === 'audit' && (
        <div className="bg-white p-6 sm:p-8 rounded-3xl border border-slate-200 shadow-sm space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-black text-slate-900">Immutable Audit Trail</h3>
              <p className="text-xs text-slate-500">Chronological record of administrative modifications, rule changes, and status transitions</p>
            </div>
            <span className="px-3 py-1 rounded-full bg-slate-100 text-slate-700 text-xs font-bold">
              {s.recent_audit_logs.length} Recent Events
            </span>
          </div>

          <div className="divide-y divide-slate-100 border border-slate-100 rounded-2xl overflow-hidden text-xs">
            {s.recent_audit_logs.length === 0 ? (
              <div className="p-8 text-center text-slate-400">
                No administrative actions recorded yet. Actions will automatically appear here.
              </div>
            ) : (
              s.recent_audit_logs.map((log) => (
                <div key={log.id} className="p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-2 hover:bg-slate-50/70 transition-colors">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="font-mono font-black text-[10px] px-2 py-0.5 rounded bg-indigo-100 text-indigo-800">
                        {log.action}
                      </span>
                      <span className="font-bold text-slate-900">{log.actor_name} ({log.actor_role})</span>
                    </div>
                    <p className="text-slate-600 text-xs">{log.reason || 'Administrative action logged.'}</p>
                  </div>
                  <span className="text-[10px] font-mono text-slate-400 shrink-0">
                    {log.timestamp ? new Date(log.timestamp).toLocaleString('en-IN') : 'Just now'}
                  </span>
                </div>
              ))
            )}
          </div>
        </div>
      )}

      {/* CUSTOM STAGE & SANCTION CONTROLS MODAL */}
      {modalApp && (
        <div className="fixed inset-0 z-50 bg-slate-900/70 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto">
          <div className="bg-white rounded-3xl max-w-xl w-full p-6 sm:p-8 shadow-2xl border border-slate-100 space-y-6 my-6 max-h-[90vh] overflow-y-auto animate-in fade-in zoom-in-95 text-xs">
            
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <div>
                <h3 className="text-base font-black text-slate-900">Custom Stage &amp; Sanction Controls</h3>
                <p className="text-xs text-slate-500">
                  {modalApp.customer_name} &bull; <span className="font-mono font-bold text-slate-700">{modalApp.application_number}</span>
                </p>
              </div>
              <button
                onClick={() => setModalApp(null)}
                className="p-1.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-600 font-black cursor-pointer"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleSaveModalStage} className="space-y-4">
              
              <div>
                <label className="font-bold text-slate-700 block mb-1">Target Government Stage</label>
                <select
                  value={modalForm.target_stage}
                  onChange={(e) => setModalForm({ ...modalForm, target_stage: e.target.value })}
                  className="w-full p-2.5 rounded-xl border border-slate-200 font-bold bg-slate-50 focus:bg-white outline-none focus:ring-2 focus:ring-emerald-500"
                >
                  <option value="STAGE_2_UNDER_REVIEW">Stage 2: Bank Appraisal (Under Review)</option>
                  <option value="STAGE_3_SANCTIONED">Stage 3: Credit Sanction &amp; In-Principle Approved</option>
                  <option value="STAGE_4_FUNDS_RELEASED">Stage 4: Margin Money Subsidy Released</option>
                  <option value="STAGE_5_COMPLETED">Stage 5: Loan Disbursed &amp; Completed</option>
                  <option value="REJECTED">Reject Application</option>
                </select>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label className="font-bold text-slate-700 block mb-1">Margin Subsidy Amount (₹)</label>
                  <input
                    type="number"
                    value={modalForm.fund_amount}
                    onChange={(e) => setModalForm({ ...modalForm, fund_amount: Number(e.target.value) })}
                    className="w-full p-2.5 rounded-xl border border-slate-200 font-mono font-bold bg-slate-50 focus:bg-white outline-none focus:ring-2 focus:ring-emerald-500"
                  />
                </div>

                <div>
                  <label className="font-bold text-slate-700 block mb-1">Appointment Date (Optional)</label>
                  <input
                    type="date"
                    value={modalForm.appointment_date}
                    onChange={(e) => setModalForm({ ...modalForm, appointment_date: e.target.value })}
                    className="w-full p-2.5 rounded-xl border border-slate-200 font-bold bg-slate-50 focus:bg-white outline-none focus:ring-2 focus:ring-emerald-500"
                  />
                </div>
              </div>

              <div>
                <label className="font-bold text-slate-700 block mb-1">Official Nodal Remarks (Dispatched to Beneficiary)</label>
                <input
                  type="text"
                  placeholder="e.g. Loan sanction issued after physical branch verification."
                  value={modalForm.remarks}
                  onChange={(e) => setModalForm({ ...modalForm, remarks: e.target.value })}
                  className="w-full p-2.5 rounded-xl border border-slate-200 font-medium bg-slate-50 focus:bg-white outline-none focus:ring-2 focus:ring-emerald-500"
                  required
                />
              </div>

              <div className="pt-3 border-t border-slate-100 flex items-center justify-end gap-2">
                <button
                  type="button"
                  onClick={() => setModalApp(null)}
                  className="px-4 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={savingModal}
                  className="px-5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-black flex items-center gap-2 shadow-lg shadow-emerald-600/20 cursor-pointer"
                >
                  {savingModal ? <RefreshCw className="w-4 h-4 animate-spin" /> : <CheckCircle2 className="w-4 h-4" />}
                  <span>Save Stage &amp; Notify Customer</span>
                </button>
              </div>

            </form>

          </div>
        </div>
      )}

      {/* Quick Governance Links */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Link 
          to="/admin/users"
          className="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm hover:border-emerald-400 hover:shadow-md transition-all flex items-center justify-between group"
        >
          <div className="space-y-1">
            <h4 className="font-black text-slate-900 text-sm group-hover:text-emerald-700 transition-colors">
              Customer Management &amp; Dossiers
            </h4>
            <p className="text-xs text-slate-500">Inspect demographic audits, documents &amp; loan states</p>
          </div>
          <ArrowRight className="w-5 h-5 text-slate-400 group-hover:text-emerald-600 transition-all transform group-hover:translate-x-1" />
        </Link>

        <Link 
          to="/admin/schemes"
          className="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm hover:border-emerald-400 hover:shadow-md transition-all flex items-center justify-between group"
        >
          <div className="space-y-1">
            <h4 className="font-black text-slate-900 text-sm group-hover:text-emerald-700 transition-colors">
              Government Scheme Master
            </h4>
            <p className="text-xs text-slate-500">Add, edit, activate or upgrade official programs</p>
          </div>
          <ArrowRight className="w-5 h-5 text-slate-400 group-hover:text-emerald-600 transition-all transform group-hover:translate-x-1" />
        </Link>

        <Link 
          to="/admin/rules"
          className="p-5 rounded-2xl bg-white border border-slate-200 shadow-sm hover:border-emerald-400 hover:shadow-md transition-all flex items-center justify-between group"
        >
          <div className="space-y-1">
            <h4 className="font-black text-slate-900 text-sm group-hover:text-emerald-700 transition-colors">
              Deterministic Rule Engine
            </h4>
            <p className="text-xs text-slate-500">Customize mathematical policy predicates &amp; weights</p>
          </div>
          <ArrowRight className="w-5 h-5 text-slate-400 group-hover:text-emerald-600 transition-all transform group-hover:translate-x-1" />
        </Link>
      </div>

    </div>
  );
}
