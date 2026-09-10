import React from 'react';
import { Bell, Award, FileCheck, CheckCircle2, Clock } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

export default function NotificationsPage() {
  const { t } = useLanguage();
  const notifications = [
    { title: t('New Subsidy Slab Announced for PMEGP', 'New Subsidy Slab Announced for PMEGP'), desc: t('Rural special category subsidy increased to 35% with ₹50 Lakh project ceiling.', 'Rural special category subsidy increased to 35% with ₹50 Lakh project ceiling.'), time: '2 hours ago', type: 'subsidy' },
    { title: t('Aadhaar OCR Verification Successful', 'Aadhaar OCR Verification Successful'), desc: t('UIDAI card cross-verified with 100% name and demographic match.', 'UIDAI card cross-verified with 100% name and demographic match.'), time: '1 day ago', type: 'doc' },
    { title: t('State DIC Camp Scheduled in Mumbai', 'State DIC Camp Scheduled in Mumbai'), desc: t('Fast-track PMEGP loan sanction camp on Sept 20th at Bandra Kurla Complex.', 'Fast-track PMEGP loan sanction camp on Sept 20th at Bandra Kurla Complex.'), time: '3 days ago', type: 'event' }
  ];

  return (
    <div className="max-w-3xl mx-auto py-8 px-4 space-y-6">
      <div className="flex items-center gap-3">
        <div className="p-2.5 bg-emerald-100 text-emerald-800 rounded-xl">
          <Bell className="w-5 h-5" />
        </div>
        <div>
          <h1 className="text-2xl font-black text-slate-900">{t('notifications & alerts')}</h1>
          <p className="text-xs text-slate-500">{t('gazette policy updates and application reminders')}</p>
        </div>
      </div>

      <div className="bg-white rounded-2xl border border-slate-200 divide-y divide-slate-100 shadow-sm">
        {notifications.map((n, idx) => (
          <div key={idx} className="p-5 flex items-start gap-4 hover:bg-slate-50/50">
            <div className="p-2 bg-emerald-50 text-emerald-600 rounded-lg shrink-0 mt-0.5">
              <CheckCircle2 className="w-4 h-4" />
            </div>
            <div className="space-y-1">
              <h3 className="font-bold text-slate-900 text-sm">{n.title}</h3>
              <p className="text-xs text-slate-600 leading-relaxed">{n.desc}</p>
              <span className="text-[10px] text-slate-400 block">{n.time}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
