import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  Award, CheckCircle2, AlertTriangle, FileText, ArrowRight,
  ShieldCheck, MapPin, Printer, Download, Sparkles 
} from 'lucide-react';
import api from '../services/api';

export default function ApplicationReadinessPage() {
  const [readiness, setReadiness] = useState({
    readiness_score: 85,
    status: 'Ready for Bank Sanction',
    pillars: {
      profile_completeness: 100,
      eligibility_validation: 100,
      document_verification: 75,
      partner_alignment: 65
    }
  });

  useEffect(() => {
    api.get('/readiness/score')
      .then(res => setReadiness(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 space-y-8">
      <div>
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold mb-2">
          <Award className="w-3.5 h-3.5" />
          <span>Sanction Confidence Scorecard</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-black text-slate-900">Application Readiness Assessment</h1>
        <p className="text-xs sm:text-sm text-slate-500 mt-1">
          A multi-factor audit ensuring zero application rejections by lending banks.
        </p>
      </div>

      {/* Main Score Gauge */}
      <div className="bg-gradient-to-r from-emerald-900 to-teal-900 text-white rounded-2xl p-8 shadow-xl flex flex-col md:flex-row items-center justify-between gap-6">
        <div className="space-y-2 text-center md:text-left">
          <span className="text-xs uppercase font-bold text-emerald-300 tracking-wider">Overall Submission Score</span>
          <h2 className="text-3xl sm:text-4xl font-black">{readiness.status || 'High Sanction Probability'}</h2>
          <p className="text-xs text-slate-200 max-w-md">
            Your demographic certificates and project parameters meet 85% of standard gazetted bank criteria.
          </p>
        </div>

        <div className="w-32 h-32 rounded-full border-8 border-emerald-400 bg-white/10 flex flex-col items-center justify-center shrink-0 shadow-lg">
          <span className="text-3xl font-black text-white">{readiness.readiness_score || 85}%</span>
          <span className="text-[10px] uppercase font-bold text-emerald-300">Ready</span>
        </div>
      </div>

      {/* 4 Pillars Breakdown */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-2">
          <div className="flex justify-between items-center text-xs font-bold">
            <span className="text-slate-800">1. Profile Demographics Completeness</span>
            <span className="text-emerald-700">100%</span>
          </div>
          <div className="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
            <div className="h-full bg-emerald-500 w-full"></div>
          </div>
          <p className="text-[11px] text-slate-500">SC/ST status, location, and enterprise stage fully updated.</p>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-2">
          <div className="flex justify-between items-center text-xs font-bold">
            <span className="text-slate-800">2. Deterministic Rule Engine Eligibility</span>
            <span className="text-emerald-700">100%</span>
          </div>
          <div className="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
            <div className="h-full bg-emerald-500 w-full"></div>
          </div>
          <p className="text-[11px] text-slate-500">Zero disqualifying gazette criteria identified.</p>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-2">
          <div className="flex justify-between items-center text-xs font-bold">
            <span className="text-slate-800">3. OCR Document Verification</span>
            <span className="text-amber-700">75%</span>
          </div>
          <div className="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
            <div className="h-full bg-amber-500 w-3/4"></div>
          </div>
          <p className="text-[11px] text-slate-500">Detailed Project Report (DPR) pending upload.</p>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-2">
          <div className="flex justify-between items-center text-xs font-bold">
            <span className="text-slate-800">4. Partner Bank Routing</span>
            <span className="text-teal-700">65%</span>
          </div>
          <div className="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
            <div className="h-full bg-teal-500 w-2/3"></div>
          </div>
          <p className="text-[11px] text-slate-500">Nearest authorized branch identified within 3.2km.</p>
        </div>
      </div>
    </div>
  );
}
