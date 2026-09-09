import React from 'react';
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
