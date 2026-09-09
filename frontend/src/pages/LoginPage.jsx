import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { Lock, Mail, ShieldCheck, ArrowRight, UserCheck, AlertCircle } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';

export default function LoginPage() {
  const { login } = useAuth();
  const { t } = useLanguage();
  const navigate = useNavigate();
  const location = useLocation();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const from = location.state?.from?.pathname || '/dashboard';

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const res = await login(email, password);
      if (res.user?.role === 'admin') {
        navigate('/admin');
      } else {
        navigate(from, { replace: true });
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Invalid email or password. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const fillDemo = (role) => {
    if (role === 'entrepreneur') {
      setEmail('priya@example.com');
      setPassword('password123');
    } else if (role === 'vendor') {
      setEmail('rahul@example.com');
      setPassword('password123');
    } else if (role === 'admin') {
      setEmail('admin@schemesathi.gov.in');
      setPassword('admin123');
    }
  };

  return (
    <div className="min-h-[85vh] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 bg-slate-50">
      <div className="max-w-md w-full space-y-8 bg-white p-8 rounded-2xl shadow-xl border border-slate-200">
        <div className="text-center">
          <div className="inline-flex p-3 rounded-2xl bg-emerald-100 text-emerald-800 mb-3">
            <ShieldCheck className="w-8 h-8" />
          </div>
          <h2 className="text-2xl font-extrabold text-slate-900">{t('login')} to Scheme Sathi</h2>
          <p className="text-xs text-slate-500 mt-1">Access your personalized eligibility profile & applications</p>
        </div>

        {error && (
          <div className="p-3.5 rounded-xl bg-red-50 border border-red-200 text-red-700 text-xs flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {/* Demo Fast-Fill Bar */}
        <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 text-xs">
          <span className="font-semibold text-slate-700 block mb-1.5">Quick Demo Login:</span>
          <div className="flex gap-2">
            <button
              type="button"
              onClick={() => fillDemo('entrepreneur')}
              className="flex-1 py-1 px-2 bg-white border border-slate-300 rounded text-[11px] font-medium text-slate-700 hover:bg-emerald-50 hover:border-emerald-300"
            >
              Woman Founder
            </button>
            <button
              type="button"
              onClick={() => fillDemo('vendor')}
              className="flex-1 py-1 px-2 bg-white border border-slate-300 rounded text-[11px] font-medium text-slate-700 hover:bg-emerald-50 hover:border-emerald-300"
            >
              Street Vendor
            </button>
            <button
              type="button"
              onClick={() => fillDemo('admin')}
              className="flex-1 py-1 px-2 bg-white border border-slate-300 rounded text-[11px] font-medium text-slate-700 hover:bg-emerald-50 hover:border-emerald-300"
            >
              Admin Portal
            </button>
          </div>
        </div>

        <form className="mt-6 space-y-4" onSubmit={handleSubmit}>
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Email Address</label>
            <div className="relative">
              <Mail className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="name@example.com"
                className="w-full pl-9 pr-3 py-2.5 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Password</label>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full pl-9 pr-3 py-2.5 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 px-4 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-lg shadow-md transition-all flex items-center justify-center gap-2 text-sm disabled:opacity-50"
          >
            {loading ? <span>Authenticating...</span> : (
              <>
                <span>Sign In</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </form>

        <div className="text-center pt-2">
          <p className="text-xs text-slate-600">
            Don't have an account?{' '}
            <Link to="/register" className="font-bold text-emerald-700 hover:underline">
              Create Entrepreneur Profile
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
