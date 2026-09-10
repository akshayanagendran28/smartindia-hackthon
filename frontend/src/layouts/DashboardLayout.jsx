import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { 
  LayoutDashboard, Sparkles, FileSearch, Calculator, FileCheck2, MapPin, 
  MessageSquare, Award, Bell, History, UserCircle, Settings, LogOut,
  Layers, Sliders, Users, BarChart3, ChevronRight, ShieldCheck
} from 'lucide-react';

const DashboardLayout = ({ children, title, subtitle, isAdmin = false }) => {
  const { user, logout } = useAuth();
  const { t } = useLanguage();
  const location = useLocation();
  const navigate = useNavigate();

  const userNavItems = [
    { label: "Dashboard Overview", key: "dashboardOverview", path: "/dashboard", icon: LayoutDashboard },
    { label: "Find My Scheme", key: "navFindScheme", path: "/find-scheme", icon: Sparkles, highlight: true },
    { label: "Requirement Questionnaire", key: "requirement questionnaire", path: "/questionnaire", icon: FileSearch },
    { label: "Recommended Schemes", key: "recommended schemes", path: "/results", icon: Award },
    { label: "Financial / EMI Calculator", key: "financial / emi calculator", path: "/calculator", icon: Calculator },
    { label: "Document Assistant (OCR)", key: "document assistant (ocr)", path: "/documents", icon: FileCheck2 },
    { label: "Document Checklist", key: "document checklist", path: "/checklist", icon: FileCheck2 },
    { label: "Application Readiness", key: "application readiness assessment", path: "/readiness", icon: ShieldCheck },
    { label: "Channel Partner Locator", key: "channel partner locator", path: "/partners", icon: MapPin },
    { label: "Scheme Sathi AI Chat", key: "scheme sathi ai chat", path: "/chat", icon: MessageSquare },
    { label: "Saved Schemes & History", key: "saved schemes & history", path: "/history", icon: History },
    { label: "Notifications", key: "notifications", path: "/notifications", icon: Bell },
    { label: "My Profile", key: "my profile", path: "/profile", icon: UserCircle }
  ];

  const adminNavItems = [
    { label: "Executive Dashboard", key: "Executive Dashboard", path: "/admin", icon: LayoutDashboard },
    { label: "Scheme Management", key: "Scheme Management", path: "/admin/schemes", icon: Layers },
    { label: "Eligibility Rule Builder", key: "Eligibility Rule Builder", path: "/admin/rules", icon: Sliders },
    { label: "Channel Partner Manager", key: "Channel Partner Manager", path: "/admin/partners", icon: MapPin },
    { label: "User Directory", key: "User Directory", path: "/admin/users", icon: Users },
    { label: "Platform Analytics", key: "Platform Analytics", path: "/admin/analytics", icon: BarChart3 }
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
              <h3 className="font-bold text-sm text-slate-900 truncate">{user?.full_name || 'Prasanth A K'}</h3>
              <div className="flex items-center gap-1.5">
                <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded uppercase tracking-wider ${isAdmin ? 'bg-purple-100 text-purple-700' : 'bg-emerald-100 text-emerald-800'}`}>
                  {isAdmin ? t('Supervisor / Admin', 'Supervisor / Admin') : t(user?.role || 'Entrepreneur', user?.role || 'Entrepreneur')}
                </span>
              </div>
            </div>
          </div>
        </div>

        <nav className="p-3 space-y-1 flex-1 overflow-y-auto max-h-[calc(100vh-140px)]">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            const displayLabel = t(item.key, item.label);
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
                  <span>{displayLabel}</span>
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
              <span>{t('admin portal')}</span>
            </Link>
          )}
          {isAdmin && (
            <Link to="/dashboard" className="flex items-center gap-2 px-3 py-2 rounded-lg text-xs font-semibold text-gov-blue hover:bg-blue-50">
              <LayoutDashboard className="w-4 h-4 text-gov-blue" />
              <span>{t('switch to user view')}</span>
            </Link>
          )}
          <button
            onClick={() => { logout(); navigate('/'); }}
            className="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-xs font-semibold text-red-600 hover:bg-red-50 text-left"
          >
            <LogOut className="w-4 h-4 text-red-500" />
            <span>{t('sign out')}</span>
          </button>
        </div>
      </aside>

      <main className="flex-1 p-4 sm:p-6 lg:p-8 overflow-y-auto">
        {(title || subtitle) && (
          <div className="mb-6 pb-4 border-b border-slate-200 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
            <div>
              {title && <h1 className="text-xl sm:text-2xl font-black text-slate-900 tracking-tight">{t(title, title)}</h1>}
              {subtitle && <p className="text-xs sm:text-sm text-slate-500 mt-0.5">{t(subtitle, subtitle)}</p>}
            </div>
            {isAdmin && (
              <span className="self-start sm:self-auto bg-purple-100 text-purple-800 text-xs font-bold px-2.5 py-1 rounded-full border border-purple-200">
                {t('Admin Control Room', 'Admin Control Room')}
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
