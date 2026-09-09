import React, { useState, useEffect } from 'react';
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
