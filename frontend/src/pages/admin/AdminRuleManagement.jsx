import React, { useState } from 'react';
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
