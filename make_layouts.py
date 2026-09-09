import os

base = 'C:/Users/aksha/.gemini/antigravity/scratch/scheme-sathi/frontend/src/layouts'
os.makedirs(base, exist_ok=True)

# 1. Navbar.jsx
navbar_code = """import React, { useState } from 'react';
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
"""

with open(os.path.join(base, 'Navbar.jsx'), 'w', encoding='utf-8') as f:
    f.write(navbar_code)

# 2. Footer.jsx
footer_code = """import React from 'react';
import { Link } from 'react-router-dom';
import { Building2, ShieldCheck, HeartHandshake, ExternalLink } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-gov-darkblue text-slate-200 pt-12 pb-8 border-t-4 border-gov-accent">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          
          <div className="md:col-span-1 space-y-3">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-lg bg-gov-accent flex items-center justify-center text-white font-bold">
                <Building2 className="w-5 h-5 text-gov-darkblue" />
              </div>
              <span className="font-extrabold text-xl text-white tracking-tight">SCHEME SATHI</span>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">
              AI-driven multi-factor government financial scheme discovery & eligibility matching platform for marginalized entrepreneurs and students.
            </p>
            <div className="inline-block bg-slate-800/80 border border-slate-700 rounded-lg px-2.5 py-1 text-[11px] text-amber-300 font-medium">
              Smart India Hackathon 2026 | ID: SIH26092
            </div>
          </div>

          <div>
            <h4 className="text-sm font-bold text-white uppercase tracking-wider mb-3">Key Features</h4>
            <ul className="space-y-2 text-xs text-slate-300">
              <li><Link to="/find-scheme" className="hover:text-gov-accent transition-colors">✨ Find My Scheme (Questionnaire)</Link></li>
              <li><Link to="/schemes" className="hover:text-gov-accent transition-colors">🏛 Verified Government Schemes</Link></li>
              <li><Link to="/calculator" className="hover:text-gov-accent transition-colors">📊 EMI & Subsidy Calculator</Link></li>
              <li><Link to="/documents" className="hover:text-gov-accent transition-colors">📑 Document OCR Assistant</Link></li>
              <li><Link to="/partners" className="hover:text-gov-accent transition-colors">📍 Channel Partner Locator Map</Link></li>
            </ul>
          </div>

          <div>
            <h4 className="text-sm font-bold text-white uppercase tracking-wider mb-3">Official Portals</h4>
            <ul className="space-y-2 text-xs text-slate-300">
              <li><a href="https://www.kviconline.gov.in" target="_blank" rel="noreferrer" className="flex items-center gap-1 hover:text-gov-accent">KVIC PMEGP Portal <ExternalLink className="w-3 h-3 text-slate-400" /></a></li>
              <li><a href="https://www.mudra.org.in" target="_blank" rel="noreferrer" className="flex items-center gap-1 hover:text-gov-accent">Pradhan Mantri MUDRA <ExternalLink className="w-3 h-3 text-slate-400" /></a></li>
              <li><a href="https://www.standupmitra.in" target="_blank" rel="noreferrer" className="flex items-center gap-1 hover:text-gov-accent">Stand-Up Mitra Portal <ExternalLink className="w-3 h-3 text-slate-400" /></a></li>
              <li><a href="https://pmsvanidhi.mohua.gov.in" target="_blank" rel="noreferrer" className="flex items-center gap-1 hover:text-gov-accent">PM SVANidhi Portal <ExternalLink className="w-3 h-3 text-slate-400" /></a></li>
              <li><a href="https://pmvishwakarma.gov.in" target="_blank" rel="noreferrer" className="flex items-center gap-1 hover:text-gov-accent">PM Vishwakarma <ExternalLink className="w-3 h-3 text-slate-400" /></a></li>
            </ul>
          </div>

          <div>
            <h4 className="text-sm font-bold text-white uppercase tracking-wider mb-3">GovTech Trust & Safety</h4>
            <div className="space-y-2.5 text-xs text-slate-300">
              <div className="flex items-start gap-2">
                <ShieldCheck className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                <span>Deterministic rule evaluation ensures zero AI hallucinations in eligibility decisions.</span>
              </div>
              <div className="flex items-start gap-2">
                <HeartHandshake className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
                <span>Supports 6 regional Indian languages for inclusive access across rural and urban sectors.</span>
              </div>
              <div className="bg-slate-800/80 p-2.5 rounded-lg border border-slate-700 text-slate-300">
                <p className="text-[11px] font-semibold text-white">National MSME Helpline</p>
                <p className="text-xs text-amber-300 font-mono">1800-180-6763 (Toll Free)</p>
              </div>
            </div>
          </div>

        </div>

        <div className="pt-6 border-t border-slate-800 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-400 gap-3">
          <p>© 2026 SCHEME SATHI (SIH26092 Prototype). All government scheme data is sourced from verified public gazettes.</p>
          <div className="flex items-center gap-4 text-slate-400 text-xs">
            <span>Prototype Demo Environment</span>
            <span>•</span>
            <Link to="/admin" className="hover:text-amber-300 transition-colors">Admin Gateway</Link>
          </div>
        </div>
      </div>
    </footer>
  );
};
export default Footer;
"""

with open(os.path.join(base, 'Footer.jsx'), 'w', encoding='utf-8') as f:
    f.write(footer_code)

# 3. DashboardLayout.jsx
dash_code = """import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { 
  LayoutDashboard, Sparkles, FileSearch, Calculator, FileCheck2, MapPin, 
  MessageSquare, Award, Bell, History, UserCircle, Settings, LogOut,
  Layers, Sliders, Users, BarChart3, ChevronRight, ShieldCheck
} from 'lucide-react';

const DashboardLayout = ({ children, title, subtitle, isAdmin = false }) => {
  const { user, logout } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();

  const userNavItems = [
    { label: "Dashboard Overview", path: "/dashboard", icon: LayoutDashboard },
    { label: "Find My Scheme", path: "/find-scheme", icon: Sparkles, highlight: true },
    { label: "Requirement Questionnaire", path: "/questionnaire", icon: FileSearch },
    { label: "Recommended Schemes", path: "/results", icon: Award },
    { label: "Financial / EMI Calculator", path: "/calculator", icon: Calculator },
    { label: "Document Assistant (OCR)", path: "/documents", icon: FileCheck2 },
    { label: "Document Checklist", path: "/checklist", icon: FileCheck2 },
    { label: "Application Readiness", path: "/readiness", icon: ShieldCheck },
    { label: "Channel Partner Locator", path: "/partners", icon: MapPin },
    { label: "Scheme Sathi AI Chat", path: "/chat", icon: MessageSquare },
    { label: "Saved Schemes & History", path: "/history", icon: History },
    { label: "Notifications", path: "/notifications", icon: Bell },
    { label: "My Profile", path: "/profile", icon: UserCircle }
  ];

  const adminNavItems = [
    { label: "Executive Dashboard", path: "/admin", icon: LayoutDashboard },
    { label: "Scheme Management", path: "/admin/schemes", icon: Layers },
    { label: "Eligibility Rule Builder", path: "/admin/rules", icon: Sliders },
    { label: "Channel Partner Manager", path: "/admin/partners", icon: MapPin },
    { label: "User Directory", path: "/admin/users", icon: Users },
    { label: "Platform Analytics", path: "/admin/analytics", icon: BarChart3 }
  ];

  const navItems = isAdmin ? adminNavItems : userNavItems;

  return (
    <div className="min-h-screen bg-slate-100 flex flex-col md:flex-row">
      <aside className="w-full md:w-64 bg-white border-r border-slate-200 flex flex-col shrink-0">
        <div className="p-4 border-b border-slate-100 bg-slate-50/50">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gov-blue text-white flex items-center justify-center font-bold text-lg shadow-sm">
              {user?.full_name ? user.full_name[0].toUpperCase() : 'U'}
            </div>
            <div className="overflow-hidden">
              <h3 className="font-bold text-sm text-slate-900 truncate">{user?.full_name || 'Rajesh Kumar'}</h3>
              <div className="flex items-center gap-1.5">
                <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded uppercase tracking-wider ${isAdmin ? 'bg-purple-100 text-purple-700' : 'bg-emerald-100 text-emerald-800'}`}>
                  {isAdmin ? 'Supervisor / Admin' : (user?.role || 'Entrepreneur')}
                </span>
              </div>
            </div>
          </div>
        </div>

        <nav className="p-3 space-y-1 flex-1 overflow-y-auto max-h-[calc(100vh-140px)]">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center justify-between px-3 py-2 rounded-xl text-xs font-semibold transition-all ${
                  isActive
                    ? 'bg-gov-blue text-white shadow-sm'
                    : item.highlight
                    ? 'text-gov-blue bg-blue-50/80 hover:bg-blue-100 font-bold'
                    : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
                }`}
              >
                <div className="flex items-center gap-2.5">
                  <Icon className={`w-4 h-4 ${isActive ? 'text-white' : item.highlight ? 'text-gov-accent' : 'text-slate-400'}`} />
                  <span>{item.label}</span>
                </div>
                {isActive && <ChevronRight className="w-3.5 h-3.5 text-white/70" />}
              </Link>
            );
          })}
        </nav>

        <div className="p-3 border-t border-slate-100 space-y-1 bg-slate-50">
          {!isAdmin && (
            <Link to="/admin" className="flex items-center gap-2 px-3 py-2 rounded-lg text-xs font-semibold text-purple-700 hover:bg-purple-50">
              <Settings className="w-4 h-4 text-purple-600" />
              <span>Admin Portal</span>
            </Link>
          )}
          {isAdmin && (
            <Link to="/dashboard" className="flex items-center gap-2 px-3 py-2 rounded-lg text-xs font-semibold text-gov-blue hover:bg-blue-50">
              <LayoutDashboard className="w-4 h-4 text-gov-blue" />
              <span>Switch to User View</span>
            </Link>
          )}
          <button
            onClick={() => { logout(); navigate('/'); }}
            className="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-xs font-semibold text-red-600 hover:bg-red-50 text-left"
          >
            <LogOut className="w-4 h-4 text-red-500" />
            <span>Sign Out</span>
          </button>
        </div>
      </aside>

      <main className="flex-1 p-4 sm:p-6 lg:p-8 overflow-y-auto">
        {(title || subtitle) && (
          <div className="mb-6 pb-4 border-b border-slate-200 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
            <div>
              {title && <h1 className="text-xl sm:text-2xl font-black text-slate-900 tracking-tight">{title}</h1>}
              {subtitle && <p className="text-xs sm:text-sm text-slate-500 mt-0.5">{subtitle}</p>}
            </div>
            {isAdmin && (
              <span className="self-start sm:self-auto bg-purple-100 text-purple-800 text-xs font-bold px-2.5 py-1 rounded-full border border-purple-200">
                Admin Control Room
              </span>
            )}
          </div>
        )}

        {children}
      </main>
    </div>
  );
};
export default DashboardLayout;
"""

with open(os.path.join(base, 'DashboardLayout.jsx'), 'w', encoding='utf-8') as f:
    f.write(dash_code)

print('Layout components created successfully!')
