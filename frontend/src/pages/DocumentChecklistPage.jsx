import React from 'react';
import { Link } from 'react-router-dom';
import { FileCheck, CheckCircle2, AlertCircle, ArrowRight, Printer, Download } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

export default function DocumentChecklistPage() {
  const { t } = useLanguage();
  const documents = [
    { name: t('docAadhaar'), status: 'Verified', mandatory: true, desc: 'Identity & Address proof with mobile OTP linkage' },
    { name: t('docPan'), status: 'Verified', mandatory: true, desc: 'Tax identification required for bank loan sanction' },
    { name: t('docCaste'), status: 'Verified', mandatory: true, desc: 'Required for 35% Special Category Subsidy' },
    { name: t('docDpr'), status: 'Pending', mandatory: true, desc: 'Project cost breakdown, machinery list & revenue model' },
    { name: t('docBank'), status: 'Verified', mandatory: true, desc: 'Financial transaction proof' },
    { name: t('docEdp'), status: 'Optional', mandatory: false, desc: 'Adds +15% matching preference' },
    { name: t('docUdyam'), status: 'Verified', mandatory: false, desc: 'Government MSME recognition' }
  ];

  return (
    <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold mb-2">
            <FileCheck className="w-3.5 h-3.5" />
            <span>{t('sihBadgeText')} • {t('translationBadge')}</span>
          </div>
          <h1 className="text-2xl font-black text-slate-900">{t('docChecklistTitle')}</h1>
          <p className="text-xs text-slate-500 mt-1">{t('docChecklistSubtitle')}</p>
        </div>

        <div className="flex gap-2">
          <button
            onClick={() => window.print()}
            className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-xs rounded-xl flex items-center gap-1.5"
          >
            <Printer className="w-3.5 h-3.5" />
            <span>{t('btnPrintChecklist')}</span>
          </button>
        </div>
      </div>

      <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
        <div className="divide-y divide-slate-100">
          {documents.map((doc, idx) => (
            <div key={idx} className="p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-3 hover:bg-slate-50/50">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="font-bold text-slate-900 text-sm">{doc.name}</span>
                  {doc.mandatory && <span className="text-[10px] font-bold text-red-600 bg-red-50 px-2 py-0.5 rounded">{t('mandatoryTag')}</span>}
                </div>
                <p className="text-xs text-slate-500">{doc.desc}</p>
              </div>

              <div className="flex items-center gap-3">
                <span className={`px-3 py-1 rounded-full text-xs font-bold flex items-center gap-1 ${doc.status === 'Verified' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'}`}>
                  {doc.status === 'Verified' ? <CheckCircle2 className="w-3.5 h-3.5" /> : <AlertCircle className="w-3.5 h-3.5" />}
                  <span>{doc.status}</span>
                </span>
                <Link
                  to="/documents"
                  className="px-3 py-1.5 bg-slate-100 hover:bg-emerald-50 hover:text-emerald-700 text-slate-700 text-xs font-semibold rounded-lg"
                >
                  {t('navDocAssistant')}
                </Link>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
