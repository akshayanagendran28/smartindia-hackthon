import React, { useState, useEffect } from 'react';
import { 
  Building2, MapPin, Plus, Phone, Mail, Globe, 
  Search, Filter, Users, CheckCircle2, RefreshCw, 
  ChevronRight, ExternalLink, ShieldCheck, Eye, 
  Layers, CreditCard, Clock, X
} from 'lucide-react';
import api from '../../services/api';

export default function AdminPartnerManagement() {
  const [partners, setPartners] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [stateFilter, setStateFilter] = useState('');
  const [typeFilter, setTypeFilter] = useState('');
  
  // Assigned Applications Modal for a specific partner
  const [selectedPartner, setSelectedPartner] = useState(null);
  const [assignedApps, setAssignedApps] = useState([]);
  const [appsLoading, setAppsLoading] = useState(false);

  // Add Partner Modal
  const [showAddModal, setShowAddModal] = useState(false);
  const [partnerForm, setPartnerForm] = useState({
    name: '',
    partner_type: 'Lead District Bank',
    address: '',
    state: 'Maharashtra',
    district: 'Mumbai',
    pincode: '400001',
    latitude: 18.9220,
    longitude: 72.8347,
    contact_person: 'Senior Branch Manager',
    contact_phone: '+91 22 2266 1234',
    contact_email: 'leadbank.mumbai@gov.in',
    website: 'https://bankofindia.co.in',
    supported_scheme_codes: ['PMEGP', 'STANDUP-IND', 'SVANIDHI']
  });
  const [creating, setCreating] = useState(false);
  const [toast, setToast] = useState(null);

  const showToast = (msg, type = 'success') => {
    setToast({ msg, type });
    setTimeout(() => setToast(null), 4000);
  };

  const loadPartners = async () => {
    try {
      setLoading(true);
      const res = await api.get('/admin/partners');
      setPartners(res.data || []);
    } catch (err) {
      console.error('Failed to load partners:', err);
      showToast('Error loading partner directory.', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPartners();
  }, []);

  const openAssignedApplications = async (partner) => {
    try {
      setSelectedPartner(partner);
      setAppsLoading(true);
      const res = await api.get(`/admin/partners/${partner.id}/assigned-applications`);
      setAssignedApps(res.data.assigned_applications || []);
    } catch (err) {
      console.error('Failed to load assigned applications:', err);
      showToast('Error loading assigned applications.', 'error');
    } finally {
      setAppsLoading(false);
    }
  };

  const handleCreatePartner = async (e) => {
    e.preventDefault();
    try {
      setCreating(true);
      await api.post('/admin/partners', partnerForm);
      showToast(`Partner branch "${partnerForm.name}" created successfully!`);
      setShowAddModal(false);
      loadPartners();
    } catch (err) {
      console.error('Failed to create partner:', err);
      showToast('Failed to create partner.', 'error');
    } finally {
      setCreating(false);
    }
  };

  const filteredPartners = partners.filter((p) => {
    const matchesSearch = !search || p.name.toLowerCase().includes(search.toLowerCase()) || p.district.toLowerCase().includes(search.toLowerCase());
    const matchesState = !stateFilter || p.state === stateFilter;
    const matchesType = !typeFilter || p.partner_type === typeFilter;
    return matchesSearch && matchesState && matchesType;
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
            <span>Channel Partner Directory ({partners.length} Authorized Desks)</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-slate-900">Authorized Lending Institutions &amp; Bank Desks</h1>
          <p className="text-xs text-slate-500">Live directory of lead district banks, partner branches, and assigned beneficiary dossiers</p>
        </div>

        <div className="flex items-center gap-3">
          <button 
            onClick={loadPartners}
            className="px-3.5 py-2 bg-white border border-slate-200 hover:bg-slate-50 rounded-xl font-bold text-xs flex items-center gap-2 text-slate-700 shadow-sm cursor-pointer"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            <span>Refresh</span>
          </button>
          
          <button
            onClick={() => setShowAddModal(true)}
            className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-black text-xs rounded-xl shadow-lg shadow-emerald-600/20 flex items-center gap-1.5 transition-all cursor-pointer"
          >
            <Plus className="w-4 h-4 stroke-[3]" />
            <span>Add Partner Branch</span>
          </button>
        </div>
      </div>

      {/* Search & Filter Bar */}
      <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm flex flex-col md:flex-row items-center gap-4">
        <div className="relative flex-1 w-full">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
          <input 
            type="text"
            placeholder="Search by bank name, district, or address..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-10 pr-4 py-2 rounded-xl border border-slate-200 text-xs font-semibold bg-slate-50 focus:bg-white focus:ring-2 focus:ring-emerald-500 outline-none"
          />
        </div>

        <div className="flex items-center gap-3 w-full md:w-auto">
          <select
            value={stateFilter}
            onChange={(e) => setStateFilter(e.target.value)}
            className="p-2 rounded-xl border border-slate-200 text-xs font-semibold bg-slate-50 focus:bg-white outline-none"
          >
            <option value="">All States</option>
            <option value="Maharashtra">Maharashtra</option>
            <option value="Delhi">Delhi</option>
            <option value="Tamil Nadu">Tamil Nadu</option>
            <option value="Karnataka">Karnataka</option>
            <option value="Uttar Pradesh">Uttar Pradesh</option>
          </select>

          <select
            value={typeFilter}
            onChange={(e) => setTypeFilter(e.target.value)}
            className="p-2 rounded-xl border border-slate-200 text-xs font-semibold bg-slate-50 focus:bg-white outline-none"
          >
            <option value="">All Institution Types</option>
            <option value="Lead District Bank">Lead District Bank</option>
            <option value="Public Sector Bank">Public Sector Bank</option>
            <option value="CSC / Seva Kendra">CSC / Seva Kendra</option>
            <option value="State Financial Corporation">State Financial Corp</option>
          </select>
        </div>
      </div>

      {/* Partners Cards Grid */}
      {loading ? (
        <div className="p-16 text-center text-slate-400 text-xs flex flex-col items-center justify-center gap-3">
          <RefreshCw className="w-6 h-6 animate-spin text-emerald-600" />
          <span>Loading authorized partner network from database...</span>
        </div>
      ) : filteredPartners.length === 0 ? (
        <div className="p-12 text-center bg-white rounded-3xl border border-slate-200 text-slate-500 text-xs">
          No partner branches found matching your filter criteria.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredPartners.map((partner) => (
            <div 
              key={partner.id}
              className="bg-white rounded-3xl p-5 border border-slate-200 shadow-sm hover:border-emerald-300 hover:shadow-md transition-all space-y-4 flex flex-col justify-between"
            >
              <div className="space-y-3">
                
                {/* Card Header */}
                <div className="flex items-start justify-between gap-3">
                  <div className="space-y-1">
                    <span className="px-2.5 py-0.5 rounded-full text-[10px] font-black uppercase tracking-wider bg-indigo-50 text-indigo-800 border border-indigo-100">
                      {partner.partner_type}
                    </span>
                    <h3 className="font-black text-slate-900 text-base leading-snug">
                      {partner.name}
                    </h3>
                  </div>

                  <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                    partner.is_active ? 'bg-emerald-100 text-emerald-800' : 'bg-slate-200 text-slate-600'
                  }`}>
                    {partner.is_active ? '● Active' : '○ Inactive'}
                  </span>
                </div>

                {/* Location & Contact */}
                <div className="space-y-1.5 text-xs text-slate-600">
                  <p className="flex items-start gap-1.5">
                    <MapPin className="w-3.5 h-3.5 text-slate-400 shrink-0 mt-0.5" />
                    <span>{partner.address}, {partner.district}, {partner.state}</span>
                  </p>
                  {partner.contact_phone && (
                    <p className="flex items-center gap-1.5 font-mono text-[11px]">
                      <Phone className="w-3.5 h-3.5 text-slate-400" />
                      <span>{partner.contact_phone}</span>
                    </p>
                  )}
                </div>

                {/* Real Metrics Gauge (Assigned, Pending, Processing) */}
                <div className="grid grid-cols-3 gap-2 p-3 rounded-2xl bg-slate-50 border border-slate-100 text-center">
                  <div>
                    <span className="text-[10px] font-bold text-slate-400 block uppercase">Assigned</span>
                    <span className="font-black text-emerald-700 text-base">{partner.assigned_customers_count}</span>
                  </div>
                  <div>
                    <span className="text-[10px] font-bold text-slate-400 block uppercase">Pending Inv</span>
                    <span className="font-black text-amber-700 text-base">{partner.pending_invitations_count}</span>
                  </div>
                  <div>
                    <span className="text-[10px] font-bold text-slate-400 block uppercase">In Review</span>
                    <span className="font-black text-indigo-700 text-base">{partner.processing_applications_count}</span>
                  </div>
                </div>

                {/* Supported Scheme Codes */}
                <div className="flex flex-wrap items-center gap-1.5 pt-1">
                  {partner.supported_scheme_codes?.map((code, idx) => (
                    <span key={idx} className="font-mono text-[10px] font-bold px-2 py-0.5 rounded bg-slate-100 text-slate-700">
                      {code}
                    </span>
                  ))}
                </div>

              </div>

              {/* Action Button */}
              <div className="pt-3 border-t border-slate-100 flex items-center justify-between">
                <span className="text-[10px] font-semibold text-slate-400">
                  Geo: {partner.latitude?.toFixed(2)}, {partner.longitude?.toFixed(2)}
                </span>
                
                <button
                  onClick={() => openAssignedApplications(partner)}
                  className="px-3.5 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs flex items-center gap-1.5 shadow-sm transition-all cursor-pointer"
                >
                  <Eye className="w-3.5 h-3.5" />
                  <span>View Customers ({partner.assigned_customers_count})</span>
                </button>
              </div>

            </div>
          ))}
        </div>
      )}

      {/* ASSIGNED APPLICATIONS MODAL */}
      {selectedPartner && (
        <div className="fixed inset-0 z-50 bg-slate-900/70 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto">
          <div className="bg-white rounded-3xl max-w-4xl w-full p-6 sm:p-8 shadow-2xl border border-slate-100 space-y-6 my-6 max-h-[90vh] overflow-y-auto animate-in fade-in zoom-in-95">
            
            <div className="flex items-center justify-between pb-4 border-b border-slate-100">
              <div>
                <div className="flex items-center gap-2">
                  <Landmark className="w-5 h-5 text-emerald-600" />
                  <h3 className="font-black text-slate-900 text-lg">{selectedPartner.name}</h3>
                </div>
                <p className="text-xs text-slate-500">
                  Assigned Citizen Dossiers &bull; {selectedPartner.district}, {selectedPartner.state}
                </p>
              </div>

              <button
                onClick={() => setSelectedPartner(null)}
                className="p-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-600 font-black text-sm cursor-pointer"
              >
                ✕
              </button>
            </div>

            {appsLoading ? (
              <div className="p-12 text-center text-slate-400 text-xs flex flex-col items-center justify-center gap-3">
                <RefreshCw className="w-6 h-6 animate-spin text-emerald-600" />
                <span>Loading assigned applications from database...</span>
              </div>
            ) : assignedApps.length === 0 ? (
              <div className="p-12 text-center bg-slate-50 rounded-2xl border border-slate-200 text-slate-500 text-xs">
                No customer applications currently assigned to this branch desk.
              </div>
            ) : (
              <div className="divide-y divide-slate-100 border border-slate-200 rounded-2xl overflow-hidden text-xs">
                {assignedApps.map((app) => (
                  <div key={app.id} className="p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3 hover:bg-slate-50">
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <span className="font-mono text-xs font-black text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                          {app.application_number}
                        </span>
                        <span className="font-bold text-slate-900">{app.customer_name}</span>
                        <span className="text-slate-500 text-[11px]">({app.customer_email})</span>
                      </div>
                      <p className="text-slate-600 text-xs">
                        Scheme: <strong>{app.scheme_name}</strong> &bull; Amount: <strong>₹{(app.loan_amount || 0).toLocaleString('en-IN')}</strong>
                      </p>
                    </div>

                    <div className="flex items-center gap-2 shrink-0">
                      <span className="px-2.5 py-1 rounded-full text-[10px] font-black uppercase bg-indigo-50 text-indigo-800 border border-indigo-100">
                        Loan: {app.loan_status}
                      </span>
                      <span className="px-2.5 py-1 rounded-full text-[10px] font-black uppercase bg-emerald-50 text-emerald-800 border border-emerald-100">
                        Fund: {app.fund_status}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}

          </div>
        </div>
      )}

      {/* ADD CHANNEL PARTNER MODAL */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 bg-slate-900/70 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto">
          <div className="bg-white rounded-3xl max-w-2xl w-full p-6 sm:p-8 shadow-2xl border border-slate-100 space-y-6 my-6 animate-in fade-in zoom-in-95">
            
            <div className="flex items-center justify-between pb-4 border-b border-slate-100">
              <div className="flex items-center gap-2.5">
                <div className="p-2 rounded-xl bg-emerald-100 text-emerald-800">
                  <Building2 className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="font-black text-slate-900 text-lg">Register Authorized Partner Branch</h3>
                  <p className="text-xs text-slate-500">Add a new lending desk or branch to the Scheme Sathi network</p>
                </div>
              </div>

              <button
                onClick={() => setShowAddModal(false)}
                className="text-slate-400 hover:text-slate-700 font-bold p-1 rounded-lg"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleCreatePartner} className="space-y-4 text-xs">
              <div>
                <label className="font-bold text-slate-700 block mb-1">Partner Branch Name</label>
                <input
                  type="text"
                  placeholder="e.g. State Bank of India - Connaught Place Lead Branch"
                  value={partnerForm.name}
                  onChange={(e) => setPartnerForm({ ...partnerForm, name: e.target.value })}
                  className="w-full p-2.5 rounded-xl border border-slate-200 font-semibold bg-slate-50 focus:bg-white outline-none focus:ring-2 focus:ring-emerald-500"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="font-bold text-slate-700 block mb-1">Institution Type</label>
                  <select
                    value={partnerForm.partner_type}
                    onChange={(e) => setPartnerForm({ ...partnerForm, partner_type: e.target.value })}
                    className="w-full p-2.5 rounded-xl border border-slate-200 font-semibold bg-slate-50 focus:bg-white outline-none focus:ring-2 focus:ring-emerald-500"
                  >
                    <option value="Lead District Bank">Lead District Bank</option>
                    <option value="Public Sector Bank">Public Sector Bank</option>
                    <option value="CSC / Seva Kendra">CSC / Seva Kendra</option>
                    <option value="State Financial Corporation">State Financial Corporation</option>
                  </select>
                </div>

                <div>
                  <label className="font-bold text-slate-700 block mb-1">State</label>
                  <input
                    type="text"
                    value={partnerForm.state}
                    onChange={(e) => setPartnerForm({ ...partnerForm, state: e.target.value })}
                    className="w-full p-2.5 rounded-xl border border-slate-200 font-semibold bg-slate-50 focus:bg-white outline-none focus:ring-2 focus:ring-emerald-500"
                    required
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="font-bold text-slate-700 block mb-1">District</label>
                  <input
                    type="text"
                    value={partnerForm.district}
                    onChange={(e) => setPartnerForm({ ...partnerForm, district: e.target.value })}
                    className="w-full p-2.5 rounded-xl border border-slate-200 font-semibold bg-slate-50 focus:bg-white outline-none focus:ring-2 focus:ring-emerald-500"
                    required
                  />
                </div>

                <div>
                  <label className="font-bold text-slate-700 block mb-1">Pincode</label>
                  <input
                    type="text"
                    value={partnerForm.pincode}
                    onChange={(e) => setPartnerForm({ ...partnerForm, pincode: e.target.value })}
                    className="w-full p-2.5 rounded-xl border border-slate-200 font-semibold bg-slate-50 focus:bg-white outline-none focus:ring-2 focus:ring-emerald-500"
                  />
                </div>
              </div>

              <div>
                <label className="font-bold text-slate-700 block mb-1">Full Branch Address</label>
                <input
                  type="text"
                  value={partnerForm.address}
                  onChange={(e) => setPartnerForm({ ...partnerForm, address: e.target.value })}
                  className="w-full p-2.5 rounded-xl border border-slate-200 font-medium bg-slate-50 focus:bg-white outline-none focus:ring-2 focus:ring-emerald-500"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="font-bold text-slate-700 block mb-1">Contact Phone</label>
                  <input
                    type="text"
                    value={partnerForm.contact_phone}
                    onChange={(e) => setPartnerForm({ ...partnerForm, contact_phone: e.target.value })}
                    className="w-full p-2.5 rounded-xl border border-slate-200 font-semibold bg-slate-50 focus:bg-white outline-none focus:ring-2 focus:ring-emerald-500"
                  />
                </div>

                <div>
                  <label className="font-bold text-slate-700 block mb-1">Contact Email</label>
                  <input
                    type="email"
                    value={partnerForm.contact_email}
                    onChange={(e) => setPartnerForm({ ...partnerForm, contact_email: e.target.value })}
                    className="w-full p-2.5 rounded-xl border border-slate-200 font-semibold bg-slate-50 focus:bg-white outline-none focus:ring-2 focus:ring-emerald-500"
                  />
                </div>
              </div>

              <div className="flex justify-end gap-3 pt-4 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-4 py-2 rounded-xl text-slate-600 font-bold hover:bg-slate-100"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={creating}
                  className="px-5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-black shadow-lg shadow-emerald-600/20"
                >
                  {creating ? 'Registering...' : 'Save Partner Branch'}
                </button>
              </div>

            </form>
          </div>
        </div>
      )}

    </div>
  );
}
