import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { Building2, Globe, User, LogOut, Menu, X, Sparkles, LayoutDashboard } from 'lucide-react';

const Navbar = () => {
  const { user, logout } = useAuth();
  const { currentLanguage, setLanguage, languages, t } = useLanguage();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isLangOpen, setIsLangOpen] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <header className="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-slate-200 shadow-sm">
      <div className="h-1 w-full bg-gradient-to-r from-[#FF9933] via-white to-[#138808]"></div>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          <Link to="/" className="flex items-center gap-3 group">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-gov-darkblue to-gov-blue text-white flex items-center justify-center font-bold text-xl shadow-md group-hover:scale-105 transition-transform">
              <Building2 className="w-6 h-6 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-1.5">
                <span className="font-extrabold text-xl text-gov-darkblue tracking-tight">SCHEME</span>
                <span className="font-extrabold text-xl text-gov-accent tracking-tight">SATHI</span>
                <span className="text-[10px] font-semibold bg-emerald-100 text-emerald-800 px-1.5 py-0.5 rounded border border-emerald-300">SIH 2026</span>
              </div>
              <p className="text-[11px] text-slate-500 font-medium hidden sm:block">AI-Driven Financial Scheme Matching for Entrepreneurs</p>
            </div>
          </Link>

          <nav className="hidden md:flex items-center space-x-1 lg:space-x-2 text-sm font-medium text-slate-700">
            <Link to="/" className={`px-3 py-1.5 rounded-lg transition-colors ${location.pathname === '/' ? 'text-gov-blue font-semibold bg-blue-50' : 'hover:text-gov-blue hover:bg-slate-100'}`}>
              {t('navHome')}
            </Link>
            <Link to="/find-scheme" className={`px-3 py-1.5 rounded-lg flex items-center gap-1.5 transition-colors ${location.pathname === '/find-scheme' ? 'text-gov-blue font-semibold bg-blue-50' : 'hover:text-gov-blue hover:bg-slate-100'}`}>
              <Sparkles className="w-4 h-4 text-gov-accent" />
              {t('navFindScheme')}
            </Link>
            <Link to="/schemes" className={`px-3 py-1.5 rounded-lg transition-colors ${location.pathname === '/schemes' ? 'text-gov-blue font-semibold bg-blue-50' : 'hover:text-gov-blue hover:bg-slate-100'}`}>
              {t('navSchemes')}
            </Link>
            <Link to="/calculator" className={`px-3 py-1.5 rounded-lg transition-colors ${location.pathname === '/calculator' ? 'text-gov-blue font-semibold bg-blue-50' : 'hover:text-gov-blue hover:bg-slate-100'}`}>
              {t('navEmi')}
            </Link>
            <Link to="/documents" className={`px-3 py-1.5 rounded-lg transition-colors ${location.pathname === '/documents' ? 'text-gov-blue font-semibold bg-blue-50' : 'hover:text-gov-blue hover:bg-slate-100'}`}>
              {t('navDocAssistant')}
            </Link>
            <Link to="/partners" className={`px-3 py-1.5 rounded-lg transition-colors ${location.pathname === '/partners' ? 'text-gov-blue font-semibold bg-blue-50' : 'hover:text-gov-blue hover:bg-slate-100'}`}>
              {t('navPartners')}
            </Link>
            <Link to="/chat" className={`px-3 py-1.5 rounded-lg transition-colors ${location.pathname === '/chat' ? 'text-gov-blue font-semibold bg-blue-50' : 'hover:text-gov-blue hover:bg-slate-100'}`}>
              {t('navChat')}
            </Link>
          </nav>

          <div className="flex items-center gap-2 sm:gap-3">
            <div className="relative">
              <button 
                onClick={() => setIsLangOpen(!isLangOpen)}
                className="flex items-center gap-1.5 px-2.5 py-1.5 text-xs font-semibold text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-lg border border-slate-300 transition-colors"
              >
                <Globe className="w-3.5 h-3.5 text-gov-blue" />
                <span className="hidden sm:inline">{languages.find(l => l.code === currentLanguage)?.name}</span>
                <span className="sm:hidden uppercase">{currentLanguage}</span>
              </button>

              {isLangOpen && (
                <div className="absolute right-0 mt-2 w-40 bg-white rounded-xl shadow-xl border border-slate-200 py-1.5 z-50">
                  <div className="px-3 py-1 text-[11px] font-bold text-slate-400 uppercase tracking-wider">Select Language</div>
                  {languages.map((lang) => (
                    <button
                      key={lang.code}
                      onClick={() => { setLanguage(lang.code); setIsLangOpen(false); }}
                      className={`w-full text-left px-3 py-1.5 text-xs flex items-center justify-between hover:bg-blue-50 ${currentLanguage === lang.code ? 'font-bold text-gov-blue bg-blue-50/50' : 'text-slate-700'}`}
                    >
                      <span>{lang.name}</span>
                      <span className="text-[11px] text-slate-400">{lang.native}</span>
                    </button>
                  ))}
                </div>
              )}
            </div>

            {user ? (
              <div className="flex items-center gap-2">
                <Link
                  to={user.role === 'admin' || user.role === 'supervisor' ? '/admin' : '/dashboard'}
                  className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-bold text-gov-darkblue bg-blue-100/70 hover:bg-blue-200/80 rounded-lg border border-blue-300 transition-colors"
                >
                  <LayoutDashboard className="w-3.5 h-3.5 text-gov-blue" />
                  <span className="hidden sm:inline">{user.full_name?.split(' ')[0]}</span>
                  {user.role === 'admin' && (
                    <span className="bg-purple-600 text-white text-[9px] px-1.5 py-0.5 rounded uppercase font-extrabold">Admin</span>
                  )}
                </Link>
                <button
                  onClick={handleLogout}
                  className="p-1.5 text-slate-500 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                  title="Logout"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <Link to="/login" className="px-3 py-1.5 text-xs font-semibold text-slate-700 hover:text-gov-blue">{t('navLogin')}</Link>
                <Link to="/register" className="px-3.5 py-1.5 text-xs font-bold text-white bg-gov-blue hover:bg-gov-darkblue rounded-lg shadow-sm">{t('navRegister')}</Link>
              </div>
            )}

            <button onClick={() => setIsMenuOpen(!isMenuOpen)} className="md:hidden p-1.5 rounded-lg text-slate-600 hover:bg-slate-100">
              {isMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>
      </div>

      {isMenuOpen && (
        <div className="md:hidden border-t border-slate-200 bg-white px-4 pt-2 pb-4 space-y-1 shadow-lg">
          <Link to="/" onClick={() => setIsMenuOpen(false)} className="block px-3 py-2 rounded-lg text-sm text-slate-700 hover:bg-blue-50">{t('navHome')}</Link>
          <Link to="/find-scheme" onClick={() => setIsMenuOpen(false)} className="block px-3 py-2 rounded-lg text-sm font-semibold text-gov-blue bg-blue-50">✨ {t('navFindScheme')}</Link>
          <Link to="/schemes" onClick={() => setIsMenuOpen(false)} className="block px-3 py-2 rounded-lg text-sm text-slate-700 hover:bg-blue-50">{t('navSchemes')}</Link>
          <Link to="/calculator" onClick={() => setIsMenuOpen(false)} className="block px-3 py-2 rounded-lg text-sm text-slate-700 hover:bg-blue-50">{t('navEmi')}</Link>
          <Link to="/documents" onClick={() => setIsMenuOpen(false)} className="block px-3 py-2 rounded-lg text-sm text-slate-700 hover:bg-blue-50">{t('navDocAssistant')}</Link>
          <Link to="/partners" onClick={() => setIsMenuOpen(false)} className="block px-3 py-2 rounded-lg text-sm text-slate-700 hover:bg-blue-50">{t('navPartners')}</Link>
          <Link to="/chat" onClick={() => setIsMenuOpen(false)} className="block px-3 py-2 rounded-lg text-sm text-slate-700 hover:bg-blue-50">{t('navChat')}</Link>
        </div>
      )}
    </header>
  );
};
export default Navbar;
