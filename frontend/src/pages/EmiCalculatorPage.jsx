import React, { useState, useEffect, useMemo } from 'react';
import { useLocation, useNavigate, Link } from 'react-router-dom';
import { 
  Calculator, DollarSign, Calendar, Percent, Sparkles, 
  TrendingUp, ShieldCheck, ArrowRight, PieChart, Lock, CheckCircle2,
  Building2, ExternalLink, RefreshCw, GraduationCap, Clock, Award, Landmark, Shield
} from 'lucide-react';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';
import { useLanguage } from '../context/LanguageContext';
import { useApplication } from '../context/ApplicationContext';
import StepProgressIndicator from '../components/StepProgressIndicator';

/**
 * Deterministic Statutory Government Interest Rate Evaluator
 * Interest rate is FIXED by Gazette policy for each scheme, social category, and gender.
 */
export const getStatutoryGovernmentInterestRate = (schemeCode, category = 'General', gender = 'female', purposeType = 'EDUCATION') => {
  const code = String(schemeCode || '').toUpperCase();
  const cat = String(category || '').toUpperCase();
  const isFemale = String(gender || '').toLowerCase() === 'female' || String(gender || '').toLowerCase() === 'woman';
  const isSpecialCategory = ['SC', 'ST', 'OBC', 'MINORITY'].includes(cat) || isFemale;

  if (code === 'NMDFC-EDU' || code === 'NMDFC_EDU' || code === 'NMDFC') {
    return {
      rate: 3.0,
      display: '3.0% p.a.',
      badge: 'NMDFC Statutory Concession',
      reason: 'Mandated by Ministry of Minority Affairs (3% fixed concessional rate for notified minorities)'
    };
  }

  if (code === 'NSFDC-EDU' || code === 'NSFDC_EDU' || code === 'NSFDC_EL') {
    const rate = isFemale ? 3.5 : 4.0;
    return {
      rate: rate,
      display: `${rate}% p.a.`,
      badge: isFemale ? 'NSFDC Special Concession (3.5% Girl Student Quota)' : 'NSFDC SC Concession (4.0% Fixed)',
      reason: isFemale 
        ? 'Ministry of Social Justice: 3.5% p.a. concessional rate for SC female students' 
        : 'Ministry of Social Justice: 4.0% p.a. concessional rate for Scheduled Caste students'
    };
  }

  if (code === 'NBCFDC-EDU' || code === 'NBCFDC_EDU' || code === 'NBCFDC') {
    const rate = isFemale ? 3.5 : 4.0;
    return {
      rate: rate,
      display: `${rate}% p.a.`,
      badge: isFemale ? 'NBCFDC Special Concession (3.5% Girl Student Quota)' : 'NBCFDC OBC Concession (4.0% Fixed)',
      reason: isFemale 
        ? 'Ministry of Social Justice: 3.5% p.a. concessional rate for OBC girl students' 
        : 'Ministry of Social Justice: 4.0% p.a. concessional rate for OBC students'
    };
  }

  if (code === 'CSIS') {
    return {
      rate: 8.5,
      isSubvented: true,
      display: '8.5% p.a. (100% Full Govt Subvention)',
      badge: '100% CSIS Interest Subvention (₹0 Student Cost During Study)',
      reason: 'Ministry of Education: 100% full interest subsidy during course + 1-year moratorium for income <= Rs. 4.5L'
    };
  }

  if (code === 'AMBEDKAR-EDU' || code === 'AMBEDKAR_EDU') {
    return {
      rate: 8.5,
      isSubvented: true,
      display: '8.5% p.a. (100% Moratorium Subvention)',
      badge: 'Dr. Ambedkar Overseas 100% Interest Subsidy',
      reason: 'Ministry of Social Justice: 100% interest subvention for OBC/EBC overseas Masters & PhD'
    };
  }

  if (code === 'CGFSEL') {
    return {
      rate: 8.5,
      display: '8.5% p.a.',
      badge: 'IBA Model Scheme (NCGTC Guarantee)',
      reason: 'Collateral-free higher education loan up to Rs. 7.5L with 100% NCGTC credit guarantee'
    };
  }

  if (code === 'PM_VISHWAKARMA' || code === 'VISHWAKARMA') {
    return {
      rate: 5.0,
      display: '5.0% p.a. Fixed Concessional',
      badge: 'PM Vishwakarma Statutory Rate (8% Govt Subvention)',
      reason: 'Ministry of MSME: 5% fixed interest rate with 8% interest subvention borne by Central Govt'
    };
  }

  if (code === 'PM_SVANIDHI' || code === 'SVANIDHI') {
    return {
      rate: 7.0,
      display: '7.0% Interest Subvention (Effective ~2%)',
      badge: 'PM SVANidhi 7% Direct Subsidy',
      reason: 'Ministry of Housing & Urban Affairs: 7% interest subsidy directly credited to vendor bank account'
    };
  }

  if (code === 'MAHILA_SAMRIDHI' || code === 'MAHILA-SAMRIDHI') {
    return {
      rate: 4.0,
      display: '4.0% p.a. Fixed Concessional',
      badge: 'Mahila Samridhi Women Concession (4.0%)',
      reason: 'Ministry of Social Justice: 4% fixed rate for backward class women micro-entrepreneurs'
    };
  }

  if (code === 'STAND_UP_INDIA' || code === 'STANDUP-IND') {
    return {
      rate: 7.75,
      display: '7.75% p.a. (MCLR + CGSSI)',
      badge: 'Stand-Up India Statutory Cap',
      reason: 'Department of Financial Services: Lowest applicable bank rate for SC/ST and women greenfields'
    };
  }

  if (code.includes('MUDRA')) {
    return {
      rate: 8.0,
      display: '8.0% p.a.',
      badge: 'MUDRA Statutory Band (No Processing Fee)',
      reason: 'Pradhan Mantri Mudra Yojana: Collateral-free micro finance standard rate'
    };
  }

  if (code === 'PMEGP') {
    return {
      rate: 8.5,
      display: '8.5% p.a. (Bank Base Rate)',
      badge: isSpecialCategory ? 'PMEGP 35% Capital Margin Money Grant' : 'PMEGP 25% Capital Margin Money Grant',
      reason: isSpecialCategory 
        ? 'MoMSME: 35% capital subsidy for rural special category with bank base lending rate' 
        : 'MoMSME: 25% capital subsidy with bank base lending rate'
    };
  }

  // Default purpose fallback
  if (purposeType === 'EDUCATION') {
    return {
      rate: 8.5,
      display: '8.5% p.a. (IBA Education Base Rate)',
      badge: 'IBA Model Education Rate',
      reason: 'Standard Indian Banks Association (IBA) Education Loan Rate'
    };
  }

  return {
    rate: 8.5,
    display: '8.5% p.a. (Standard Bank Base Rate)',
    badge: 'Statutory Base Lending Rate',
    reason: 'Reserve Bank of India (RBI) Priority Sector Lending Guideline'
  };
};

export default function EmiCalculatorPage() {
  const { t } = useLanguage();
  const location = useLocation();
  const navigate = useNavigate();
  const { application, purposeType, selectedScheme, updateLoanAmount } = useApplication();

  const activeScheme = location.state?.selectedScheme || location.state?.scheme || selectedScheme;
  const isEducationScheme = (activeScheme?.purpose_type === 'EDUCATION') || (purposeType === 'EDUCATION');

  // Single source of truth loan amount
  const [loanAmount, setLoanAmount] = useState(
    location.state?.loanAmount || application.loanAmount || (isEducationScheme ? 450000 : 1200000)
  );

  // Determine fixed statutory interest rate based on scheme, caste/category, and gender
  const statutoryRateInfo = useMemo(() => {
    return getStatutoryGovernmentInterestRate(
      activeScheme?.scheme_code || activeScheme?.code || (isEducationScheme ? 'CSIS' : 'PMEGP'),
      application.social_category || application.category || 'General',
      application.gender || 'female',
      isEducationScheme ? 'EDUCATION' : (purposeType || 'BUSINESS')
    );
  }, [activeScheme, application.social_category, application.category, application.gender, isEducationScheme, purposeType]);

  const interestRate = statutoryRateInfo.rate;

  const getInitialSubsidy = () => {
    const code = (activeScheme?.scheme_code || activeScheme?.code || '').toUpperCase();
    if (code === 'CSIS' || code === 'AMBEDKAR-EDU') return 100;
    if (code === 'PMEGP') return 35;
    if (code === 'SVANIDHI' || code === 'PM_SVANIDHI') return 7;
    if (code === 'VISHWAKARMA' || code === 'PM_VISHWAKARMA') return 8;
    return isEducationScheme ? 0 : 25;
  };

  const getInitialTenure = () => {
    if (activeScheme?.repayment_period_months) {
      return Math.max(1, Math.round(activeScheme.repayment_period_months / 12));
    }
    return isEducationScheme ? 10 : 5;
  };

  const [tenureYears, setTenureYears] = useState(getInitialTenure());
  const [subsidyPercent, setSubsidyPercent] = useState(getInitialSubsidy());
  const [moratoriumMonths, setMoratoriumMonths] = useState(isEducationScheme ? 48 : 6);

  useEffect(() => {
    if (activeScheme) {
      setSubsidyPercent(getInitialSubsidy());
      setTenureYears(getInitialTenure());
      setMoratoriumMonths(activeScheme.moratorium_period_months || (isEducationScheme ? 48 : 6));
    }
  }, [activeScheme]);

  const handleLoanChange = (val) => {
    const num = Number(val);
    setLoanAmount(num);
    updateLoanAmount(num);
  };

  // Financial calculations
  const effectiveSubsidy = isEducationScheme ? 0 : (loanAmount * subsidyPercent) / 100;
  const netLoanAmount = isEducationScheme ? loanAmount : Math.max(0, loanAmount - effectiveSubsidy);

  const isCsisFullSubvention = isEducationScheme && (activeScheme?.scheme_code === 'CSIS' || subsidyPercent === 100 || statutoryRateInfo.isSubvented);
  const moratoriumSavings = isCsisFullSubvention ? Math.round((loanAmount * (interestRate / 100) * (moratoriumMonths / 12))) : 0;

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
      year: `${t('Year')} ${y}`,
      remainingBalance: Math.round(balance),
      principalPaid: Math.round(netLoanAmount - balance),
      interestPaid: Math.round(yearlyInterest * y)
    });
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 space-y-6">
      {/* Workflow Step Progress */}
      <StepProgressIndicator currentStep={6} />

      {/* Header Banner */}
      <div className="bg-gradient-to-r from-teal-800 via-emerald-800 to-slate-900 rounded-3xl p-6 sm:p-8 text-white shadow-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-2 max-w-2xl">
            <div className="flex flex-wrap items-center gap-2">
              <span className="bg-emerald-400/20 text-emerald-300 text-xs font-bold px-3 py-1 rounded-full border border-emerald-400/30 flex items-center gap-1.5">
                <ShieldCheck className="w-3.5 h-3.5" />
                <span>{isEducationScheme ? t('Statutory Education Loan Subvention') : t('Government Capital Subsidy & EMI Planner')}</span>
              </span>
              <span className="bg-blue-400/20 text-blue-200 text-xs font-mono font-bold px-2.5 py-0.5 rounded-full border border-blue-400/30">
                {application.social_category || application.category || 'SC'} Quota • {application.gender === 'female' ? t('Woman / Female') : t('Male')}
              </span>
            </div>
            <h1 className="text-2xl md:text-3xl font-black tracking-tight">
              {isEducationScheme ? t('Education Loan & Interest Subvention Calculator') : t('Dynamic EMI & Government Subsidy Calculator')}
            </h1>
            <p className="text-slate-200 text-xs sm:text-sm leading-relaxed">
              {isEducationScheme
                ? t('Official government-mandated interest subvention under CSIS, course moratorium timeline, and concessional post-study EMIs.')
                : t('Compute real-time capital margin money subsidy, net bank credit exposure, and monthly amortization schedule.')}
            </p>
          </div>

          {activeScheme && (
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-4 border border-white/20 text-left min-w-[220px] shrink-0">
              <span className="text-[10px] text-emerald-300 uppercase font-bold tracking-wider block">{t('Selected Scheme')}</span>
              <span className="text-sm font-black text-white line-clamp-1 mt-0.5">{t(activeScheme.scheme_name || activeScheme.name)}</span>
              <span className="text-xs text-emerald-400 font-mono font-bold mt-1 block">{activeScheme.scheme_code || activeScheme.code}</span>
            </div>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Controls Column (Left 4 Cols) */}
        <div className="lg:col-span-5 bg-white rounded-3xl p-6 shadow-sm border border-slate-200 space-y-6">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
              <Calculator className="h-5 w-5 text-emerald-600" />
              <span>{t('Loan Parameters')}</span>
            </h3>
            <span className="text-[11px] font-bold text-slate-400 font-mono">myScheme.gov.in</span>
          </div>

          {/* Loan Amount Input */}
          <div>
            <div className="flex justify-between items-center mb-1.5">
              <label className="text-xs font-bold text-slate-700 uppercase tracking-wider">
                {isEducationScheme ? t('Education Loan Required (₹)') : t('Sanctioned Loan Quantum (₹)')}
              </label>
              <span className="font-black text-emerald-700 text-sm">₹{loanAmount.toLocaleString('en-IN')}</span>
            </div>
            <input
              type="range"
              min={isEducationScheme ? 50000 : 25000}
              max={isEducationScheme ? 4000000 : 10000000}
              step={25000}
              value={loanAmount}
              onChange={(e) => handleLoanChange(e.target.value)}
              className="w-full accent-emerald-600 h-2 bg-slate-200 rounded-lg cursor-pointer"
            />
            <input
              type="number"
              value={loanAmount}
              onChange={(e) => handleLoanChange(e.target.value)}
              className="w-full mt-2 px-3 py-2 text-sm font-bold border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
            />
          </div>

          {/* FIXED STATUTORY GOVERNMENT INTEREST RATE (NON-EDITABLE) */}
          <div className="p-4 bg-slate-50 border-2 border-emerald-300 rounded-2xl space-y-2">
            <div className="flex items-center justify-between">
              <label className="text-xs font-bold text-slate-800 uppercase tracking-wider flex items-center gap-1.5">
                <Lock className="w-3.5 h-3.5 text-emerald-700" />
                <span>{t('Government Gazette Fixed Interest Rate')}</span>
              </label>
              <span className="text-xs font-black text-emerald-800 bg-emerald-100 border border-emerald-300 px-2.5 py-0.5 rounded-full">
                {statutoryRateInfo.display}
              </span>
            </div>
            
            <div className="p-2.5 bg-white rounded-xl border border-slate-200 text-xs space-y-1">
              <div className="flex items-center gap-1.5 text-emerald-900 font-bold">
                <ShieldCheck className="w-4 h-4 text-emerald-600 shrink-0" />
                <span>{statutoryRateInfo.badge}</span>
              </div>
              <p className="text-[11px] text-slate-600 leading-relaxed">
                {statutoryRateInfo.reason}
              </p>
              <span className="text-[10px] text-slate-400 block pt-0.5">
                * Locked by statutory policy — Not editable by borrower or commercial broker.
              </span>
            </div>
          </div>

          {/* Repayment Tenure */}
          <div>
            <div className="flex justify-between items-center mb-1.5">
              <label className="text-xs font-bold text-slate-700 uppercase tracking-wider">
                {t('Post-Moratorium Tenure (Years)')}
              </label>
              <span className="font-bold text-slate-900 text-sm">{tenureYears} {t('Years')}</span>
            </div>
            <input
              type="range"
              min={1}
              max={15}
              step={1}
              value={tenureYears}
              onChange={(e) => setTenureYears(Number(e.target.value))}
              className="w-full accent-emerald-600 h-2 bg-slate-200 rounded-lg cursor-pointer"
            />
          </div>

          {/* Moratorium / Subsidy Factor */}
          {isEducationScheme ? (
            <div className="bg-emerald-50 border border-emerald-200 rounded-2xl p-4 space-y-2">
              <div className="flex items-center gap-2">
                <GraduationCap className="h-4 w-4 text-emerald-700" />
                <span className="text-xs font-bold text-emerald-900 uppercase">{t('Moratorium Period')}</span>
              </div>
              <p className="text-xs text-emerald-800 leading-relaxed">
                {t('Course Duration')} (4 {t('Years')}) + 12 {t('Months')} {t('Grace')} = <strong>{moratoriumMonths} {t('Months')} {t('Moratorium')}</strong>.
              </p>
              {isCsisFullSubvention && (
                <div className="p-2 text-xs font-bold text-emerald-900 bg-emerald-100 rounded-xl border border-emerald-300 flex items-center gap-1.5">
                  <CheckCircle2 className="w-4 h-4 text-emerald-700 shrink-0" />
                  <span>{t('100% Full Govt Subvention: Student pays ₹0 interest during study!')}</span>
                </div>
              )}
            </div>
          ) : (
            <div>
              <div className="flex justify-between items-center mb-1.5">
                <label className="text-xs font-bold text-slate-700 uppercase tracking-wider">
                  {t('Government Subsidy / Margin Grant (%)')}
                </label>
                <span className="font-bold text-teal-700 text-sm">{subsidyPercent}%</span>
              </div>
              <input
                type="range"
                min={0}
                max={50}
                step={5}
                value={subsidyPercent}
                onChange={(e) => setSubsidyPercent(Number(e.target.value))}
                className="w-full accent-teal-600 h-2 bg-slate-200 rounded-lg cursor-pointer"
              />
            </div>
          )}

          {/* Next Action: Proceed to Channel Partners */}
          <button
            type="button"
            onClick={() => navigate('/partners', { state: { selectedScheme: activeScheme } })}
            className="w-full py-3 px-4 rounded-2xl font-bold text-sm bg-gradient-to-r from-emerald-600 to-teal-600 text-white hover:from-emerald-700 hover:to-teal-700 shadow-md flex items-center justify-center gap-2 transition-all cursor-pointer hover:scale-[1.01]"
          >
            <span>{t('Locate Processing Partner Branches')}</span>
            <ArrowRight className="h-4 w-4" />
          </button>
        </div>

        {/* Breakdown & Analytics Column (Right 7 Cols) */}
        <div className="lg:col-span-7 space-y-6">
          {/* 3 Metric Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="bg-white p-5 rounded-3xl border border-slate-200 shadow-sm">
              <span className="text-xs font-bold text-slate-500 block uppercase">{t('Monthly EMI')}</span>
              <span className="text-2xl font-black text-slate-900 mt-1 block">₹{Math.round(calculatedEmi).toLocaleString('en-IN')}</span>
              <span className="text-[11px] text-emerald-600 font-semibold">{tenureYears * 12} {t('monthly installments')}</span>
            </div>

            <div className="bg-white p-5 rounded-3xl border border-slate-200 shadow-sm">
              <span className="text-xs font-bold text-slate-500 block uppercase">{t('Total Interest')}</span>
              <span className="text-2xl font-black text-amber-600 mt-1 block">₹{Math.round(totalInterest).toLocaleString('en-IN')}</span>
              <span className="text-[11px] text-slate-400 font-medium">{t('At fixed statutory rate')}</span>
            </div>

            <div className="bg-white p-5 rounded-3xl border border-slate-200 shadow-sm">
              <span className="text-xs font-bold text-slate-500 block uppercase">
                {isEducationScheme ? t('Moratorium Savings') : t('Capital Subsidy')}
              </span>
              <span className="text-2xl font-black text-emerald-700 mt-1 block">
                ₹{(isEducationScheme ? moratoriumSavings : effectiveSubsidy).toLocaleString('en-IN')}
              </span>
              <span className="text-[11px] text-emerald-600 font-semibold">
                {isEducationScheme ? t('100% Govt Reimbursed') : `${subsidyPercent}% Grant`}
              </span>
            </div>
          </div>

          {/* Amortization Schedule Chart */}
          <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="font-black text-slate-900 text-base">{t('Amortization Schedule')}</h3>
              <span className="text-xs font-mono font-bold text-slate-500">{t('Principle vs Interest Balance')}</span>
            </div>

            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={chartData} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                  <defs>
                    <linearGradient id="colorBal" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#10b981" stopOpacity={0.8}/>
                      <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                    </linearGradient>
                    <linearGradient id="colorInt" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.8}/>
                      <stop offset="95%" stopColor="#f59e0b" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                  <XAxis dataKey="year" tick={{ fontSize: 11 }} />
                  <YAxis tick={{ fontSize: 11 }} tickFormatter={(v) => `₹${(v/100000).toFixed(1)}L`} />
                  <Tooltip formatter={(value) => [`₹${Number(value).toLocaleString('en-IN')}`, '']} />
                  <Area type="monotone" dataKey="remainingBalance" name={t('Remaining Balance')} stroke="#10b981" fillOpacity={1} fill="url(#colorBal)" />
                  <Area type="monotone" dataKey="interestPaid" name={t('Interest Paid')} stroke="#f59e0b" fillOpacity={1} fill="url(#colorInt)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
