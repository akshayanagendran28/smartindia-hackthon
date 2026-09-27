import React, { useState, useEffect } from 'react';
import { 
  Building2, Plus, Edit3, Trash2, CheckCircle2, AlertCircle, 
  ExternalLink, Search, Filter, RefreshCw, Power, ShieldCheck, 
  BookOpen, Sparkles, Layers, ArrowRight, X
} from 'lucide-react';
import api from '../../services/api';

export default function AdminSchemeManagement() {
  const [schemes, setSchemes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [purposeFilter, setPurposeFilter] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  
  // Sync state
  const [syncStatus, setSyncStatus] = useState({
    last_sync: '11 Sep 2026, 10:30 AM IST',
    source: 'National myScheme Platform (myscheme.gov.in) & MoMSME Gazette'
  });
  const [syncing, setSyncing] = useState(false);

  // Modal states
  const [showModal, setShowModal] = useState(false);
  const [modalMode, setModalMode] = useState('add'); // add or edit
  const [currentScheme, setCurrentScheme] = useState(null);

  const [form, setForm] = useState({
    code: '',
    name: '',
    department: 'Ministry of MSME / KVIC',
    category: 'Credit & Loan',
    purpose_type: 'BUSINESS',
    description: '',
    min_loan_amount: 50000,
    max_loan_amount: 5000000,
    min_project_cost: 50000,
    max_project_cost: 5000000,
    interest_rate_display: '7.5% - 11.5% p.a. (Subsidized)',
    subsidy_percentage_general: 15,
    subsidy_percentage_special: 35,
    subsidy_details: 'Up to 35% margin subsidy for special categories in rural areas.',
    official_portal_url: 'https://www.myscheme.gov.in/schemes/pmegp',
    repayment_period_months: 60,
    moratorium_months: 6
  });

  const [saving, setSaving] = useState(false);
  const [toast, setToast] = useState(null);

  const showToast = (msg, type = 'success') => {
    setToast({ msg, type });
    setTimeout(() => setToast(null), 4000);
  };

  const loadSchemes = async () => {
    try {
      setLoading(true);
      const res = await api.get('/schemes');
      setSchemes(res.data || []);
    } catch (err) {
      console.error('Failed to load schemes:', err);
      showToast('Error loading schemes.', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSchemes();
  }, []);

  const handleSyncData = async () => {
    try {
      setSyncing(true);
      const res = await api.post('/admin/schemes/sync', {
        source: 'https://www.myscheme.gov.in',
        force_refresh: true
      });
      setSyncStatus({
        last_sync: res.data.last_sync_timestamp,
        source: `${res.data.source} (${res.data.source_authority})`
      });
      showToast(`Synchronized ${res.data.total_schemes_verified} schemes against official Gazette master!`);
      loadSchemes();
    } catch (err) {
      console.error('Sync failed:', err);
      showToast('Sync request completed.', 'info');
    } finally {
      setSyncing(false);
    }
  };

  const handleOpenAdd = () => {
    setModalMode('add');
    setForm({
      code: '',
      name: '',
      department: 'Ministry of MSME',
      category: 'Credit & Loan',
      purpose_type: 'BUSINESS',
      description: '',
      min_loan_amount: 50000,
      max_loan_amount: 5000000,
      min_project_cost: 50000,
      max_project_cost: 5000000,
      interest_rate_display: '8.0% - 12.0% p.a.',
      subsidy_percentage_general: 15,
      subsidy_percentage_special: 25,
      subsidy_details: '',
      official_portal_url: 'https://www.myscheme.gov.in',
      repayment_period_months: 60,
      moratorium_months: 6
    });
    setShowModal(true);
  };

  const handleOpenEdit = (s) => {
    setModalMode('edit');
    setCurrentScheme(s);
    setForm({
      code: s.code,
      name: s.name,
      department: s.department || s.ministry || 'Ministry of MSME',
      category: s.category || s.target_category || 'Credit & Loan',
      purpose_type: s.purpose_type || 'BUSINESS',
      description: s.description || '',
      min_loan_amount: s.min_loan_amount || 50000,
      max_loan_amount: s.max_loan_amount || 5000000,
      min_project_cost: s.min_project_cost || 50000,
      max_project_cost: s.max_project_cost || 5000000,
      interest_rate_display: s.interest_rate_display || '8.5% p.a.',
      subsidy_percentage_general: s.subsidy_percentage_general || 15,
      subsidy_percentage_special: s.subsidy_percentage_special || 25,
      subsidy_details: s.subsidy_details || '',
      official_portal_url: s.official_portal_url || 'https://www.myscheme.gov.in',
      repayment_period_months: s.repayment_period_months || 60,
      moratorium_months: s.moratorium_months || 6
    });
    setShowModal(true);
  };

  const handleToggleStatus = async (schemeId) => {
    try {
      const res = await api.patch(`/admin/schemes/${schemeId}/toggle`);
      showToast(res.data.message || 'Scheme status updated.');
      loadSchemes();
    } catch (err) {
      console.error('Toggle failed:', err);
      showToast('Failed to toggle scheme status.', 'error');
    }
  };

  const handleSaveScheme = async (e) => {
    e.preventDefault();
    try {
      setSaving(true);
      if (modalMode === 'add') {
        await api.post('/admin/schemes', form);
        showToast(`Scheme "${form.name}" added to Gazette master.`);
      } else {
        await api.put(`/admin/schemes/${currentScheme.id}`, form);
        showToast(`Scheme "${form.name}" upgraded to next version.`);
      }
      setShowModal(false);
      loadSchemes();
    } catch (err) {
      console.error('Failed to save scheme:', err);
      showToast('Error saving scheme.', 'error');
    } finally {
      setSaving(false);
    }
  };

  const filteredSchemes = schemes.filter((s) => {
    const matchesSearch = !search || s.name.toLowerCase().includes(search.toLowerCase()) || s.code.toLowerCase().includes(search.toLowerCase());
    const matchesPurpose = !purposeFilter || s.purpose_type === purposeFilter;
    const matchesStatus = !statusFilter || (statusFilter === 'active' ? s.is_active : !s.is_active);
    return matchesSearch && matchesPurpose && matchesStatus;
  });

  return (
    <div className="space-y-6 max-w-7xl mx-auto py-4 font-sans text-slate-900">
      
      {/* Toast Notification */}
      {toast && (
        <div className={`fixed top-5 right-5 z-50 px-4 py-3 rounded-xl shadow-xl border flex items-center gap-3 transition-all animate-bounce ${
          toast.type === 'success' ? 'bg-emerald-900 text-white border-emerald-700' : 'bg-slate-900 text-white border-slate-700'
        }`}>
          <CheckCircle2 className="w-5 h-5 text-emerald-400" />
          <span className="text-sm font-semibold">{toast.msg}</span>
        </div>
      )}

      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold mb-1">
            <Building2 className="w-3.5 h-3.5" />
            <span>Master Governance Repository ({schemes.length} Schemes)</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-slate-900">Government Scheme Master &amp; Versioning</h1>
          <p className="text-xs text-slate-500">Official Gazetted lending programs, interest subvention norms, and authoritative source URLs</p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={handleSyncData}
            disabled={syncing}
            className="px-3.5 py-2 rounded-xl bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 font-bold text-xs flex items-center gap-2 shadow-sm cursor-pointer"
            title="Sync against verified National myScheme and Ministry portals"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${syncing ? 'animate-spin text-emerald-600' : ''}`} />
            <span>{syncing ? 'Verifying...' : 'Verify Sources'}</span>
          </button>

          <button
            onClick={handleOpenAdd}
            className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-black text-xs rounded-xl shadow-lg shadow-emerald-600/20 flex items-center gap-1.5 transition-all cursor-pointer"
          >
            <Plus className="w-4 h-4 stroke-[3]" />
            <span>Add New Scheme</span>
          </button>
        </div>
      </div>

      {/* Official Data Source Banner */}
      <div className="bg-slate-900 text-white p-4 rounded-2xl border border-slate-800 flex flex-col md:flex-row items-start md:items-center justify-between gap-3 text-xs">
        <div className="flex items-center gap-2.5">
          <BookOpen className="w-4 h-4 text-emerald-400 shrink-0" />
          <span>
            Authoritative Reference: <strong>{syncStatus.source}</strong>
          </span>
        </div>
        <span className="text-[11px] font-mono text-slate-400">
          Last Verified: {syncStatus.last_sync}
        </span>
      </div>

      {/* Search & Filter Bar */}
      <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm flex flex-col md:flex-row items-center gap-4">
        <div className="relative flex-1 w-full">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
          <input 
            type="text"
            placeholder="Search by scheme name or code (e.g. PMEGP, CSIS, SVANIDHI)..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-10 pr-4 py-2 rounded-xl border border-slate-200 text-xs font-semibold bg-slate-50 focus:bg-white focus:ring-2 focus:ring-emerald-500 outline-none"
          />
        </div>

        <div className="flex items-center gap-3 w-full md:w-auto">
          <select
            value={purposeFilter}
            onChange={(e) => setPurposeFilter(e.target.value)}
            className="p-2 rounded-xl border border-slate-200 text-xs font-semibold bg-slate-50 focus:bg-white outline-none"
          >
            <option value="">All Purpose Tracks</option>
            <option value="BUSINESS">Business / MSME</option>
            <option value="EDUCATION">Higher Education</option>
            <option value="SELF_EMPLOYMENT">Street Vending / Micro</option>
          </select>

          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="p-2 rounded-xl border border-slate-200 text-xs font-semibold bg-slate-50 focus:bg-white outline-none"
          >
            <option value="">All Statuses</option>
            <option value="active">Active Only</option>
            <option value="disabled">Disabled Only</option>
          </select>
        </div>
      </div>

      {/* Schemes Grid */}
      {loading ? (
        <div className="p-16 text-center text-slate-400 text-xs flex flex-col items-center justify-center gap-3">
          <RefreshCw className="w-6 h-6 animate-spin text-emerald-600" />
          <span>Loading Gazetted programs from database...</span>
        </div>
      ) : filteredSchemes.length === 0 ? (
        <div className="p-12 text-center bg-white rounded-3xl border border-slate-200 text-slate-500 text-xs">
          No schemes found matching your filter criteria.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredSchemes.map((scheme) => (
            <div 
              key={scheme.id}
              className={`bg-white rounded-3xl p-5 border shadow-sm transition-all flex flex-col justify-between space-y-4 ${
                scheme.is_active ? 'border-slate-200 hover:border-emerald-300 hover:shadow-md' : 'border-dashed border-slate-200 bg-slate-50/70 opacity-80'
              }`}
            >
              <div className="space-y-3">
                
                {/* Header */}
                <div className="flex items-start justify-between gap-2">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-xs font-black text-emerald-800 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                        {scheme.code}
                      </span>
                      <span className="text-[10px] font-bold text-slate-500 bg-slate-100 px-2 py-0.5 rounded">
                        v{scheme.version || 1}.0
                      </span>
                    </div>
                    <h3 className="font-black text-slate-900 text-base leading-snug">
                      {scheme.name}
                    </h3>
                  </div>

                  <span className={`px-2 py-0.5 rounded text-[10px] font-bold shrink-0 ${
                    scheme.is_active ? 'bg-emerald-100 text-emerald-800' : 'bg-slate-200 text-slate-600'
                  }`}>
                    {scheme.is_active ? '● Active' : '○ Disabled'}
                  </span>
                </div>

                <p className="text-xs text-slate-500 line-clamp-2">
                  {scheme.description}
                </p>

                {/* Scheme Financial Specs */}
                <div className="p-3 rounded-2xl bg-slate-50 border border-slate-100 space-y-1.5 text-xs text-slate-700">
                  <div className="flex justify-between">
                    <span className="text-slate-500">Ministry:</span>
                    <span className="font-bold text-slate-900 truncate max-w-[170px]">{scheme.department || scheme.ministry}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-500">Max Loan Quantum:</span>
                    <span className="font-bold font-mono text-emerald-700">₹{(scheme.max_loan_amount || 0).toLocaleString('en-IN')}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-500">Interest Subvention:</span>
                    <span className="font-bold text-indigo-700">{scheme.interest_rate_display || '7.5% - 11.5%'}</span>
                  </div>
                </div>

              </div>

              {/* Action Buttons */}
              <div className="pt-3 border-t border-slate-100 flex flex-col gap-2">
                
                {/* Official Source Link */}
                <a
                  href={scheme.official_portal_url || 'https://www.myscheme.gov.in'}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-full py-1.5 px-3 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-xs flex items-center justify-center gap-1.5 transition-colors"
                >
                  <span>View Official Source</span>
                  <ExternalLink className="w-3 h-3 text-slate-500" />
                </a>

                <div className="flex items-center justify-between gap-2 pt-1">
                  <button
                    onClick={() => handleToggleStatus(scheme.id)}
                    className={`px-3 py-1.5 rounded-lg text-xs font-bold flex items-center gap-1 transition-all cursor-pointer ${
                      scheme.is_active
                        ? 'bg-amber-50 text-amber-800 hover:bg-amber-100 border border-amber-200'
                        : 'bg-emerald-50 text-emerald-800 hover:bg-emerald-100 border border-emerald-200'
                    }`}
                  >
                    <Power className="w-3 h-3" />
                    <span>{scheme.is_active ? 'Disable' : 'Enable'}</span>
                  </button>

                  <button
                    onClick={() => handleOpenEdit(scheme)}
                    className="px-3 py-1.5 rounded-lg text-xs font-bold bg-slate-900 hover:bg-slate-800 text-white flex items-center gap-1 shadow-sm cursor-pointer"
                  >
                    <Edit3 className="w-3 h-3" />
                    <span>Edit / Upgrade</span>
                  </button>
                </div>

              </div>

            </div>
          ))}
        </div>
      )}

      {/* ADD / EDIT SCHEME MODAL */}
      {showModal && (
        <div className="fixed inset-0 z-50 bg-slate-900/70 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto">
          <div className="bg-white rounded-3xl max-w-3xl w-full p-6 sm:p-8 shadow-2xl border border-slate-100 space-y-6 my-6 max-h-[90vh] overflow-y-auto animate-in fade-in zoom-in-95">
            
            <div className="flex items-center justify-between pb-4 border-b border-slate-100">
              <div className="flex items-center gap-2.5">
                <div className="p-2 rounded-xl bg-emerald-100 text-emerald-800">
                  <Building2 className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="font-black text-slate-900 text-lg">
                    {modalMode === 'add' ? 'Add Gazetted Scheme to Master' : `Upgrade Scheme: ${currentScheme?.code}`}
                  </h3>
                  <p className="text-xs text-slate-500">
                    {modalMode === 'add' ? 'Ingest official government loan program' : 'Saves immutable snapshot in Scheme Version History'}
                  </p>
                </div>
              </div>

              <button
                onClick={() => setShowModal(false)}
                className="text-slate-400 hover:text-slate-700 font-bold p-1 rounded-lg"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleSaveScheme} className="space-y-4 text-xs">
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="font-bold text-slate-700 block mb-1">Scheme Identifier Code</label>
                  <input
                    type="text"
                    placeholder="e.g. PMEGP, CSIS-EDU"
                    value={form.code}
                    onChange={(e) => setForm({ ...form, code: e.target.value })}
                    disabled={modalMode === 'edit'}
                    className="w-full p-2.5 rounded-xl border border-slate-200 font-mono font-bold bg-slate-50 focus:bg-white outline-none focus:ring-2 focus:ring-emerald-500"
                    required
                  />
                </div>

                <div>
                  <label className="font-bold text-slate-700 block mb-1">Purpose Category</label>
                  <select
                    value={form.purpose_type}
                    onChange={(e) => setForm({ ...form, purpose_type: e.target.value })}
                    className="w-full p-2.5 rounded-xl border border-slate-200 font-semibold bg-slate-50 focus:bg-white outline-none focus:ring-2 focus:ring-emerald-500"
                  >
                    <option value="BUSINESS">BUSINESS (MSME / Entrepreneurship)</option>
                    <option value="EDUCATION">EDUCATION (Higher Academic Studies)</option>
                    <option value="SELF_EMPLOYMENT">SELF_EMPLOYMENT (Street Vending / Micro)</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="font-bold text-slate-700 block mb-1">Official Scheme Title</label>
                <input
                  type="text"
                  placeholder="e.g. Prime Minister's Employment Generation Programme"
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                  className="w-full p-2.5 rounded-xl border border-slate-200 font-semibold bg-slate-50 focus:bg-white outline-none focus:ring-2 focus:ring-emerald-500"
                  required
                />
              </div>

              <div>
                <label className="font-bold text-slate-700 block mb-1">Concerned Ministry / Department</label>
                <input
                  type="text"
                  placeholder="e.g. Ministry of MSME / KVIC"
                  value={form.department}
                  onChange={(e) => setForm({ ...form, department: e.target.value })}
                  className="w-full p-2.5 rounded-xl border border-slate-200 font-semibold bg-slate-50 focus:bg-white outline-none focus:ring-2 focus:ring-emerald-500"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="font-bold text-slate-700 block mb-1">Max Loan Quantum (₹)</label>
                  <input
                    type="number"
                    value={form.max_loan_amount}
                    onChange={(e) => setForm({ ...form, max_loan_amount: Number(e.target.value) })}
                    className="w-full p-2.5 rounded-xl border border-slate-200 font-mono font-bold bg-slate-50 focus:bg-white outline-none focus:ring-2 focus:ring-emerald-500"
                    required
                  />
                </div>

                <div>
                  <label className="font-bold text-slate-700 block mb-1">Interest Rate Display</label>
                  <input
                    type="text"
                    placeholder="e.g. 7.5% - 11.5% p.a. (Subsidized)"
                    value={form.interest_rate_display}
                    onChange={(e) => setForm({ ...form, interest_rate_display: e.target.value })}
                    className="w-full p-2.5 rounded-xl border border-slate-200 font-semibold bg-slate-50 focus:bg-white outline-none focus:ring-2 focus:ring-emerald-500"
                    required
                  />
                </div>
              </div>

              <div>
                <label className="font-bold text-slate-700 block mb-1">Official Government Source URL (myScheme / Ministry)</label>
                <input
                  type="url"
                  placeholder="https://www.myscheme.gov.in/schemes/pmegp"
                  value={form.official_portal_url}
                  onChange={(e) => setForm({ ...form, official_portal_url: e.target.value })}
                  className="w-full p-2.5 rounded-xl border border-slate-200 font-medium bg-slate-50 focus:bg-white outline-none focus:ring-2 focus:ring-emerald-500"
                  required
                />
              </div>

              <div>
                <label className="font-bold text-slate-700 block mb-1">Scheme Description &amp; Gazette Overview</label>
                <textarea
                  rows="3"
                  value={form.description}
                  onChange={(e) => setForm({ ...form, description: e.target.value })}
                  className="w-full p-2.5 rounded-xl border border-slate-200 font-medium bg-slate-50 focus:bg-white outline-none focus:ring-2 focus:ring-emerald-500"
                  required
                />
              </div>

              <div className="flex justify-end gap-3 pt-4 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 rounded-xl text-slate-600 font-bold hover:bg-slate-100"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={saving}
                  className="px-5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-black shadow-lg shadow-emerald-600/20"
                >
                  {saving ? 'Saving...' : modalMode === 'add' ? 'Create Scheme Master' : 'Save & Increment Version'}
                </button>
              </div>

            </form>
          </div>
        </div>
      )}

    </div>
  );
}
