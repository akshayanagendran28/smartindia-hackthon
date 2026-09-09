import React, { useState, useEffect } from 'react';
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
