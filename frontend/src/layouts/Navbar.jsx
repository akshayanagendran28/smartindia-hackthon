import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { Building2, Globe, LogOut, LayoutDashboard } from 'lucide-react';

const Navbar = () => {
  const { user, logout } = useAuth();
  const { currentLanguage, setLanguage, languages, t } = useLanguage();
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
              </div>
              <p className="text-[11px] text-slate-500 font-medium hidden sm:block">{t('Statutory Scheme Matching & Subventions')}</p>
            </div>
          </Link>

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
                  <div className="px-3 py-1 text-[11px] font-bold text-slate-400 uppercase tracking-wider">{t('Select Language')}</div>
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
                <Link to="/login" className="px-3 py-1.5 text-xs font-semibold text-slate-700 hover:text-gov-blue">{t('Login')}</Link>
                <Link to="/register" className="px-3.5 py-1.5 text-xs font-bold text-white bg-gov-blue hover:bg-gov-darkblue rounded-lg shadow-sm">{t('Register')}</Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};
export default Navbar;
