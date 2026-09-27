import React from 'react';
import { Link } from 'react-router-dom';
import { Building2, ShieldCheck, HeartHandshake, ExternalLink } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

const Footer = () => {
  const { t } = useLanguage();
  return (
    <footer className="bg-gov-darkblue text-slate-200 pt-12 pb-8 border-t-4 border-gov-accent">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          
          <div className="md:col-span-1 space-y-3">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-lg bg-gov-accent flex items-center justify-center text-white font-bold">
                <Building2 className="w-5 h-5 text-gov-darkblue" />
              </div>
              <span className="font-extrabold text-xl text-white tracking-tight">{t('appName')}</span>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">
              {t('heroSubtitle')}
            </p>
            <div className="inline-block bg-slate-800/80 border border-slate-700 rounded-lg px-2.5 py-1 text-[11px] text-emerald-300 font-medium">
              {t('translationBadge')}
            </div>
          </div>

          <div>
            <h4 className="text-sm font-bold text-white uppercase tracking-wider mb-3">{t('navFeatures')}</h4>
            <ul className="space-y-2 text-xs text-slate-300">
              <li><Link to="/find-scheme" className="hover:text-gov-accent transition-colors">✨ {t('navFindScheme')}</Link></li>
              <li><Link to="/schemes" className="hover:text-gov-accent transition-colors">🏛 {t('navSchemes')}</Link></li>
              <li><Link to="/calculator" className="hover:text-gov-accent transition-colors">📊 {t('navEmi')}</Link></li>
              <li><Link to="/documents" className="hover:text-gov-accent transition-colors">📑 {t('navDocAssistant')}</Link></li>
              <li><Link to="/partners" className="hover:text-gov-accent transition-colors">📍 {t('navPartners')}</Link></li>
            </ul>
          </div>

          <div>
            <h4 className="text-sm font-bold text-white uppercase tracking-wider mb-3">{t('Official Portals', 'Official Portals')}</h4>
            <ul className="space-y-2 text-xs text-slate-300">
              <li><a href="https://www.kviconline.gov.in" target="_blank" rel="noreferrer" className="flex items-center gap-1 hover:text-gov-accent">KVIC PMEGP Portal <ExternalLink className="w-3 h-3 text-slate-400" /></a></li>
              <li><a href="https://www.mudra.org.in" target="_blank" rel="noreferrer" className="flex items-center gap-1 hover:text-gov-accent">Pradhan Mantri MUDRA <ExternalLink className="w-3 h-3 text-slate-400" /></a></li>
              <li><a href="https://www.standupmitra.in" target="_blank" rel="noreferrer" className="flex items-center gap-1 hover:text-gov-accent">Stand-Up Mitra Portal <ExternalLink className="w-3 h-3 text-slate-400" /></a></li>
              <li><a href="https://pmsvanidhi.mohua.gov.in" target="_blank" rel="noreferrer" className="flex items-center gap-1 hover:text-gov-accent">PM SVANidhi Portal <ExternalLink className="w-3 h-3 text-slate-400" /></a></li>
              <li><a href="https://pmvishwakarma.gov.in" target="_blank" rel="noreferrer" className="flex items-center gap-1 hover:text-gov-accent">PM Vishwakarma <ExternalLink className="w-3 h-3 text-slate-400" /></a></li>
            </ul>
          </div>

          <div>
            <h4 className="text-sm font-bold text-white uppercase tracking-wider mb-3">{t('GovTech Trust & Safety', 'GovTech Trust & Safety')}</h4>
            <div className="space-y-2.5 text-xs text-slate-300">
              <div className="flex items-start gap-2">
                <ShieldCheck className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                <span>{t('step2WorkflowDesc')}</span>
              </div>
              <div className="flex items-start gap-2">
                <HeartHandshake className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
                <span>{t('translationBadge')}</span>
              </div>
              <div className="bg-slate-800/80 p-2.5 rounded-lg border border-slate-700 text-slate-300">
                <p className="text-[11px] font-semibold text-white">{t('National MSME Helpline', 'National MSME Helpline')}</p>
                <p className="text-xs text-amber-300 font-mono">1800-180-6763 (Toll Free)</p>
              </div>
            </div>
          </div>

        </div>

        <div className="pt-6 border-t border-slate-800 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-400 gap-3">
          <p>© 2026 {t('appName')}. {t('sihSubtext')}</p>
          <div className="flex items-center gap-4 text-slate-400 text-xs">
            <span>{t('Prototype Demo Environment', 'Prototype Demo Environment')}</span>
            <span>•</span>
            <Link to="/admin" className="hover:text-amber-300 transition-colors">{t('navAdmin')}</Link>
          </div>
        </div>
      </div>
    </footer>
  );
};
export default Footer;
