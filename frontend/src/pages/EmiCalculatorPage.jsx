import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate, Link } from 'react-router-dom';
import { 
  Calculator, DollarSign, Calendar, Percent, Sparkles, 
  TrendingUp, ShieldCheck, ArrowRight, PieChart, Lock, CheckCircle2,
  Building2, ExternalLink, RefreshCw
} from 'lucide-react';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';
import { useLanguage } from '../context/LanguageContext';
import { useApplication } from '../context/ApplicationContext';
import StepProgressIndicator from '../components/StepProgressIndicator';

export default function EmiCalculatorPage() {
  const { t } = useLanguage();
  const location = useLocation();
  const navigate = useNavigate();
  const { application, selectedScheme, updateLoanAmount } = useApplication();

  const activeScheme = location.state?.selectedScheme || selectedScheme;

  // Initialize parameters from selected scheme or application single source of truth
  const [loanAmount, setLoanAmount] = useState(
    location.state?.loanAmount || application.loanAmount || 1200000
  );
  
  const getInitialSubsidy = () => {
    if (activeScheme?.scheme_code === 'PMEGP') return 35;
    if (activeScheme?.scheme_code === 'SVANIDHI') return 7;
    if (activeScheme?.scheme_code === 'VISHWAKARMA') return 8;
    return 25;
  };

  const getInitialInterest = () => {
    if (activeScheme?.scheme_code === 'VISHWAKARMA') return 5.0;
    if (activeScheme?.scheme_code === 'SVANIDHI') return 7.0;
    if (activeScheme?.scheme_code === 'STANDUP-IND') return 7.5;
    return 8.5;
  };

  const getInitialTenure = () => {
    if (activeScheme?.repayment_period_months) {
      return Math.max(1, Math.round(activeScheme.repayment_period_months / 12));
    }
    return 5;
  };

  const [interestRate, setInterestRate] = useState(getInitialInterest());
  const [tenureYears, setTenureYears] = useState(getInitialTenure());
  const [subsidyPercent, setSubsidyPercent] = useState(getInitialSubsidy());
  const [moratoriumMonths, setMoratoriumMonths] = useState(6);

  useEffect(() => {
    if (activeScheme) {
      setSubsidyPercent(getInitialSubsidy());
      setInterestRate(getInitialInterest());
      setTenureYears(getInitialTenure());
    }
  }, [activeScheme]);

  const handleLoanChange = (val) => {
    const num = Number(val);
    setLoanAmount(num);
    updateLoanAmount(num);
  };

  // Financial calculations
  const effectiveSubsidy = (loanAmount * subsidyPercent) / 100;
  const netLoanAmount = Math.max(0, loanAmount - effectiveSubsidy);

  const monthlyRate = interestRate / (12 * 100);
  const totalMonths = tenureYears * 12;

  // Monthly EMI = [P x R x (1+R)^N] / [(1+R)^N - 1]
  const calculatedEmi = monthlyRate > 0
    ? (netLoanAmount * monthlyRate * Math.pow(1 + monthlyRate, totalMonths)) / (Math.pow(1 + monthlyRate, totalMonths) - 1)
    : netLoanAmount / totalMonths;

  const totalPayment = calculatedEmi * totalMonths;
  const totalInterest = Math.max(0, totalPayment - netLoanAmount);

  // Generate Amortization Chart Data (Year by Year)
  const chartData = [];
  let balance = netLoanAmount;
  for (let y = 1; y <= tenureYears; y++) {
    const yearlyInterest = balance * (interestRate / 100);
    const yearlyPrincipal = (calculatedEmi * 12) - yearlyInterest;
    balance = Math.max(0, balance - yearlyPrincipal);
    chartData.push({
      year: `Year ${y}`,
      remainingBalance: Math.round(balance),
      principalPaid: Math.round(netLoanAmount - balance),
      interestPaid: Math.round(yearlyInterest * y)
    });
  }

  const setPreset = (amount, rate, tenure, sub) => {
    handleLoanChange(amount);
    setInterestRate(rate);
    setTenureYears(tenure);
    setSubsidyPercent(sub);
  };

  // Gated: If no scheme selected, render lock screen
  if (!activeScheme) {
    return (
      <div className="max-w-4xl mx-auto py-10 px-4 sm:px-6 space-y-8">
        <StepProgressIndicator currentStep={6} />
        
        <div className="bg-white p-12 rounded-3xl border border-slate-200 shadow-xl text-center space-y-6">
          <div className="w-20 h-20 bg-amber-50 text-amber-600 rounded-3xl flex items-center justify-center mx-auto shadow-inner border border-amber-200/60">
            <Lock className="w-10 h-10" />
          </div>

          <div className="space-y-2 max-w-lg mx-auto">
            <h2 className="text-2xl font-black text-slate-900">
              EMI & Subvention Calculator Locked
            </h2>
            <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
              In the Scheme Sathi workflow, financial calculations require active parameters (subvention caps, interest rate ceilings, and moratorium rules) from your qualified government scheme.
            </p>
          </div>

          <div className="p-4 bg-slate-50 border border-slate-200 rounded-2xl max-w-md mx-auto text-xs text-slate-600 space-y-2 text-left">
            <div className="font-bold text-slate-800 flex items-center gap-1.5">
              <ShieldCheck className="w-4 h-4 text-emerald-600" />
              <span>Current Applicant Context:</span>
            </div>
            <div className="flex justify-between border-b border-slate-200 pb-1">
              <span>Required Loan:</span>
              <span className="font-bold text-slate-900">₹{(application.loanAmount / 100000).toLocaleString('en-IN')} Lakhs</span>
            </div>
            <div className="flex justify-between">
              <span>Beneficiary Category:</span>
              <span className="font-bold text-slate-900">{application.category} ({application.district}, {application.state})</span>
            </div>
          </div>

          <div className="pt-2 flex flex-col sm:flex-row justify-center gap-3">
            <button
              onClick={() => navigate('/results')}
              className="px-6 py-3 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-black rounded-xl shadow-lg transition-all flex items-center justify-center gap-2 hover:scale-[1.02]"
            >
              <span>Go to Step 4: Select an Eligible Scheme</span>
              <ArrowRight className="w-4 h-4" />
            </button>
            <button
              onClick={() => navigate('/documents')}
              className="px-6 py-3 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-xl transition-all"
            >
              Review Verified Documents
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto py-8 px-4 sm:px-6 space-y-8">
      {/* 7-Step Dynamic Progress Breadcrumb Indicator */}
      <StepProgressIndicator currentStep={6} />

      {/* Selected Scheme Active Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-emerald-950 to-slate-900 p-6 rounded-3xl text-white shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4 border border-emerald-900/50">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <span className="px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 text-xs font-black border border-emerald-500/30">
              Active Scheme: {activeScheme.scheme_code}
            </span>
            <span className="text-xs text-slate-300">
              &bull; {activeScheme.ministry || 'Government of India'}
            </span>
          </div>
          <h1 className="text-2xl font-black text-white">{activeScheme.scheme_name || activeScheme.name}</h1>
          <p className="text-xs text-slate-300">
            Preloaded with official subsidy matrices: <strong className="text-emerald-300">{subsidyPercent}% Government Subvention</strong> &bull; {interestRate}% p.a.
          </p>
        </div>

        <Link
          to="/results"
          className="shrink-0 px-4 py-2 bg-white/10 hover:bg-white/20 text-white rounded-xl text-xs font-bold transition-all flex items-center gap-1.5 self-start md:self-auto border border-white/10"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Switch Scheme</span>
        </Link>
      </div>

      {/* Preset Scheme Quick Buttons */}
      <div className="flex flex-wrap gap-2 items-center bg-slate-100 p-2 rounded-2xl text-xs">
        <span className="font-bold text-slate-500 px-2">Quick Presets:</span>
        <button
          onClick={() => setPreset(1000000, 8.5, 5, 35)}
          className="px-3 py-1.5 bg-white hover:bg-emerald-50 text-slate-700 hover:text-emerald-800 font-bold rounded-xl border border-slate-200 transition-all"
        >
          PMEGP Rural (₹10L @ 35% Subsidy)
        </button>
        <button
          onClick={() => setPreset(2500000, 7.5, 7, 0)}
          className="px-3 py-1.5 bg-white hover:bg-emerald-50 text-slate-700 hover:text-emerald-800 font-bold rounded-xl border border-slate-200 transition-all"
        >
          Stand-Up India (₹25L @ 7.5%)
        </button>
        <button
          onClick={() => setPreset(50000, 7.0, 1, 7)}
          className="px-3 py-1.5 bg-white hover:bg-emerald-50 text-slate-700 hover:text-emerald-800 font-bold rounded-xl border border-slate-200 transition-all"
        >
          PM SVANidhi (₹50k @ 7%)
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left Slider Inputs */}
        <div className="lg:col-span-6 bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-6">
          <h2 className="text-base font-black text-slate-900 pb-2 border-b border-slate-100 flex items-center justify-between">
            <span>Financial Parameter Calibration</span>
            <span className="text-[10px] text-slate-400 font-mono">Single Source of Truth</span>
          </h2>

          {/* Sanction Loan Slider */}
          <div>
            <div className="flex justify-between text-xs font-bold text-slate-700 mb-1">
              <span>Required Loan Amount</span>
              <span className="text-emerald-700 text-sm font-black">₹{loanAmount.toLocaleString('en-IN')}</span>
            </div>
            <input
              type="range"
              min="10000"
              max="5000000"
              step="25000"
              value={loanAmount}
              onChange={(e) => handleLoanChange(e.target.value)}
              className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-emerald-600"
            />
            <div className="flex justify-between text-[10px] text-slate-400 mt-1">
              <span>₹10,000</span>
              <span>₹25 Lakh</span>
              <span>₹50 Lakh</span>
            </div>
          </div>

          {/* Subsidy Percentage Slider */}
          <div>
            <div className="flex justify-between text-xs font-bold text-slate-700 mb-1">
              <span>Government Capital Subsidy / Subvention</span>
              <span className="text-teal-700 text-sm font-black">{subsidyPercent}% (₹{effectiveSubsidy.toLocaleString('en-IN')})</span>
            </div>
            <input
              type="range"
              min="0"
              max="50"
              step="5"
              value={subsidyPercent}
              onChange={(e) => setSubsidyPercent(Number(e.target.value))}
              className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-teal-600"
            />
            <div className="flex justify-between text-[10px] text-slate-400 mt-1">
              <span>0% (Stand-Up)</span>
              <span>25% (Urban General)</span>
              <span>35% (Special Rural)</span>
            </div>
          </div>

          {/* Interest Rate Slider */}
          <div>
            <div className="flex justify-between text-xs font-bold text-slate-700 mb-1">
              <span>Annual Interest Rate</span>
              <span className="text-slate-900 text-sm font-black">{interestRate}% p.a.</span>
            </div>
            <input
              type="range"
              min="1"
              max="18"
              step="0.25"
              value={interestRate}
              onChange={(e) => setInterestRate(Number(e.target.value))}
              className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-slate-700"
            />
          </div>

          {/* Tenure Slider */}
          <div>
            <div className="flex justify-between text-xs font-bold text-slate-700 mb-1">
              <span>Repayment Tenure</span>
              <span className="text-slate-900 text-sm font-black">{tenureYears} Years ({totalMonths} Months)</span>
            </div>
            <input
              type="range"
              min="1"
              max="10"
              step="1"
              value={tenureYears}
              onChange={(e) => setTenureYears(Number(e.target.value))}
              className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-slate-700"
            />
          </div>
        </div>

        {/* Right Calculated Results & Chart */}
        <div className="lg:col-span-6 space-y-6">
          {/* Key Output Card */}
          <div className="bg-gradient-to-br from-slate-900 to-emerald-950 text-white p-6 rounded-3xl shadow-xl space-y-4">
            <span className="text-xs uppercase font-bold tracking-widest text-emerald-400">Calculated Monthly EMI</span>
            <div className="text-4xl sm:text-5xl font-black text-white">
              ₹{Math.round(calculatedEmi).toLocaleString('en-IN')}
              <span className="text-xs font-normal text-slate-300 ml-2">/ month</span>
            </div>

            <div className="grid grid-cols-3 gap-3 pt-4 border-t border-white/10 text-xs">
              <div>
                <span className="text-slate-400 block text-[10px]">Net Principal</span>
                <span className="font-bold text-emerald-300">₹{Math.round(netLoanAmount).toLocaleString('en-IN')}</span>
              </div>
              <div>
                <span className="text-slate-400 block text-[10px]">Total Interest</span>
                <span className="font-bold text-amber-300">₹{Math.round(totalInterest).toLocaleString('en-IN')}</span>
              </div>
              <div>
                <span className="text-slate-400 block text-[10px]">Govt Subsidy</span>
                <span className="font-bold text-teal-300">₹{Math.round(effectiveSubsidy).toLocaleString('en-IN')}</span>
              </div>
            </div>
          </div>

          {/* Amortization Chart */}
          <div className="bg-white p-5 rounded-3xl border border-slate-200 shadow-sm space-y-2">
            <span className="text-xs font-bold text-slate-700 block">Amortization Principal Repayment Curve</span>
            <div className="h-44 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                  <XAxis dataKey="year" tick={{ fontSize: 10 }} />
                  <YAxis tick={{ fontSize: 10 }} tickFormatter={(v) => `₹${v / 1000}k`} />
                  <Tooltip formatter={(v) => `₹${Number(v).toLocaleString('en-IN')}`} />
                  <Area type="monotone" dataKey="remainingBalance" name="Remaining Principal" stroke="#10b981" fill="#d1fae5" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Bottom Workflow Action */}
          <div className="pt-2">
            <button
              onClick={() => navigate('/partners', { state: { schemeCode: activeScheme.scheme_code, scheme: activeScheme } })}
              className="w-full py-3.5 px-5 bg-emerald-600 hover:bg-emerald-700 text-white font-black text-xs rounded-2xl shadow-lg transition-all flex items-center justify-center gap-2 hover:scale-[1.01]"
            >
              <span>Locate Processing Partner Branches for {activeScheme.scheme_code} (Step 7)</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

