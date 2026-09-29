import React, { useState, useEffect, useMemo } from 'react';
import { 
  Users, UserCheck, ShieldCheck, Search, Filter, 
  ChevronRight, Eye, FileText, CheckCircle2, XCircle, 
  AlertTriangle, Clock, Landmark, CreditCard, DollarSign, 
  Calendar, MapPin, Phone, Mail, ArrowLeft, RefreshCw, 
  Sliders, Send, Sparkles, Building, GraduationCap, Briefcase,
  Award, Check, X
} from 'lucide-react';
import api from '../../services/api';

export default function AdminUserManagement() {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [totalCount, setTotalCount] = useState(0);
  
  // Filter states
  const [search, setSearch] = useState('');
  const [stateFilter, setStateFilter] = useState('');
  const [purposeFilter, setPurposeFilter] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('');
  const [loanStatusFilter, setLoanStatusFilter] = useState('');
  
  // Selected Customer Dossier Modal
  const [selectedCustomerId, setSelectedCustomerId] = useState(null);
  const [customerDetails, setCustomerDetails] = useState(null);
  const [detailsLoading, setDetailsLoading] = useState(false);
  
  // Admin View Mode state
  const [adminViewMode, setAdminViewMode] = useState(false);

  // Status update form states for the active application
  const [activeTab, setActiveTab] = useState('overview'); // overview, financial_controls, appointment, documents, recommendations, timeline
  const [statusForm, setStatusForm] = useState({
    application_status: '',
    loan_status: '',
    fund_status: '',
    fund_amount: 0,
    fund_remarks: '',
    appointment_status: '',
    appointment_date: '',
    appointment_time: '10:00 AM',
    appointment_venue: '',
    appointment_remarks: '',
    remarks: ''
  });
  const [savingStatus, setSavingStatus] = useState(false);
  const [toast, setToast] = useState(null);

  const showToast = (msg, type = 'success') => {
    setToast({ msg, type });
    setTimeout(() => setToast(null), 4000);
  };

  const loadCustomers = async () => {
    try {
      setLoading(true);
      const params = {};
      if (search) params.search = search;
      if (stateFilter) params.state = stateFilter;
      if (purposeFilter) params.purpose = purposeFilter;
      if (categoryFilter) params.category = categoryFilter;
      if (loanStatusFilter) params.loan_status = loanStatusFilter;

      const res = await api.get('/admin/customers', { params });
      setCustomers(res.data.customers || []);
      setTotalCount(res.data.total || 0);
    } catch (err) {
      console.error('Failed to load customers:', err);
      showToast('Error loading customer list from database.', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCustomers();
  }, [search, stateFilter, purposeFilter, categoryFilter, loanStatusFilter]);

  // Dynamically derive unique filter lists from the database records
  const availableStates = useMemo(() => {
    const states = customers.map(c => c.state).filter(Boolean);
    return Array.from(new Set(states)).sort();
  }, [customers]);

  const availablePurposes = useMemo(() => {
    const purposes = customers.map(c => c.purpose).filter(Boolean);
    return Array.from(new Set(purposes)).sort();
  }, [customers]);

  const availableCategories = useMemo(() => {
    const categories = customers.map(c => c.social_category).filter(Boolean);
    return Array.from(new Set(categories)).sort();
  }, [customers]);

  const availableLoanStatuses = useMemo(() => {
    const statuses = customers.map(c => c.latest_application?.loan_status).filter(Boolean);
    return Array.from(new Set(statuses)).sort();
  }, [customers]);

  const openCustomerDossier = async (userId) => {
    try {
      setSelectedCustomerId(userId);
      setDetailsLoading(true);
      setActiveTab('overview');
      const res = await api.get(`/admin/customers/${userId}/full-details`);
      setCustomerDetails(res.data);
      
      const latestApp = res.data.applications?.[0];
      if (latestApp) {
        setStatusForm({
          application_status: latestApp.status || 'SUBMITTED',
          loan_status: latestApp.loan_status || 'PENDING',
          fund_status: latestApp.fund_status || 'PENDING',
          fund_amount: latestApp.fund_amount || latestApp.subsidy_amount || 0,
          fund_remarks: latestApp.fund_remarks || '',
          appointment_status: latestApp.appointment_status || 'NOT_REQUIRED',
          appointment_date: latestApp.appointment_date ? latestApp.appointment_date.substring(0, 10) : '',
          appointment_time: latestApp.appointment_time || '10:30 AM',
          appointment_venue: latestApp.appointment_venue || `${latestApp.partner_name || 'Lead District Bank'} Desk`,
          appointment_remarks: latestApp.appointment_remarks || '',
          remarks: ''
        });
      }
    } catch (err) {
      console.error('Failed to load customer dossier:', err);
      showToast('Error loading customer dossier from database.', 'error');
    } finally {
      setDetailsLoading(false);
    }
  };

    const handleQuickAdvanceFromDossier = async () => {
    const activeApp = customerDetails?.applications?.[0];
    if (!activeApp) {
      showToast('No active application found for this customer.', 'error');
      return;
    }
    try {
      setSavingStatus(true);
      const res = await api.post(`/admin/applications/${activeApp.id}/advance-stage`, {
        remarks: 'Advanced to next stage by Administrator from Customer Dossier.'
      });
      showToast(res.data.message || 'Application advanced successfully!');
      const refreshRes = await api.get(`/admin/customers/${selectedCustomerId}/full-details`);
      setCustomerDetails(refreshRes.data);
      loadCustomers();
    } catch (err) {
      console.error('Failed to advance stage:', err);
      showToast('Failed to advance application stage.', 'error');
    } finally {
      setSavingStatus(false);
    }
  };

  const handleUpdateStatus = async (e) => {
    e.preventDefault();
    const activeApp = customerDetails?.applications?.[0];
    if (!activeApp) {
      showToast('No active application found for this customer.', 'error');
      return;
    }

    try {
      setSavingStatus(true);
      const res = await api.post(`/admin/applications/${activeApp.id}/update-status`, statusForm);
      showToast(res.data.message || 'Application lifecycle status updated successfully!');
      
      // Reload full details from database
      const refreshRes = await api.get(`/admin/customers/${selectedCustomerId}/full-details`);
      setCustomerDetails(refreshRes.data);
      loadCustomers(); // refresh table counts
    } catch (err) {
      console.error('Failed to update status:', err);
      showToast('Failed to update application status.', 'error');
    } finally {
      setSavingStatus(false);
    }
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto py-4 font-sans text-slate-900">
      
      {/* Toast Notification */}
      {toast && (
        <div className={`fixed top-5 right-5 z-50 px-4 py-3 rounded-xl shadow-xl border flex items-center gap-3 transition-all ${
          toast.type === 'success' ? 'bg-emerald-900 text-white border-emerald-700' : 'bg-rose-900 text-white border-rose-700'
        }`}>
          {toast.type === 'success' ? <CheckCircle2 className="w-5 h-5 text-emerald-400" /> : <AlertTriangle className="w-5 h-5 text-rose-400" />}
          <span className="text-sm font-semibold">{toast.msg}</span>
        </div>
      )}

      {/* Admin View Mode Header Banner */}
      {adminViewMode && (
        <div className="bg-amber-500 text-slate-950 p-4 rounded-2xl shadow-lg border-2 border-amber-600 flex items-center justify-between sticky top-4 z-40 animate-in fade-in">
          <div className="flex items-center gap-3">
            <ShieldCheck className="w-6 h-6 stroke-[2.5]" />
            <div>
              <span className="font-black text-sm uppercase tracking-wider block">ADMIN VIEW MODE (AUDITED PREVIEW)</span>
              <span className="text-xs font-semibold">
                Viewing customer dossier for <strong>{customerDetails?.user?.full_name}</strong> ({customerDetails?.user?.email}). All updates are logged in Audit Trail.
              </span>
            </div>
          </div>
          <button
            onClick={() => setAdminViewMode(false)}
            className="px-4 py-2 bg-slate-950 text-white hover:bg-slate-900 rounded-xl font-bold text-xs shadow cursor-pointer"
          >
            Return to Admin Console
          </button>
        </div>
      )}

      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold mb-1">
            <Users className="w-3.5 h-3.5" />
            <span>Beneficiary Pipeline ({totalCount} Registered from DB)</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-slate-900">Registered Beneficiary Management</h1>
          <p className="text-xs text-slate-500">Inspect demographic records, verify citizen documents, and execute loan/subsidy lifecycle processing</p>
        </div>

        <button 
          onClick={loadCustomers}
          className="px-4 py-2 bg-white border border-slate-200 hover:bg-slate-50 rounded-xl font-bold text-xs flex items-center gap-2 text-slate-700 shadow-sm cursor-pointer"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          <span>Refresh Database</span>
        </button>
      </div>

      {/* Search & Dynamic Filter Bar */}
      <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm flex flex-col md:flex-row items-center gap-4">
        <div className="relative flex-1 w-full">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
          <input 
            type="text"
            placeholder="Search by name, email, or mobile..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-10 pr-4 py-2 rounded-xl border border-slate-200 text-xs font-semibold bg-slate-50 focus:bg-white focus:ring-2 focus:ring-emerald-500 outline-none"
          />
        </div>

        <div className="flex flex-wrap items-center gap-3 w-full md:w-auto">
          {/* Dynamic State Filter */}
          <select
            value={stateFilter}
            onChange={(e) => setStateFilter(e.target.value)}
            className="p-2 rounded-xl border border-slate-200 text-xs font-semibold bg-slate-50 focus:bg-white outline-none"
          >
            <option value="">All States ({availableStates.length})</option>
            {availableStates.map((st) => (
              <option key={st} value={st}>{st}</option>
            ))}
          </select>

          {/* Dynamic Purpose Filter */}
          <select
            value={purposeFilter}
            onChange={(e) => setPurposeFilter(e.target.value)}
            className="p-2 rounded-xl border border-slate-200 text-xs font-semibold bg-slate-50 focus:bg-white outline-none"
          >
            <option value="">All Tracks / Purposes ({availablePurposes.length})</option>
            {availablePurposes.map((p) => (
              <option key={p} value={p}>{p}</option>
            ))}
          </select>

          {/* Dynamic Category / Demographic Filter */}
          {availableCategories.length > 0 && (
            <select
              value={categoryFilter}
              onChange={(e) => setCategoryFilter(e.target.value)}
              className="p-2 rounded-xl border border-slate-200 text-xs font-semibold bg-slate-50 focus:bg-white outline-none"
            >
              <option value="">All Categories ({availableCategories.length})</option>
              {availableCategories.map((cat) => (
                <option key={cat} value={cat}>{cat}</option>
              ))}
            </select>
          )}

          {/* Dynamic Loan Status Filter */}
          {availableLoanStatuses.length > 0 && (
            <select
              value={loanStatusFilter}
              onChange={(e) => setLoanStatusFilter(e.target.value)}
              className="p-2 rounded-xl border border-slate-200 text-xs font-semibold bg-slate-50 focus:bg-white outline-none"
            >
              <option value="">All Loan Statuses</option>
              {availableLoanStatuses.map((st) => (
                <option key={st} value={st}>{st}</option>
              ))}
            </select>
          )}
        </div>
      </div>

      {/* Beneficiary Table */}
      <div className="bg-white rounded-3xl border border-slate-200 overflow-hidden shadow-sm">
        {loading ? (
          <div className="p-12 text-center text-slate-400 text-xs flex flex-col items-center justify-center gap-3">
            <RefreshCw className="w-6 h-6 animate-spin text-emerald-600" />
            <span>Loading registered customer records from database...</span>
          </div>
        ) : customers.length === 0 ? (
          <div className="p-12 text-center text-slate-500 text-xs">
            No customers found matching the search criteria in database.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-xs text-left">
              <thead className="bg-slate-50 text-slate-700 border-b border-slate-200 uppercase font-black text-[10px] tracking-wider">
                <tr>
                  <th className="px-5 py-4">Beneficiary</th>
                  <th className="px-4 py-4">Category / Demographic</th>
                  <th className="px-4 py-4">Location</th>
                  <th className="px-4 py-4">Application &amp; Scheme</th>
                  <th className="px-4 py-4">Loan Status</th>
                  <th className="px-4 py-4">Fund Status</th>
                  <th className="px-4 py-4">Docs Verified</th>
                  <th className="px-4 py-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 font-medium">
                {customers.map((c) => {
                  const app = c.latest_application;
                  return (
                    <tr key={c.id} className="hover:bg-slate-50/70 transition-colors">
                      <td className="px-5 py-4">
                        <div className="space-y-0.5">
                          <span className="font-bold text-slate-900 text-sm block">{c.full_name}</span>
                          <span className="text-slate-500 text-[11px] block">{c.email}</span>
                          {c.mobile && <span className="text-slate-400 text-[10px] font-mono">{c.mobile}</span>}
                        </div>
                      </td>

                      <td className="px-4 py-4">
                        <div className="space-y-1">
                          <span className="inline-block px-2 py-0.5 rounded text-[10px] font-black bg-indigo-50 text-indigo-800 border border-indigo-100">
                            {c.social_category || 'Not Specified'}{c.gender ? ` (${c.gender})` : ''}
                          </span>
                          <span className="text-[11px] text-slate-500 block">
                            {c.age ? `Age: ${c.age} yrs` : 'Age: Not Specified'}
                          </span>
                        </div>
                      </td>

                      <td className="px-4 py-4">
                        <div className="space-y-0.5">
                          <span className="font-semibold text-slate-800">{c.district || 'District N/A'}</span>
                          <span className="text-slate-500 text-[11px] block">{c.state || 'State N/A'}</span>
                        </div>
                      </td>

                      <td className="px-4 py-4">
                        {app ? (
                          <div className="space-y-1">
                            <span className="font-mono text-[10px] font-bold text-emerald-800 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                              {app.scheme_code || 'SCHEME'}
                            </span>
                            <span className="font-mono text-[10px] text-slate-500 block">{app.application_number}</span>
                            <span className="text-[11px] font-bold text-slate-900 block">
                              ₹{(app.loan_amount || 0).toLocaleString('en-IN')}
                            </span>
                          </div>
                        ) : (
                          <span className="text-slate-400 italic text-[11px]">No application yet</span>
                        )}
                      </td>

                      <td className="px-4 py-4">
                        {app ? (
                          <span className={`inline-block px-2.5 py-1 rounded-full text-[10px] font-black uppercase tracking-wider ${
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
                        ) : (
                          <span className="text-slate-400 text-[10px]">--</span>
                        )}
                      </td>

                      <td className="px-4 py-4">
                        {app ? (
                          <span className={`inline-block px-2.5 py-1 rounded-full text-[10px] font-black uppercase tracking-wider ${
                            app.fund_status === 'RELEASED'
                              ? 'bg-emerald-100 text-emerald-800 border border-emerald-200'
                              : app.fund_status === 'PROCESSING' || app.fund_status === 'APPROVED'
                              ? 'bg-indigo-100 text-indigo-800 border border-indigo-200'
                              : app.fund_status === 'ON_HOLD'
                              ? 'bg-amber-100 text-amber-800 border border-amber-200'
                              : 'bg-slate-100 text-slate-700'
                          }`}>
                            {app.fund_status}
                          </span>
                        ) : (
                          <span className="text-slate-400 text-[10px]">--</span>
                        )}
                      </td>

                      <td className="px-4 py-4">
                        <div className="space-y-0.5">
                          <span className="font-bold text-slate-800 text-[11px]">
                            {c.verified_documents || 0} / {c.total_documents || 0}
                          </span>
                          <div className="w-16 h-1.5 bg-slate-100 rounded-full overflow-hidden">
                            <div 
                              className="h-full bg-emerald-500 rounded-full" 
                              style={{ width: `${c.readiness_pct || 0}%` }}
                            />
                          </div>
                        </div>
                      </td>

                      <td className="px-4 py-4 text-right">
                        <button
                          onClick={() => openCustomerDossier(c.id)}
                          className="px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs inline-flex items-center gap-1 shadow-sm transition-all cursor-pointer"
                        >
                          <Eye className="w-3.5 h-3.5" />
                          <span>View Dossier</span>
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* FULL CUSTOMER DOSSIER MODAL */}
      {selectedCustomerId && (
        <div className="fixed inset-0 z-50 bg-slate-900/70 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto">
          <div className="bg-white rounded-3xl max-w-5xl w-full p-6 sm:p-8 shadow-2xl border border-slate-100 space-y-6 my-6 max-h-[92vh] overflow-y-auto animate-in fade-in zoom-in-95">
            
            {detailsLoading ? (
              <div className="p-16 text-center text-slate-400 text-xs flex flex-col items-center justify-center gap-3">
                <RefreshCw className="w-8 h-8 animate-spin text-emerald-600" />
                <span>Loading complete citizen records &amp; audit history from database...</span>
              </div>
            ) : customerDetails ? (
              <div className="space-y-6">
                
                {/* Modal Header */}
                <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-100 gap-4">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 rounded-2xl bg-emerald-100 text-emerald-800 flex items-center justify-center font-black text-lg">
                      {customerDetails.user?.full_name?.charAt(0) || 'U'}
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <h2 className="font-black text-slate-900 text-xl">{customerDetails.user?.full_name}</h2>
                        <span className="px-2 py-0.5 rounded text-[10px] font-black uppercase bg-indigo-100 text-indigo-800">
                          {customerDetails.profile?.social_category || customerDetails.profile?.category || 'Not Specified'}
                          {customerDetails.profile?.gender ? ` • ${customerDetails.profile.gender}` : ''}
                        </span>
                      </div>
                      <p className="text-xs text-slate-500 flex items-center gap-3 mt-0.5">
                        <span className="flex items-center gap-1"><Mail className="w-3 h-3 text-slate-400" /> {customerDetails.user?.email}</span>
                        {customerDetails.user?.mobile && <span className="flex items-center gap-1"><Phone className="w-3 h-3 text-slate-400" /> {customerDetails.user.mobile}</span>}
                        <span className="flex items-center gap-1">
                          <MapPin className="w-3 h-3 text-slate-400" /> 
                          {customerDetails.profile?.district || customerDetails.user?.district || 'District N/A'}, {customerDetails.profile?.state || customerDetails.user?.state || 'State N/A'}
                        </span>
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => setAdminViewMode(true)}
                      className="px-3.5 py-2 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-black text-xs shadow-sm flex items-center gap-1.5 cursor-pointer"
                      title="Preview portal as this citizen with Admin View Mode Banner"
                    >
                      <Sparkles className="w-3.5 h-3.5" />
                      <span>Admin View Mode</span>
                    </button>

                    <button
                      onClick={() => { setSelectedCustomerId(null); setCustomerDetails(null); }}
                      className="p-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-600 font-black text-sm cursor-pointer"
                    >
                      ✕
                    </button>
                  </div>
                </div>

                {/* Sub-Navigation Tabs */}
                <div className="flex items-center gap-2 border-b border-slate-100 pb-2 overflow-x-auto text-xs font-bold">
                  <button
                    onClick={() => setActiveTab('overview')}
                    className={`px-3 py-1.5 rounded-lg transition-all cursor-pointer ${
                      activeTab === 'overview' ? 'bg-slate-900 text-white' : 'text-slate-600 hover:bg-slate-100'
                    }`}
                  >
                    Dossier Overview
                  </button>
                  <button
                    onClick={() => setActiveTab('financial_controls')}
                    className={`px-3 py-1.5 rounded-lg transition-all cursor-pointer ${
                      activeTab === 'financial_controls' ? 'bg-emerald-600 text-white' : 'text-emerald-700 hover:bg-emerald-50'
                    }`}
                  >
                    ⚡ Process Loan &amp; Funds
                  </button>
                  <button
                    onClick={() => setActiveTab('appointment')}
                    className={`px-3 py-1.5 rounded-lg transition-all cursor-pointer ${
                      activeTab === 'appointment' ? 'bg-indigo-600 text-white' : 'text-indigo-700 hover:bg-indigo-50'
                    }`}
                  >
                    📅 Schedule Appointment
                  </button>
                  <button
                    onClick={() => setActiveTab('documents')}
                    className={`px-3 py-1.5 rounded-lg transition-all cursor-pointer ${
                      activeTab === 'documents' ? 'bg-slate-900 text-white' : 'text-slate-600 hover:bg-slate-100'
                    }`}
                  >
                    Documents ({customerDetails.documents?.length || 0})
                  </button>
                  <button
                    onClick={() => setActiveTab('recommendations')}
                    className={`px-3 py-1.5 rounded-lg transition-all cursor-pointer ${
                      activeTab === 'recommendations' ? 'bg-slate-900 text-white' : 'text-slate-600 hover:bg-slate-100'
                    }`}
                  >
                    Matched Schemes ({customerDetails.recommendations?.length || 0})
                  </button>
                  <button
                    onClick={() => setActiveTab('timeline')}
                    className={`px-3 py-1.5 rounded-lg transition-all cursor-pointer ${
                      activeTab === 'timeline' ? 'bg-slate-900 text-white' : 'text-slate-600 hover:bg-slate-100'
                    }`}
                  >
                    Status Timeline &amp; Audit
                  </button>
                </div>

                {/* TAB: OVERVIEW */}
                {activeTab === 'overview' && (
                  <div className="space-y-6 text-xs">
                    
                    {/* Active Scheme Application Card */}
                    {customerDetails.applications?.length > 0 ? (
                      <div className="p-5 rounded-2xl bg-gradient-to-br from-slate-900 to-indigo-950 text-white space-y-4">
                        <div className="flex items-center justify-between">
                          <span className="font-mono text-xs text-emerald-400 font-black">
                            {customerDetails.applications[0].application_number}
                          </span>
                          <span className="px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 font-bold uppercase text-[10px]">
                            {customerDetails.applications[0].status}
                          </span>
                        </div>

                        <div>
                          <h3 className="font-black text-lg text-white">
                            {customerDetails.applications[0].scheme_name} ({customerDetails.applications[0].scheme_code})
                          </h3>
                          <p className="text-slate-300 text-xs">
                            Loan Required: <strong>₹{(customerDetails.applications[0].loan_amount || 0).toLocaleString('en-IN')}</strong> &bull; Tenure: {customerDetails.applications[0].tenure_months || 36} Months &bull; Moratorium: {customerDetails.applications[0].moratorium_months || 6} Months
                          </p>
                        </div>

                        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2 border-t border-slate-800 text-[11px]">
                          <div>
                            <span className="text-slate-400 block">Loan Status</span>
                            <span className="font-black text-amber-400">{customerDetails.applications[0].loan_status}</span>
                          </div>
                          <div>
                            <span className="text-slate-400 block">Fund Status</span>
                            <span className="font-black text-emerald-400">{customerDetails.applications[0].fund_status}</span>
                          </div>
                          <div>
                            <span className="text-slate-400 block">Assigned Partner</span>
                            <span className="font-bold text-slate-200">{customerDetails.applications[0].partner_name}</span>
                          </div>
                          <div>
                            <span className="text-slate-400 block">Appointment</span>
                            <span className="font-bold text-slate-200">{customerDetails.applications[0].appointment_status}</span>
                          </div>
                        </div>
                      </div>
                    ) : (
                      <div className="p-6 text-center bg-slate-50 border border-slate-200 rounded-2xl text-slate-500">
                        No submitted scheme application found in database for this citizen.
                      </div>
                    )}

                    {/* Personal & Demographic Profile */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-2.5">
                        <h4 className="font-black text-slate-900 text-sm">Personal &amp; Demographic Profile</h4>
                        <div className="space-y-1.5 text-slate-700">
                          <div className="flex justify-between">
                            <span className="text-slate-500">Age:</span>
                            <span className="font-bold">{customerDetails.profile?.age ? `${customerDetails.profile.age} Years` : 'Not Specified'}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-slate-500">Gender:</span>
                            <span className="font-bold uppercase">{customerDetails.profile?.gender || 'Not Specified'}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-slate-500">Affirmative Category:</span>
                            <span className="font-bold text-indigo-700">{customerDetails.profile?.social_category || customerDetails.profile?.category || 'Not Specified'}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-slate-500">Annual Income:</span>
                            <span className="font-mono font-bold">
                              {customerDetails.profile?.annual_income ? `₹${customerDetails.profile.annual_income.toLocaleString('en-IN')}` : 'Not Specified'}
                            </span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-slate-500">Area Type:</span>
                            <span className="font-bold uppercase">{customerDetails.profile?.area_type || 'Rural'}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-slate-500">Skill Training:</span>
                            <span className="font-bold text-emerald-700">{customerDetails.profile?.has_skill_training ? 'Certified / Verified' : 'Not Recorded'}</span>
                          </div>
                        </div>
                      </div>

                      <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-2.5">
                        <h4 className="font-black text-slate-900 text-sm">Purpose &amp; Project Details</h4>
                        <div className="space-y-1.5 text-slate-700">
                          <div className="flex justify-between">
                            <span className="text-slate-500">Track:</span>
                            <span className="font-bold">{customerDetails.profile?.purpose || customerDetails.profile?.purpose_type || 'Not Specified'}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-slate-500">Business / Activity Type:</span>
                            <span className="font-bold">{customerDetails.profile?.business_type || 'N/A'}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-slate-500">Industry / Sector:</span>
                            <span className="font-bold">{customerDetails.profile?.industry_sector || 'N/A'}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-slate-500">Total Project Cost:</span>
                            <span className="font-mono font-bold text-emerald-700">
                              {customerDetails.profile?.project_cost ? `₹${customerDetails.profile.project_cost.toLocaleString('en-IN')}` : 'N/A'}
                            </span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-slate-500">Required Loan:</span>
                            <span className="font-mono font-bold text-slate-900">
                              {customerDetails.profile?.required_loan ? `₹${customerDetails.profile.required_loan.toLocaleString('en-IN')}` : 'N/A'}
                            </span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-slate-500">Education / Course:</span>
                            <span className="font-bold">{customerDetails.profile?.education || customerDetails.profile?.course || 'Not Specified'}</span>
                          </div>
                        </div>
                      </div>
                    </div>

                  </div>
                )}

                {/* TAB: FINANCIAL & FUND PROCESSING */}
                {activeTab === 'financial_controls' && (
                  <div className="space-y-6 text-xs">
                    
                    {/* Visual 5-Step Stepper */}
                    {customerDetails.applications?.length > 0 && (() => {
                      const app = customerDetails.applications[0];
                      const l_stat = (app.loan_status || 'PENDING').toUpperCase();
                      const f_stat = (app.fund_status || 'PENDING').toUpperCase();
                      const app_stat = (app.status || 'SUBMITTED').toUpperCase();

                      let curStage = 1;
                      let stageName = "1. Submitted & KYC";
                      let nextLabel = "⚡ Move to Stage 2: Bank Desk Appraisal";

                      if (app_stat === 'COMPLETED') {
                        curStage = 5;
                        stageName = "5. Disbursed & Completed";
                        nextLabel = null;
                      } else if (f_stat === 'RELEASED') {
                        curStage = 4;
                        stageName = "4. Govt Subsidy Released";
                        nextLabel = "⚡ Complete Final Loan Stage";
                      } else if (l_stat === 'APPROVED' || l_stat === 'SANCTIONED') {
                        curStage = 3;
                        stageName = "3. Credit Sanction Approved";
                        nextLabel = "⚡ Disburse Govt Margin Subsidy";
                      } else if (l_stat === 'UNDER_REVIEW' || app_stat === 'PARTNER_ASSIGNED') {
                        curStage = 2;
                        stageName = "2. Partner Bank Appraisal";
                        nextLabel = "⚡ Approve Loan Sanction";
                      }

                      return (
                        <div className="p-4 rounded-2xl bg-slate-900 text-white space-y-3">
                          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                            <span className="font-black uppercase tracking-wider text-emerald-400 text-[10px]">
                              Current Lifecycle Stage: {stageName} (Stage {curStage} of 5)
                            </span>
                            {nextLabel && (
                              <button
                                type="button"
                                onClick={handleQuickAdvanceFromDossier}
                                disabled={savingStatus}
                                className="px-4 py-2 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs shadow-md flex items-center gap-1.5 transition-all cursor-pointer self-start sm:self-auto"
                              >
                                {savingStatus ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <Sparkles className="w-3.5 h-3.5" />}
                                <span>{nextLabel}</span>
                              </button>
                            )}
                          </div>

                          <div className="grid grid-cols-2 sm:grid-cols-5 gap-2 text-[10px]">
                            <div className={`p-2 rounded-xl border flex items-center gap-1.5 ${curStage >= 1 ? 'bg-emerald-950/70 border-emerald-500/50 text-emerald-300' : 'bg-slate-800/50 border-slate-700 text-slate-400'}`}>
                              <span className={`w-4 h-4 rounded-full flex items-center justify-center font-bold text-[9px] ${curStage >= 1 ? 'bg-emerald-500 text-slate-950' : 'bg-slate-700'}`}>{curStage > 1 ? '✓' : '1'}</span>
                              <span className="font-bold truncate">1. Submitted</span>
                            </div>
                            <div className={`p-2 rounded-xl border flex items-center gap-1.5 ${curStage >= 2 ? 'bg-emerald-950/70 border-emerald-500/50 text-emerald-300' : 'bg-slate-800/50 border-slate-700 text-slate-400'}`}>
                              <span className={`w-4 h-4 rounded-full flex items-center justify-center font-bold text-[9px] ${curStage >= 2 ? 'bg-emerald-500 text-slate-950' : 'bg-slate-700'}`}>{curStage > 2 ? '✓' : '2'}</span>
                              <span className="font-bold truncate">2. Appraisal</span>
                            </div>
                            <div className={`p-2 rounded-xl border flex items-center gap-1.5 ${curStage >= 3 ? 'bg-emerald-950/70 border-emerald-500/50 text-emerald-300' : 'bg-slate-800/50 border-slate-700 text-slate-400'}`}>
                              <span className={`w-4 h-4 rounded-full flex items-center justify-center font-bold text-[9px] ${curStage >= 3 ? 'bg-emerald-500 text-slate-950' : 'bg-slate-700'}`}>{curStage > 3 ? '✓' : '3'}</span>
                              <span className="font-bold truncate">3. Sanction</span>
                            </div>
                            <div className={`p-2 rounded-xl border flex items-center gap-1.5 ${curStage >= 4 ? 'bg-emerald-950/70 border-emerald-500/50 text-emerald-300' : 'bg-slate-800/50 border-slate-700 text-slate-400'}`}>
                              <span className={`w-4 h-4 rounded-full flex items-center justify-center font-bold text-[9px] ${curStage >= 4 ? 'bg-emerald-500 text-slate-950' : 'bg-slate-700'}`}>{curStage > 4 ? '✓' : '4'}</span>
                              <span className="font-bold truncate">4. Subsidy Escrow</span>
                            </div>
                            <div className={`p-2 rounded-xl border flex items-center gap-1.5 col-span-2 sm:col-span-1 ${curStage >= 5 ? 'bg-emerald-950/70 border-emerald-500/50 text-emerald-300' : 'bg-slate-800/50 border-slate-700 text-slate-400'}`}>
                              <span className={`w-4 h-4 rounded-full flex items-center justify-center font-bold text-[9px] ${curStage >= 5 ? 'bg-emerald-500 text-slate-950' : 'bg-slate-700'}`}>{curStage >= 5 ? '✓' : '5'}</span>
                              <span className="font-bold truncate">5. Disbursed</span>
                            </div>
                          </div>
                        </div>
                      );
                    })()}

                    <form onSubmit={handleUpdateStatus} className="space-y-4 pt-2">
                      <div className="p-4 rounded-2xl bg-emerald-50 border border-emerald-200 text-emerald-900">
                        <h4 className="font-black text-sm">Fine-Tune Loan Sanction &amp; Subsidy Fund Status</h4>
                        <p className="text-xs text-emerald-700 mt-0.5">
                          Updating status directly mutates database records, automatically creates a timestamped audit log, and notifies the citizen.
                        </p>
                      </div>

                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        <div>
                          <label className="font-bold text-slate-700 block mb-1">Loan Approval Lifecycle Status</label>
                          <select
                            value={statusForm.loan_status}
                            onChange={(e) => setStatusForm({ ...statusForm, loan_status: e.target.value })}
                            className="w-full p-2.5 rounded-xl border border-slate-200 font-bold bg-slate-50 focus:bg-white outline-none focus:ring-2 focus:ring-emerald-500"
                          >
                            <option value="PENDING">PENDING - Initial Verification</option>
                            <option value="UNDER_REVIEW">UNDER_REVIEW - Branch Appraisal</option>
                            <option value="SANCTIONED">SANCTIONED - Sanction Letter Issued</option>
                            <option value="APPROVED">APPROVED - Final Credit Approved</option>
                            <option value="DISBURSEMENT_PROCESSING">DISBURSEMENT_PROCESSING</option>
                            <option value="REJECTED">REJECTED - Not Feasible</option>
                          </select>
                        </div>

                        <div>
                          <label className="font-bold text-slate-700 block mb-1">Subsidy / Fund Disbursement Status</label>
                          <select
                            value={statusForm.fund_status}
                            onChange={(e) => setStatusForm({ ...statusForm, fund_status: e.target.value })}
                            className="w-full p-2.5 rounded-xl border border-slate-200 font-bold bg-slate-50 focus:bg-white outline-none focus:ring-2 focus:ring-emerald-500"
                          >
                            <option value="PENDING">PENDING - Awaiting Sanction</option>
                            <option value="PROCESSING">PROCESSING - Escrow Routing</option>
                            <option value="APPROVED">APPROVED - Ready for Release</option>
                            <option value="RELEASED">RELEASED - Funds Disbursed</option>
                            <option value="ON_HOLD">ON_HOLD - Compliance Query</option>
                          </select>
                        </div>
                      </div>

                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        <div>
                          <label className="font-bold text-slate-700 block mb-1">Approved Fund / Subsidy Amount (₹)</label>
                          <input
                            type="number"
                            value={statusForm.fund_amount}
                            onChange={(e) => setStatusForm({ ...statusForm, fund_amount: Number(e.target.value) })}
                            className="w-full p-2.5 rounded-xl border border-slate-200 font-mono font-bold bg-slate-50 focus:bg-white outline-none focus:ring-2 focus:ring-emerald-500"
                          />
                        </div>

                        <div>
                          <label className="font-bold text-slate-700 block mb-1">Core Application Status</label>
                          <select
                            value={statusForm.application_status}
                            onChange={(e) => setStatusForm({ ...statusForm, application_status: e.target.value })}
                            className="w-full p-2.5 rounded-xl border border-slate-200 font-bold bg-slate-50 focus:bg-white outline-none focus:ring-2 focus:ring-emerald-500"
                          >
                            <option value="SUBMITTED">SUBMITTED</option>
                            <option value="PARTNER_ASSIGNED">PARTNER_ASSIGNED</option>
                            <option value="UNDER_REVIEW">UNDER_REVIEW</option>
                            <option value="SANCTIONED">SANCTIONED</option>
                            <option value="COMPLETED">COMPLETED</option>
                            <option value="REJECTED">REJECTED</option>
                          </select>
                        </div>
                      </div>

                      <div>
                        <label className="font-bold text-slate-700 block mb-1">Official Remarks / Reason for Customer Timeline</label>
                        <input
                          type="text"
                          placeholder="e.g. Subsidy released to branch escrow account following appraisal."
                          value={statusForm.remarks}
                          onChange={(e) => setStatusForm({ ...statusForm, remarks: e.target.value })}
                          className="w-full p-2.5 rounded-xl border border-slate-200 font-medium bg-slate-50 focus:bg-white outline-none focus:ring-2 focus:ring-emerald-500"
                          required
                        />
                      </div>

                      <div className="flex justify-end pt-2">
                        <button
                          type="submit"
                          disabled={savingStatus}
                          className="px-6 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-black shadow-lg shadow-emerald-600/20 transition-all cursor-pointer flex items-center gap-2"
                        >
                          {savingStatus ? <RefreshCw className="w-4 h-4 animate-spin" /> : <CheckCircle2 className="w-4 h-4" />}
                          <span>Save &amp; Propagate Status to Database</span>
                        </button>
                      </div>
                    </form>
                  </div>
                )}

                {/* TAB: APPOINTMENT SCHEDULING */}
                {activeTab === 'appointment' && (
                  <form onSubmit={handleUpdateStatus} className="space-y-6 text-xs">
                    <div className="p-4 rounded-2xl bg-indigo-50 border border-indigo-200 text-indigo-900">
                      <h4 className="font-black text-sm">Schedule / Reschedule Partner Desk Appointment</h4>
                      <p className="text-xs text-indigo-700 mt-0.5">
                        Set physical branch verification date and venue for the citizen.
                      </p>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                      <div>
                        <label className="font-bold text-slate-700 block mb-1">Appointment Status</label>
                        <select
                          value={statusForm.appointment_status}
                          onChange={(e) => setStatusForm({ ...statusForm, appointment_status: e.target.value })}
                          className="w-full p-2.5 rounded-xl border border-slate-200 font-bold bg-slate-50 focus:bg-white outline-none focus:ring-2 focus:ring-indigo-500"
                        >
                          <option value="NOT_REQUIRED">NOT_REQUIRED</option>
                          <option value="PENDING">PENDING - Citizen Requested</option>
                          <option value="SCHEDULED">SCHEDULED - Confirmed by Nodal Bank</option>
                          <option value="COMPLETED">COMPLETED - Physical Verification Done</option>
                          <option value="RESCHEDULED">RESCHEDULED</option>
                          <option value="MISSED">MISSED</option>
                        </select>
                      </div>

                      <div>
                        <label className="font-bold text-slate-700 block mb-1">Appointment Date</label>
                        <input
                          type="date"
                          value={statusForm.appointment_date}
                          onChange={(e) => setStatusForm({ ...statusForm, appointment_date: e.target.value })}
                          className="w-full p-2.5 rounded-xl border border-slate-200 font-bold bg-slate-50 focus:bg-white outline-none focus:ring-2 focus:ring-indigo-500"
                        />
                      </div>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                      <div>
                        <label className="font-bold text-slate-700 block mb-1">Appointment Time Window</label>
                        <input
                          type="text"
                          placeholder="e.g. 10:30 AM - 12:00 PM"
                          value={statusForm.appointment_time}
                          onChange={(e) => setStatusForm({ ...statusForm, appointment_time: e.target.value })}
                          className="w-full p-2.5 rounded-xl border border-slate-200 font-medium bg-slate-50 focus:bg-white outline-none focus:ring-2 focus:ring-indigo-500"
                        />
                      </div>

                      <div>
                        <label className="font-bold text-slate-700 block mb-1">Branch / Desk Venue</label>
                        <input
                          type="text"
                          placeholder="e.g. Bank of India - Mumbai Lead District Office"
                          value={statusForm.appointment_venue}
                          onChange={(e) => setStatusForm({ ...statusForm, appointment_venue: e.target.value })}
                          className="w-full p-2.5 rounded-xl border border-slate-200 font-medium bg-slate-50 focus:bg-white outline-none focus:ring-2 focus:ring-indigo-500"
                        />
                      </div>
                    </div>

                    <div>
                      <label className="font-bold text-slate-700 block mb-1">Appointment Notes for Customer</label>
                      <input
                        type="text"
                        placeholder="e.g. Please bring original Aadhaar, PAN, and Caste Certificate for physical verification."
                        value={statusForm.remarks}
                        onChange={(e) => setStatusForm({ ...statusForm, remarks: e.target.value })}
                        className="w-full p-2.5 rounded-xl border border-slate-200 font-medium bg-slate-50 focus:bg-white outline-none focus:ring-2 focus:ring-indigo-500"
                        required
                      />
                    </div>

                    <div className="flex justify-end pt-2">
                      <button
                        type="submit"
                        disabled={savingStatus}
                        className="px-6 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-black shadow-lg shadow-indigo-600/20 transition-all cursor-pointer flex items-center gap-2"
                      >
                        {savingStatus ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Calendar className="w-4 h-4" />}
                        <span>Confirm Appointment in Database</span>
                      </button>
                    </div>
                  </form>
                )}

                {/* TAB: DOCUMENTS */}
                {activeTab === 'documents' && (
                  <div className="space-y-4 text-xs">
                    <h4 className="font-black text-slate-900 text-sm">Uploaded Citizen Documents from Database</h4>
                    {customerDetails.documents?.length === 0 ? (
                      <div className="p-8 text-center bg-slate-50 border border-slate-200 rounded-2xl text-slate-400">
                        No documents uploaded by this user in database yet.
                      </div>
                    ) : (
                      <div className="divide-y divide-slate-100 border border-slate-200 rounded-2xl overflow-hidden">
                        {customerDetails.documents.map((d) => (
                          <div key={d.id} className="p-4 flex items-center justify-between hover:bg-slate-50">
                            <div className="flex items-center gap-3">
                              <FileText className="w-5 h-5 text-emerald-600" />
                              <div>
                                <span className="font-bold text-slate-900 uppercase">{d.document_type}</span>
                                <span className="text-[11px] text-slate-500 block">{d.file_name}</span>
                              </div>
                            </div>
                            <span className={`px-2.5 py-1 rounded-full font-black text-[10px] uppercase ${
                              ['VERIFIED', 'SUCCESS', 'MOCK_VERIFIED'].includes(String(d.official_verification || d.verification_status || '').toUpperCase())
                                ? 'bg-emerald-100 text-emerald-800'
                                : 'bg-amber-100 text-amber-800'
                            }`}>
                              {d.official_verification || d.verification_status}
                            </span>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}

                {/* TAB: RECOMMENDATIONS */}
                {activeTab === 'recommendations' && (
                  <div className="space-y-4 text-xs">
                    <h4 className="font-black text-slate-900 text-sm">Scheme Recommendations &amp; Eligibility Matches</h4>
                    {customerDetails.recommendations?.length === 0 ? (
                      <div className="p-8 text-center bg-slate-50 border border-slate-200 rounded-2xl text-slate-400">
                        No matched schemes recorded for this citizen in database.
                      </div>
                    ) : (
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        {customerDetails.recommendations.map((r, idx) => (
                          <div key={idx} className="p-4 rounded-2xl border border-slate-200 bg-slate-50 flex items-center justify-between">
                            <div>
                              <span className="font-mono text-[10px] font-bold text-indigo-700 block">{r.scheme_code}</span>
                              <span className="font-black text-slate-900 text-sm block">{r.scheme_name}</span>
                              <span className="text-[11px] text-slate-500">Status: {r.eligibility_status || (r.is_eligible ? 'ELIGIBLE' : 'NOT_ELIGIBLE')}</span>
                            </div>
                            <div className="text-right">
                              <span className="text-lg font-black text-emerald-700">{r.match_score}%</span>
                              <span className="text-[10px] text-slate-400 block">Match Score</span>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}

                {/* TAB: TIMELINE & AUDIT */}
                {activeTab === 'timeline' && (
                  <div className="space-y-4 text-xs">
                    <h4 className="font-black text-slate-900 text-sm">Official Status Transition History</h4>
                    <div className="space-y-3 relative pl-6 before:absolute before:left-2.5 before:top-2 before:bottom-2 before:w-0.5 before:bg-slate-200">
                      {customerDetails.applications?.[0]?.status_history?.length > 0 ? (
                        customerDetails.applications[0].status_history.map((h, idx) => (
                          <div key={idx} className="relative space-y-1 bg-slate-50 p-3.5 rounded-xl border border-slate-100">
                            <span className="w-3 h-3 rounded-full bg-emerald-500 absolute -left-[19px] top-4 border-2 border-white" />
                            <div className="flex items-center justify-between">
                              <span className="font-black text-slate-900">{h.title}</span>
                              <span className="font-mono text-[10px] text-slate-400">
                                {h.timestamp ? new Date(h.timestamp).toLocaleString('en-IN') : ''}
                              </span>
                            </div>
                            <p className="text-slate-600">{h.description}</p>
                            <span className="text-[10px] font-bold text-indigo-700 block">
                              Updated By: {h.updated_by} ({h.actor_role || 'ADMIN'})
                            </span>
                          </div>
                        ))
                      ) : (
                        <div className="text-slate-400 italic">No status transition events logged yet.</div>
                      )}
                    </div>
                  </div>
                )}

              </div>
            ) : null}

          </div>
        </div>
      )}

    </div>
  );
}
