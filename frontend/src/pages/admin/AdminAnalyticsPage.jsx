import React from 'react';
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
