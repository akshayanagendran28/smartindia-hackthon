import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import { 
  Calculator, DollarSign, Calendar, Percent, Sparkles, 
  TrendingUp, ShieldCheck, ArrowRight, PieChart 
} from 'lucide-react';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';
import { useLanguage } from '../context/LanguageContext';

export default function EmiCalculatorPage() {
  const { t } = useLanguage();
  const location = useLocation();

  const [loanAmount, setLoanAmount] = useState(location.state?.loanAmount || 1000000);
  const [interestRate, setInterestRate] = useState(location.state?.interestRate || 8.5);
  const [tenureYears, setTenureYears] = useState(5);
  const [subsidyPercent, setSubsidyPercent] = useState(35);
  const [moratoriumMonths, setMoratoriumMonths] = useState(6);

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
      year: `${t('yearCol')} ${y}`,
      remainingBalance: Math.round(balance),
      principalPaid: Math.round(netLoanAmount - balance),
      interestPaid: Math.round(yearlyInterest * y)
    });
  }

  const setPreset = (name, amount, rate, tenure, sub) => {
    setLoanAmount(amount);
    setInterestRate(rate);
    setTenureYears(tenure);
    setSubsidyPercent(sub);
  };

  return (
    <div className="max-w-6xl mx-auto py-8 px-4 sm:px-6 space-y-8">
      {/* Header */}
      <div>
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold mb-2">
          <Calculator className="w-3.5 h-3.5" />
          <span>{t('sihBadgeText')} • {t('translationBadge')}</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-black text-slate-900">{t('calcTitle')}</h1>
        <p className="text-xs sm:text-sm text-slate-500 mt-1">
          {t('calcSubtitle')}
        </p>
      </div>

      {/* Preset Scheme Buttons */}
      <div className="flex flex-wrap gap-2">
        <span className="text-xs font-bold text-slate-500 self-center mr-1">{t('calcQuickPresets')}</span>
        <button
          onClick={() => setPreset('PMEGP Rural', 1000000, 8.5, 5, 35)}
          className="px-3 py-1.5 bg-white border border-slate-200 hover:border-emerald-300 rounded-lg text-xs font-semibold text-slate-700"
        >
          PMEGP Rural (₹10 {t('unitLakh')} @ 35% {t('subsidyRate')})
        </button>
        <button
          onClick={() => setPreset('Stand-Up India', 2500000, 7.5, 7, 0)}
          className="px-3 py-1.5 bg-white border border-slate-200 hover:border-emerald-300 rounded-lg text-xs font-semibold text-slate-700"
        >
          Stand-Up India (₹25 {t('unitLakh')} @ 7.5%)
        </button>
        <button
          onClick={() => setPreset('PM SVANidhi', 50000, 7.0, 1, 7)}
          className="px-3 py-1.5 bg-white border border-slate-200 hover:border-emerald-300 rounded-lg text-xs font-semibold text-slate-700"
        >
          PM SVANidhi (₹50,000)
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left Slider Inputs */}
        <div className="lg:col-span-6 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-6">
          <h2 className="text-base font-bold text-slate-900 pb-2 border-b border-slate-100">{t('step4Title')}</h2>

          {/* Sanction Loan Slider */}
          <div>
            <div className="flex justify-between text-xs font-bold text-slate-700 mb-1">
              <span>{t('loanAmountLabel')}</span>
              <span className="text-emerald-700 text-sm font-extrabold">₹{loanAmount.toLocaleString('en-IN')}</span>
            </div>
            <input
              type="range"
              min="10000"
              max="10000000"
              step="25000"
              value={loanAmount}
              onChange={(e) => setLoanAmount(Number(e.target.value))}
              className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-emerald-600"
            />
            <div className="flex justify-between text-[10px] text-slate-400 mt-1">
              <span>₹10,000</span>
              <span>₹50 Lakh</span>
              <span>₹1 Crore</span>
            </div>
          </div>

          {/* Subsidy Percentage Slider */}
          <div>
            <div className="flex justify-between text-xs font-bold text-slate-700 mb-1">
              <span>{t('subsidyPercentLabel')}</span>
              <span className="text-teal-700 text-sm font-extrabold">{subsidyPercent}% (₹{effectiveSubsidy.toLocaleString('en-IN')})</span>
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
              <span>0%</span>
              <span>25% ({t('optionUrban')})</span>
              <span>35% ({t('optionRural')})</span>
            </div>
          </div>

          {/* Interest Rate Slider */}
          <div>
            <div className="flex justify-between text-xs font-bold text-slate-700 mb-1">
              <span>{t('interestRateLabel')}</span>
              <span className="text-slate-900 text-sm font-extrabold">{interestRate}% p.a.</span>
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
              <span>{t('tenureYearsLabel')}</span>
              <span className="text-slate-900 text-sm font-extrabold">{tenureYears} {t('unitMonths')} ({totalMonths} {t('unitMonths')})</span>
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
          <div className="bg-gradient-to-br from-slate-900 to-emerald-950 text-white p-6 rounded-2xl shadow-xl space-y-4">
            <span className="text-xs uppercase font-bold tracking-widest text-emerald-400">{t('monthlyEmi')}</span>
            <div className="text-4xl sm:text-5xl font-black text-white">
              ₹{Math.round(calculatedEmi).toLocaleString('en-IN')}
              <span className="text-xs font-normal text-slate-300 ml-2">/ {t('unitMonths')}</span>
            </div>

            <div className="grid grid-cols-3 gap-3 pt-4 border-t border-white/10 text-xs">
              <div>
                <span className="text-slate-400 block text-[10px]">{t('netPrincipal')}</span>
                <span className="font-bold text-emerald-300">₹{Math.round(netLoanAmount).toLocaleString('en-IN')}</span>
              </div>
              <div>
                <span className="text-slate-400 block text-[10px]">{t('totalInterest')}</span>
                <span className="font-bold text-amber-300">₹{Math.round(totalInterest).toLocaleString('en-IN')}</span>
              </div>
              <div>
                <span className="text-slate-400 block text-[10px]">{t('effectiveSubsidy')}</span>
                <span className="font-bold text-teal-300">₹{Math.round(effectiveSubsidy).toLocaleString('en-IN')}</span>
              </div>
            </div>
          </div>

          {/* Amortization Chart */}
          <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-2">
            <span className="text-xs font-bold text-slate-700 block">{t('amortizationSchedule')}</span>
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
        </div>
      </div>
    </div>
  );
}
