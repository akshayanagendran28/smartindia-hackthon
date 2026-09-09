import React from 'react';
import { History, Award, CheckCircle2, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function HistoryPage() {
  return (
    <div className="max-w-4xl mx-auto py-8 px-4 space-y-6">
      <div className="flex items-center gap-3">
        <div className="p-2.5 bg-emerald-100 text-emerald-800 rounded-xl">
          <History className="w-5 h-5" />
        </div>
        <div>
          <h1 className="text-2xl font-black text-slate-900">Eligibility Evaluation History</h1>
          <p className="text-xs text-slate-500">Past scheme matching sessions and calculated loan plans</p>
        </div>
      </div>

      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
        <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-between">
          <div>
            <span className="text-[10px] font-bold text-slate-400 uppercase">Evaluated on Sept 7, 2026</span>
            <h3 className="font-bold text-slate-900 text-sm">Manufacturing Enterprise (₹15 Lakh Project)</h3>
            <span className="text-xs text-emerald-700 font-semibold">Matched: PMEGP (35% Subsidy), Mudra Tarun</span>
          </div>
          <Link to="/results" className="px-3 py-1.5 bg-emerald-600 text-white text-xs font-bold rounded-lg">
            View Results
          </Link>
        </div>
      </div>
    </div>
  );
}
