import React, { useState } from 'react';
import { 
  ShieldCheck, 
  Plus, 
  Sliders, 
  CheckCircle2, 
  XCircle, 
  AlertTriangle, 
  Edit3, 
  Trash2, 
  Power, 
  Play, 
  Sparkles, 
  BookOpen, 
  Layers, 
  Scale, 
  Check, 
  RefreshCw,
  Info,
  ChevronRight,
  TrendingUp,
  Percent,
  FileCheck
} from 'lucide-react';

const INITIAL_SCHEMES = [
  { code: 'PMEGP', name: "Prime Minister's Employment Generation Programme", ministry: 'Ministry of MSME / KVIC', maxSubsidy: '35%', maxLoan: '₹50 Lakhs' },
  { code: 'STANDUP-IND', name: 'Stand-Up India Scheme', ministry: 'Ministry of Finance / SIDBI', maxSubsidy: 'Composite Loan', maxLoan: '₹100 Lakhs' },
  { code: 'SVANIDHI', name: "PM Street Vendor's AtmaNirbhar Nidhi (PM SVANidhi)", ministry: 'Ministry of Housing and Urban Affairs', maxSubsidy: '7% Interest Subsidy', maxLoan: '₹50,000' },
  { code: 'CSIS-EDU', name: 'Central Sector Interest Subsidy for Education Loans', ministry: 'Ministry of Education', maxSubsidy: '100% Moratorium Interest', maxLoan: '₹10 Lakhs' },
  { code: 'PM-VISHWAKARMA', name: 'PM Vishwakarma Artisan Support', ministry: 'Ministry of MSME', maxSubsidy: '5% Concessional Interest + ₹15k Tool Kit', maxLoan: '₹3 Lakhs' },
  { code: 'NSFDC-EDU', name: 'NSFDC Backward Classes Higher Education Scheme', ministry: 'Ministry of Social Justice', maxSubsidy: 'Concessional 4% Interest', maxLoan: '₹20 Lakhs' }
];

const INITIAL_RULES = [
  {
    id: 1,
    scheme: 'PMEGP',
    code: 'PMEGP_RULE_01',
    name: 'Special Category & Demographic Subsidy Gate',
    target: 'SC / ST / OBC / Minority / Female / Divyangjan / Ex-Servicemen',
    condition: "user.social_category in ['SC','ST','OBC','Minority','Divyangjan','Ex-Servicemen'] or user.gender == 'female'",
    rule_type: 'Target Subsidy Gate',
    weight: 30,
    is_active: true,
    description: 'Applicant belongs to statutory Special Category or is a Woman Entrepreneur.',
    statutory_note: 'Grants 35% Special Rural or 25% Special Urban margin subsidy with only 5% promoter contribution (General Male receives 25% Rural / 15% Urban with 10% contribution).',
    failure_msg: 'Applicant classified as General Category Male; qualifies for Standard General Subsidy bracket (25% Rural / 15% Urban).'
  },
  {
    id: 2,
    scheme: 'PMEGP',
    code: 'PMEGP_RULE_02',
    name: 'Manufacturing Sector Project Cost Ceiling',
    target: 'Manufacturing Enterprises',
    condition: "user.business_type == 'manufacturing' and user.project_cost <= 5000000",
    rule_type: 'Statutory Quantum Cap',
    weight: 25,
    is_active: true,
    description: 'Project cost for new manufacturing enterprises must not exceed ₹50,00,000.',
    statutory_note: 'Gazette MSME ceiling under PMEGP 2022 revised guidelines is ₹50 Lakhs for manufacturing units.',
    failure_msg: 'Project cost exceeds maximum statutory limit of ₹50,00,000 for manufacturing projects.'
  },
  {
    id: 3,
    scheme: 'PMEGP',
    code: 'PMEGP_RULE_03',
    name: 'Service & Business Sector Cost Ceiling',
    target: 'Service / Trading Enterprises',
    condition: "user.business_type in ['service','trading'] and user.project_cost <= 2000000",
    rule_type: 'Statutory Quantum Cap',
    weight: 20,
    is_active: true,
    description: 'Project cost for service and trading ventures must not exceed ₹20,00,000.',
    statutory_note: 'Statutory ceiling under KVIC guidelines is ₹20 Lakhs for service sector establishments.',
    failure_msg: 'Project cost exceeds maximum limit of ₹20,00,000 for service/trading activities.'
  },
  {
    id: 4,
    scheme: 'PMEGP',
    code: 'PMEGP_RULE_04',
    name: 'Statutory Minimum Age Requirement',
    target: 'Individual Beneficiaries',
    condition: "user.age >= 18",
    rule_type: 'Legal Eligibility Filter',
    weight: 15,
    is_active: true,
    description: 'The applicant must be at least 18 years of age at the time of application.',
    statutory_note: 'No upper age limit is mandated under PMEGP guidelines.',
    failure_msg: 'Applicant must be at least 18 years old to apply for PMEGP loan assistance.'
  },
  {
    id: 5,
    scheme: 'PMEGP',
    code: 'PMEGP_RULE_05',
    name: 'Educational Qualification for High-Quantum Projects',
    target: 'Projects > ₹10L (Mfg) or > ₹5L (Service)',
    condition: "(user.business_type == 'manufacturing' and user.project_cost > 1000000 and user.education in ['8th','10th','12th','graduate','post_graduate']) or (user.business_type in ['service','trading'] and user.project_cost > 500000 and user.education in ['8th','10th','12th','graduate','post_graduate']) or (user.business_type == 'manufacturing' and user.project_cost <= 1000000) or (user.business_type in ['service','trading'] and user.project_cost <= 500000)",
    rule_type: 'Academic Prerequisite',
    weight: 15,
    is_active: true,
    description: 'At least 8th standard pass is mandatory for manufacturing projects > ₹10 Lakhs and service projects > ₹5 Lakhs.',
    statutory_note: 'For smaller projects (≤ ₹10L Mfg, ≤ ₹5L Service), no formal educational qualification is mandated.',
    failure_msg: 'Minimum 8th pass educational certificate is mandatory for project cost above ₹10 Lakhs (Mfg) or ₹5 Lakhs (Service).'
  },
  {
    id: 6,
    scheme: 'PMEGP',
    code: 'PMEGP_RULE_06',
    name: 'New Greenfield Enterprise Exclusivity',
    target: 'New Enterprise Setups',
    condition: "user.business_stage in ['New Greenfield Enterprise','idea_stage','planning','new_unit']",
    rule_type: 'Unit Classification',
    weight: 10,
    is_active: true,
    description: 'Assistance under 1st loan is granted exclusively for setting up new greenfield units.',
    statutory_note: 'Existing units are not eligible for 1st loan subsidy (eligible only for 2nd loan upgradation).',
    failure_msg: 'PMEGP 1st loan subsidy is strictly restricted to new greenfield enterprise establishment.'
  },
  {
    id: 7,
    scheme: 'PMEGP',
    code: 'PMEGP_RULE_07',
    name: 'Promoter Margin Money Equity Contribution',
    target: 'All Beneficiaries',
    condition: "(user.social_category in ['SC','ST','OBC','Minority','Woman'] or user.gender == 'female' ? user.own_contribution_pct >= 5 : user.own_contribution_pct >= 10)",
    rule_type: 'Margin Money Compliance',
    weight: 10,
    is_active: true,
    description: 'Promoter must invest minimum 5% (Special/Women) or 10% (General Male) of project cost.',
    statutory_note: 'Balance 90% to 95% is funded via bank loan and KVIC margin subsidy.',
    failure_msg: 'Own contribution is below the statutory requirement (5% for Special/Women, 10% for General).'
  },
  {
    id: 8,
    scheme: 'PMEGP',
    code: 'PMEGP_RULE_08',
    name: 'Mandatory EDP Entrepreneurship Training',
    target: 'All Sanctioned Applicants',
    condition: "user.has_skill_training == true or user.edp_undertaking == true",
    rule_type: 'Capacity Building',
    weight: 10,
    is_active: true,
    description: '10-day EDP skill training completion or formal undertaking before loan disbursement.',
    statutory_note: 'EDP training through RSETI / KVIC / MSME-DI is mandatory before releasing 2nd installment of loan.',
    failure_msg: 'Applicant must have completed EDP training or agreed to submit the mandatory undertaking.'
  },
  {
    id: 9,
    scheme: 'PMEGP',
    code: 'PMEGP_RULE_09',
    name: 'KVIC Negative List Industry Exclusion',
    target: 'All Project Activities',
    condition: "user.industry_sector not in ['meat_slaughter', 'tobacco_bidi_liquor', 'polythene_carrybags_under_75microns', 'rural_transport_auto']",
    rule_type: 'Negative List Filter',
    weight: 15,
    is_active: true,
    description: 'Project activity must not fall in the KVIC Negative List of prohibited industries.',
    statutory_note: 'Activities producing tobacco, intoxicants, meat processing, or thin polythene bags are barred.',
    failure_msg: 'Selected industry activity is prohibited under KVIC PMEGP Negative List.'
  },
  // STANDUP INDIA RULES
  {
    id: 10,
    scheme: 'STANDUP-IND',
    code: 'STANDUP_RULE_01',
    name: 'SC/ST or Woman Entrepreneur Priority',
    target: 'SC / ST / Women Promoters',
    condition: "user.social_category in ['SC','ST'] or user.gender == 'female'",
    rule_type: 'Target Demographic Gate',
    weight: 40,
    is_active: true,
    description: 'Promoter must be SC, ST, or a Woman entrepreneur (holding min 51% stake in enterprise).',
    statutory_note: 'Stand-Up India mandates at least 1 SC/ST borrower and 1 Woman borrower per bank branch.',
    failure_msg: 'Stand-Up India is exclusively open to SC, ST, or Woman entrepreneurs.'
  },
  {
    id: 11,
    scheme: 'STANDUP-IND',
    code: 'STANDUP_RULE_02',
    name: 'Composite Loan Quantum Window',
    target: 'All Stand-Up India Units',
    condition: "user.project_cost >= 1000000 and user.project_cost <= 10000000",
    rule_type: 'Statutory Quantum Cap',
    weight: 35,
    is_active: true,
    description: 'Loan quantum must range strictly between ₹10 Lakhs and ₹100 Lakhs (₹1 Crore).',
    statutory_note: 'Covers composite loans comprising term loan and working capital.',
    failure_msg: 'Loan requirement is outside the ₹10 Lakh to ₹100 Lakh statutory bracket.'
  },
  // PM SVANIDHI RULES
  {
    id: 12,
    scheme: 'SVANIDHI',
    code: 'SVANIDHI_RULE_01',
    name: 'Urban Street Vendor Certification / Vending Certificate',
    target: 'Urban Street Vendors',
    condition: "user.is_street_vendor == true and user.has_vending_certificate == true",
    rule_type: 'Target Demographic Gate',
    weight: 40,
    is_active: true,
    description: 'Beneficiary must be a certified urban street vendor possessing a ULB recommendation or vending ID.',
    statutory_note: 'Provides collateral-free working capital micro-loans with 7% interest subsidy on regular repayment.',
    failure_msg: 'Urban Local Body (ULB) vending card or recommendation letter is required.'
  },
  {
    id: 13,
    scheme: 'SVANIDHI',
    code: 'SVANIDHI_RULE_02',
    name: '1st Tranche Micro-Loan Quantum Cap',
    target: 'Initial Working Capital',
    condition: "user.project_cost <= 10000 or user.project_cost <= 50000",
    rule_type: 'Statutory Quantum Cap',
    weight: 30,
    is_active: true,
    description: 'Loan amounts are stepped: 1st tranche ₹10,000, 2nd tranche ₹20,000, 3rd tranche ₹50,000.',
    statutory_note: 'No collateral or margin money required from the vendor.',
    failure_msg: 'Initial tranche exceeds the permissible micro-loan ceiling.'
  }
];

export default function AdminRuleManagement() {
  const [rules, setRules] = useState(INITIAL_RULES);
  const [selectedScheme, setSelectedScheme] = useState('PMEGP');
  const [modalOpen, setModalOpen] = useState(false);
  const [modalMode, setModalMode] = useState('add'); // 'add' or 'edit'
  const [activeRule, setActiveRule] = useState(null);
  const [toast, setToast] = useState(null);

  // Sandbox simulation state
  const [sandbox, setSandbox] = useState({
    gender: 'female',
    social_category: 'OBC',
    area: 'rural',
    business_type: 'manufacturing',
    project_cost: 2500000,
    age: 28,
    education: '10th',
    business_stage: 'New Greenfield Enterprise',
    own_contribution_pct: 10,
    has_skill_training: true,
    edp_undertaking: true,
    industry_sector: 'food_processing',
    is_street_vendor: false,
    has_vending_certificate: false
  });

  const showToast = (msg, type = 'success') => {
    setToast({ msg, type });
    setTimeout(() => setToast(null), 4000);
  };

  const schemeRules = rules.filter(r => r.scheme === selectedScheme);
  const currentSchemeMeta = INITIAL_SCHEMES.find(s => s.code === selectedScheme) || INITIAL_SCHEMES[0];

  // Open modal for ADD
  const handleOpenAdd = () => {
    setModalMode('add');
    setActiveRule({
      scheme: selectedScheme,
      code: `${selectedScheme}_RULE_${String(schemeRules.length + 1).padStart(2, '0')}`,
      name: '',
      target: '',
      condition: '',
      rule_type: 'Weighted Metric',
      weight: 15,
      is_active: true,
      description: '',
      statutory_note: '',
      failure_msg: ''
    });
    setModalOpen(true);
  };

  // Open modal for EDIT
  const handleOpenEdit = (rule) => {
    setModalMode('edit');
    setActiveRule({ ...rule });
    setModalOpen(true);
  };

  // Toggle rule status
  const handleToggleStatus = (id) => {
    setRules(prev => prev.map(r => {
      if (r.id === id) {
        const newStatus = !r.is_active;
        showToast(`Rule "${r.name}" is now ${newStatus ? 'Active' : 'Disabled'}.`, newStatus ? 'success' : 'info');
        return { ...r, is_active: newStatus };
      }
      return r;
    }));
  };

  // Delete rule
  const handleDeleteRule = (id) => {
    const target = rules.find(r => r.id === id);
    if (window.confirm(`Are you sure you want to delete "${target?.name}"?`)) {
      setRules(prev => prev.filter(r => r.id !== id));
      showToast(`Rule "${target?.name}" deleted.`, 'info');
    }
  };

  // Save rule from modal
  const handleSaveRule = (e) => {
    e.preventDefault();
    if (!activeRule.name || !activeRule.condition) {
      alert('Please provide Rule Name and Condition expression.');
      return;
    }

    if (modalMode === 'add') {
      const newId = Math.max(...rules.map(r => r.id), 0) + 1;
      const created = { ...activeRule, id: newId };
      setRules(prev => [...prev, created]);
      showToast(`New rule "${created.name}" created successfully.`);
    } else {
      setRules(prev => prev.map(r => r.id === activeRule.id ? activeRule : r));
      showToast(`Rule "${activeRule.name}" updated successfully.`);
    }
    setModalOpen(false);
  };

  // Evaluate single rule against sandbox
  const evaluateRule = (rule) => {
    if (!rule.is_active) return { evaluated: false, status: 'disabled', message: 'Rule disabled' };
    
    const u = sandbox;
    try {
      if (rule.scheme === 'PMEGP') {
        if (rule.code.includes('01') || rule.name.includes('Special Category')) {
          const isSpecial = ['SC', 'ST', 'OBC', 'Minority', 'Divyangjan', 'Ex-Servicemen'].includes(u.social_category) || u.gender === 'female';
          return {
            evaluated: true,
            passed: isSpecial,
            score: isSpecial ? rule.weight : 0,
            badge: isSpecial ? 'Special Category Subsidy (35% Rural / 25% Urban)' : 'General Category Bracket (25% Rural / 15% Urban)',
            message: isSpecial ? 'Passed: Eligible for 35% Max Special Margin Subsidy' : 'Notice: General Male bracket applies (25% Rural / 15% Urban)'
          };
        }
        if (rule.code.includes('02') || rule.name.includes('Manufacturing')) {
          if (u.business_type !== 'manufacturing') {
            return { evaluated: true, passed: true, score: rule.weight, message: 'N/A: Non-manufacturing track' };
          }
          const ok = u.project_cost <= 5000000;
          return {
            evaluated: true,
            passed: ok,
            score: ok ? rule.weight : 0,
            message: ok ? `Passed: ₹${(u.project_cost / 100000).toFixed(2)}L <= ₹50 Lakhs limit` : `Failed: Project cost ₹${(u.project_cost / 100000).toFixed(2)}L exceeds ₹50L ceiling`
          };
        }
        if (rule.code.includes('03') || rule.name.includes('Service')) {
          if (u.business_type === 'manufacturing') {
            return { evaluated: true, passed: true, score: rule.weight, message: 'N/A: Manufacturing track' };
          }
          const ok = u.project_cost <= 2000000;
          return {
            evaluated: true,
            passed: ok,
            score: ok ? rule.weight : 0,
            message: ok ? `Passed: ₹${(u.project_cost / 100000).toFixed(2)}L <= ₹20 Lakhs limit` : `Failed: Project cost ₹${(u.project_cost / 100000).toFixed(2)}L exceeds ₹20L ceiling`
          };
        }
        if (rule.code.includes('04') || rule.name.includes('Age')) {
          const ok = u.age >= 18;
          return {
            evaluated: true,
            passed: ok,
            score: ok ? rule.weight : 0,
            message: ok ? `Passed: Age ${u.age} >= 18 years` : `Failed: Age ${u.age} is below 18 years`
          };
        }
        if (rule.code.includes('05') || rule.name.includes('Educational')) {
          const requiresEdu = (u.business_type === 'manufacturing' && u.project_cost > 1000000) || (u.business_type !== 'manufacturing' && u.project_cost > 500000);
          if (!requiresEdu) {
            return { evaluated: true, passed: true, score: rule.weight, message: 'Passed: Project quantum <= exemption ceiling (No min edu required)' };
          }
          const ok = ['8th', '10th', '12th', 'graduate', 'post_graduate'].includes(u.education);
          return {
            evaluated: true,
            passed: ok,
            score: ok ? rule.weight : 0,
            message: ok ? `Passed: ${u.education} meets min 8th standard pass requirement` : 'Failed: Minimum 8th standard pass required for this loan quantum'
          };
        }
        if (rule.code.includes('06') || rule.name.includes('Greenfield')) {
          const ok = ['New Greenfield Enterprise', 'idea_stage', 'planning', 'new_unit'].includes(u.business_stage);
          return {
            evaluated: true,
            passed: ok,
            score: ok ? rule.weight : 0,
            message: ok ? 'Passed: Greenfield new enterprise project' : 'Failed: Only new greenfield enterprises eligible for 1st loan subsidy'
          };
        }
        if (rule.code.includes('07') || rule.name.includes('Margin')) {
          const isSpecial = ['SC', 'ST', 'OBC', 'Minority', 'Divyangjan', 'Ex-Servicemen'].includes(u.social_category) || u.gender === 'female';
          const requiredPct = isSpecial ? 5 : 10;
          const ok = u.own_contribution_pct >= requiredPct;
          return {
            evaluated: true,
            passed: ok,
            score: ok ? rule.weight : 0,
            message: ok ? `Passed: ${u.own_contribution_pct}% meets ${requiredPct}% required promoter equity` : `Failed: Own contribution ${u.own_contribution_pct}% < ${requiredPct}% required`
          };
        }
        if (rule.code.includes('08') || rule.name.includes('EDP')) {
          const ok = u.has_skill_training || u.edp_undertaking;
          return {
            evaluated: true,
            passed: ok,
            score: ok ? rule.weight : 0,
            message: ok ? 'Passed: EDP training / statutory undertaking satisfied' : 'Failed: EDP training or undertaking required'
          };
        }
        if (rule.code.includes('09') || rule.name.includes('Negative')) {
          const negativeList = ['meat_slaughter', 'tobacco_bidi_liquor', 'polythene_carrybags_under_75microns', 'rural_transport_auto'];
          const ok = !negativeList.includes(u.industry_sector);
          return {
            evaluated: true,
            passed: ok,
            score: ok ? rule.weight : 0,
            message: ok ? `Passed: ${u.industry_sector} is KVIC approved activity` : 'Failed: Industry falls in prohibited Negative List'
          };
        }
      }
      return { evaluated: true, passed: true, score: rule.weight, message: 'Condition met successfully' };
    } catch {
      return { evaluated: false, passed: false, score: 0, message: 'Evaluation syntax error' };
    }
  };

  // Sandbox calculations
  const activeSchemeRules = schemeRules.filter(r => r.is_active);
  const evaluationResults = schemeRules.map(r => ({
    rule: r,
    result: evaluateRule(r)
  }));

  const totalPossibleWeight = activeSchemeRules.reduce((sum, r) => sum + r.weight, 0);
  const earnedScore = evaluationResults
    .filter(e => e.rule.is_active && e.result.passed)
    .reduce((sum, e) => sum + e.result.score, 0);
  const matchPercentage = totalPossibleWeight > 0 ? Math.round((earnedScore / totalPossibleWeight) * 100) : 0;

  // PMEGP Subsidy Rate calculation
  const isSpecialDemographic = ['SC', 'ST', 'OBC', 'Minority', 'Divyangjan', 'Ex-Servicemen'].includes(sandbox.social_category) || sandbox.gender === 'female';
  const isRural = sandbox.area === 'rural';
  let subsidyPct = 15;
  let ownContributionReq = 10;
  if (isSpecialDemographic && isRural) {
    subsidyPct = 35;
    ownContributionReq = 5;
  } else if (isSpecialDemographic && !isRural) {
    subsidyPct = 25;
    ownContributionReq = 5;
  } else if (!isSpecialDemographic && isRural) {
    subsidyPct = 25;
    ownContributionReq = 10;
  } else {
    subsidyPct = 15;
    ownContributionReq = 10;
  }

  const calculatedMaxSubsidyAmount = Math.round((sandbox.project_cost * subsidyPct) / 100);
  const calculatedPromoterEquity = Math.round((sandbox.project_cost * ownContributionReq) / 100);
  const calculatedBankLoanAmount = sandbox.project_cost - calculatedPromoterEquity;

  return (
    <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 space-y-8 font-sans text-slate-900">
      
      {/* Toast Notification */}
      {toast && (
        <div className={`fixed top-5 right-5 z-50 px-4 py-3 rounded-xl shadow-xl border flex items-center gap-3 transition-all animate-bounce ${
          toast.type === 'success' ? 'bg-emerald-900 text-white border-emerald-700' : 'bg-slate-900 text-white border-slate-700'
        }`}>
          <CheckCircle2 className="w-5 h-5 text-emerald-400" />
          <span className="text-sm font-semibold">{toast.msg}</span>
        </div>
      )}

      {/* Header Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 rounded-3xl p-6 sm:p-8 text-white shadow-xl relative overflow-hidden border border-slate-800">
        <div className="absolute -right-10 -bottom-10 w-72 h-72 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="space-y-2">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 text-xs font-bold uppercase tracking-wider border border-emerald-500/30">
              <ShieldCheck className="w-3.5 h-3.5" /> Admin Rule Engine Center
            </div>
            <h1 className="text-2xl sm:text-3xl font-black tracking-tight text-white">
              Deterministic Rule Engine &amp; Policy Matrix
            </h1>
            <p className="text-slate-300 text-sm max-w-2xl">
              Inspect, customize, test, and dynamically configure mathematical eligibility predicates, demographic criteria, project caps, and weights against official Government Gazette parameters.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <button
              onClick={handleOpenAdd}
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-sm shadow-lg shadow-emerald-500/20 transition-all active:scale-95 cursor-pointer"
            >
              <Plus className="w-4 h-4 stroke-[3]" /> Add New Rule
            </button>
          </div>
        </div>
      </div>

      {/* Scheme Selector Tabs */}
      <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-thin">
        {INITIAL_SCHEMES.map((scheme) => (
          <button
            key={scheme.code}
            onClick={() => setSelectedScheme(scheme.code)}
            className={`px-4 py-2.5 rounded-xl font-bold text-xs shrink-0 transition-all flex items-center gap-2 cursor-pointer ${
              selectedScheme === scheme.code
                ? 'bg-emerald-600 text-white shadow-md shadow-emerald-600/30 scale-[1.02]'
                : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200'
            }`}
          >
            <span className="font-mono font-black text-xs">{scheme.code}</span>
            <span className="hidden sm:inline font-medium opacity-90">| {scheme.name.split(' ')[0]}...</span>
            <span className={`px-1.5 py-0.5 rounded text-[10px] ${
              selectedScheme === scheme.code ? 'bg-emerald-700 text-emerald-100' : 'bg-slate-100 text-slate-500'
            }`}>
              {rules.filter(r => r.scheme === scheme.code).length}
            </span>
          </button>
        ))}
      </div>

      {/* Scheme Quick Information Card */}
      <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-1 rounded-lg bg-indigo-100 text-indigo-800 font-mono text-xs font-black">
              {currentSchemeMeta.code}
            </span>
            <h2 className="font-bold text-slate-900 text-lg">{currentSchemeMeta.name}</h2>
          </div>
          <p className="text-xs text-slate-500 flex items-center gap-1.5">
            <BookOpen className="w-3.5 h-3.5 text-slate-400" /> Authority: {currentSchemeMeta.ministry}
          </p>
        </div>

        <div className="flex items-center gap-6 divide-x divide-slate-100 text-xs">
          <div className="px-3 space-y-0.5">
            <span className="text-slate-400 font-semibold block text-[10px] uppercase tracking-wider">Max Subsidy</span>
            <span className="font-black text-emerald-600 text-sm">{currentSchemeMeta.maxSubsidy}</span>
          </div>
          <div className="px-3 space-y-0.5">
            <span className="text-slate-400 font-semibold block text-[10px] uppercase tracking-wider">Max Quantum</span>
            <span className="font-black text-slate-900 text-sm">{currentSchemeMeta.maxLoan}</span>
          </div>
          <div className="px-3 space-y-0.5">
            <span className="text-slate-400 font-semibold block text-[10px] uppercase tracking-wider">Active Rules</span>
            <span className="font-black text-indigo-600 text-sm">
              {schemeRules.filter(r => r.is_active).length} / {schemeRules.length}
            </span>
          </div>
        </div>
      </div>

      {/* Grid: Left = Rules List, Right = Live Simulator */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Left Column: Rules List (7 Cols) */}
        <div className="lg:col-span-7 space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Sliders className="w-4 h-4 text-emerald-600" />
              <h3 className="font-black text-slate-900 text-base">
                Configured Statutory Rules ({schemeRules.length})
              </h3>
            </div>
            <button 
              onClick={handleOpenAdd}
              className="text-xs font-bold text-emerald-700 hover:text-emerald-800 flex items-center gap-1 bg-emerald-50 hover:bg-emerald-100 px-2.5 py-1 rounded-lg border border-emerald-200 transition-colors cursor-pointer"
            >
              <Plus className="w-3.5 h-3.5" /> Add Rule
            </button>
          </div>

          <div className="space-y-3">
            {schemeRules.map((rule, idx) => (
              <div 
                key={rule.id}
                className={`bg-white rounded-2xl border transition-all duration-200 p-5 shadow-sm space-y-3.5 ${
                  rule.is_active 
                    ? 'border-slate-200 hover:border-emerald-300 hover:shadow-md' 
                    : 'border-dashed border-slate-200 bg-slate-50/70 opacity-75'
                }`}
              >
                {/* Rule Card Header */}
                <div className="flex items-start justify-between gap-3">
                  <div className="space-y-1">
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="font-mono text-xs font-black text-slate-600 bg-slate-100 px-2 py-0.5 rounded border border-slate-200">
                        Rule {idx + 1}
                      </span>
                      <span className="font-mono text-[11px] font-bold text-indigo-700 bg-indigo-50 px-2 py-0.5 rounded border border-indigo-100">
                        {rule.code}
                      </span>
                      <span className={`text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full ${
                        rule.is_active ? 'bg-emerald-100 text-emerald-800' : 'bg-slate-200 text-slate-600'
                      }`}>
                        {rule.is_active ? '● Active' : '○ Disabled'}
                      </span>
                      <span className="text-[10px] font-semibold text-slate-500 bg-slate-100 px-2 py-0.5 rounded">
                        {rule.rule_type}
                      </span>
                    </div>

                    <h4 className="font-black text-slate-900 text-base pt-0.5">
                      {rule.name}
                    </h4>
                  </div>

                  {/* Weight Gauge */}
                  <div className="text-right shrink-0 bg-emerald-50 border border-emerald-100 px-3 py-1.5 rounded-xl">
                    <span className="text-[10px] uppercase font-bold text-emerald-800 block tracking-wider">Weight</span>
                    <span className="font-black text-emerald-700 text-base">{rule.weight}%</span>
                  </div>
                </div>

                {/* Target & Description */}
                {rule.target && (
                  <div className="text-xs text-slate-700 flex items-center gap-1.5 font-medium">
                    <span className="font-bold text-slate-500 uppercase text-[10px] tracking-wider">Target:</span>
                    <span className="bg-amber-50 text-amber-900 border border-amber-200/60 px-2 py-0.5 rounded font-semibold text-xs">
                      {rule.target}
                    </span>
                  </div>
                )}

                {/* Condition Expression */}
                <div className="space-y-1">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block">
                    Mathematical Condition / Predicate
                  </span>
                  <div className="p-2.5 rounded-xl bg-slate-900 text-emerald-400 font-mono text-xs overflow-x-auto shadow-inner border border-slate-800">
                    <code>{rule.condition}</code>
                  </div>
                </div>

                {/* Statutory Note */}
                {rule.statutory_note && (
                  <p className="text-xs text-slate-600 bg-slate-50 p-2.5 rounded-xl border border-slate-100 flex items-start gap-2">
                    <Info className="w-3.5 h-3.5 text-indigo-500 shrink-0 mt-0.5" />
                    <span>{rule.statutory_note}</span>
                  </p>
                )}

                {/* Action Buttons: [ Edit ] [ Disable / Enable ] [ Delete ] */}
                <div className="flex flex-wrap items-center justify-between pt-2 border-t border-slate-100 gap-2">
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handleToggleStatus(rule.id)}
                      className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition-all cursor-pointer ${
                        rule.is_active
                          ? 'bg-amber-50 text-amber-800 hover:bg-amber-100 border border-amber-200'
                          : 'bg-emerald-50 text-emerald-800 hover:bg-emerald-100 border border-emerald-200'
                      }`}
                    >
                      <Power className="w-3 h-3" />
                      {rule.is_active ? 'Disable Rule' : 'Enable Rule'}
                    </button>
                    
                    <button
                      onClick={() => handleOpenEdit(rule)}
                      className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold bg-slate-100 text-slate-700 hover:bg-slate-200 border border-slate-200 transition-all cursor-pointer"
                    >
                      <Edit3 className="w-3 h-3" /> Edit
                    </button>
                  </div>

                  <button
                    onClick={() => handleDeleteRule(rule.id)}
                    className="inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs font-bold text-rose-600 hover:bg-rose-50 border border-transparent hover:border-rose-200 transition-all cursor-pointer"
                  >
                    <Trash2 className="w-3 h-3" /> Delete
                  </button>
                </div>

              </div>
            ))}
          </div>
        </div>

        {/* Right Column: Live Deterministic Simulator (5 Cols) */}
        <div className="lg:col-span-5 space-y-6">
          
          <div className="bg-white rounded-3xl p-6 border border-slate-200 shadow-md space-y-6 sticky top-6">
            
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <div className="flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-emerald-600" />
                <h3 className="font-black text-slate-900 text-base">
                  Live Rule Simulator
                </h3>
              </div>
              <span className="px-2 py-0.5 rounded text-[10px] font-black uppercase tracking-wider bg-emerald-100 text-emerald-800">
                Sandbox Mode
              </span>
            </div>

            {/* Simulated Applicant Input Controls */}
            <div className="space-y-4 text-xs">
              
              {/* Gender & Category */}
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="font-bold text-slate-700 block mb-1">Gender</label>
                  <select 
                    value={sandbox.gender}
                    onChange={(e) => setSandbox({ ...sandbox, gender: e.target.value })}
                    className="w-full p-2 rounded-xl border border-slate-200 font-semibold bg-slate-50 focus:ring-2 focus:ring-emerald-500 focus:bg-white outline-none"
                  >
                    <option value="female">Female (Special)</option>
                    <option value="male">Male (General)</option>
                    <option value="other">Other / Transgender</option>
                  </select>
                </div>

                <div>
                  <label className="font-bold text-slate-700 block mb-1">Social Category</label>
                  <select 
                    value={sandbox.social_category}
                    onChange={(e) => setSandbox({ ...sandbox, social_category: e.target.value })}
                    className="w-full p-2 rounded-xl border border-slate-200 font-semibold bg-slate-50 focus:ring-2 focus:ring-emerald-500 focus:bg-white outline-none"
                  >
                    <option value="OBC">OBC (Special)</option>
                    <option value="SC">SC (Special)</option>
                    <option value="ST">ST (Special)</option>
                    <option value="Minority">Minority (Special)</option>
                    <option value="Divyangjan">Divyangjan (Special)</option>
                    <option value="Ex-Servicemen">Ex-Servicemen (Special)</option>
                    <option value="General">General</option>
                  </select>
                </div>
              </div>

              {/* Area & Business Type */}
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="font-bold text-slate-700 block mb-1">Location Area</label>
                  <select 
                    value={sandbox.area}
                    onChange={(e) => setSandbox({ ...sandbox, area: e.target.value })}
                    className="w-full p-2 rounded-xl border border-slate-200 font-semibold bg-slate-50 focus:ring-2 focus:ring-emerald-500 focus:bg-white outline-none"
                  >
                    <option value="rural">Rural (35% / 25%)</option>
                    <option value="urban">Urban (25% / 15%)</option>
                  </select>
                </div>

                <div>
                  <label className="font-bold text-slate-700 block mb-1">Business Activity</label>
                  <select 
                    value={sandbox.business_type}
                    onChange={(e) => setSandbox({ ...sandbox, business_type: e.target.value })}
                    className="w-full p-2 rounded-xl border border-slate-200 font-semibold bg-slate-50 focus:ring-2 focus:ring-emerald-500 focus:bg-white outline-none"
                  >
                    <option value="manufacturing">Manufacturing (₹50L Cap)</option>
                    <option value="service">Service (₹20L Cap)</option>
                    <option value="trading">Trading (₹20L Cap)</option>
                  </select>
                </div>
              </div>

              {/* Project Cost Slider */}
              <div className="space-y-1.5">
                <div className="flex justify-between font-bold text-slate-700">
                  <span>Total Project Cost:</span>
                  <span className="font-mono text-emerald-700 text-sm">₹{(sandbox.project_cost).toLocaleString('en-IN')}</span>
                </div>
                <input 
                  type="range" 
                  min="50000" 
                  max="6000000" 
                  step="50000"
                  value={sandbox.project_cost}
                  onChange={(e) => setSandbox({ ...sandbox, project_cost: Number(e.target.value) })}
                  className="w-full accent-emerald-600 h-2 bg-slate-200 rounded-lg cursor-pointer"
                />
                <div className="flex justify-between text-[10px] text-slate-400 font-mono">
                  <span>₹50k</span>
                  <span>₹20L (Service Cap)</span>
                  <span>₹50L (Mfg Cap)</span>
                  <span>₹60L</span>
                </div>
              </div>

              {/* Age & Education */}
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="font-bold text-slate-700 block mb-1">Applicant Age ({sandbox.age} yrs)</label>
                  <input 
                    type="number" 
                    min="14" 
                    max="80"
                    value={sandbox.age}
                    onChange={(e) => setSandbox({ ...sandbox, age: Number(e.target.value) })}
                    className="w-full p-2 rounded-xl border border-slate-200 font-semibold bg-slate-50 focus:ring-2 focus:ring-emerald-500 focus:bg-white outline-none"
                  />
                </div>

                <div>
                  <label className="font-bold text-slate-700 block mb-1">Education</label>
                  <select 
                    value={sandbox.education}
                    onChange={(e) => setSandbox({ ...sandbox, education: e.target.value })}
                    className="w-full p-2 rounded-xl border border-slate-200 font-semibold bg-slate-50 focus:ring-2 focus:ring-emerald-500 focus:bg-white outline-none"
                  >
                    <option value="10th">10th Standard Pass</option>
                    <option value="8th">8th Standard Pass</option>
                    <option value="12th">12th / Diploma</option>
                    <option value="graduate">Graduate / Degree</option>
                    <option value="below_8th">Below 8th Standard</option>
                  </select>
                </div>
              </div>

              {/* Own Contribution Equity Slider */}
              <div className="space-y-1">
                <div className="flex justify-between font-bold text-slate-700">
                  <span>Promoter Equity Contribution:</span>
                  <span className="font-mono text-indigo-700 font-bold">{sandbox.own_contribution_pct}%</span>
                </div>
                <input 
                  type="range" 
                  min="0" 
                  max="30" 
                  step="1"
                  value={sandbox.own_contribution_pct}
                  onChange={(e) => setSandbox({ ...sandbox, own_contribution_pct: Number(e.target.value) })}
                  className="w-full accent-indigo-600 h-2 bg-slate-200 rounded-lg cursor-pointer"
                />
              </div>

              {/* Checkboxes for Training & Industry */}
              <div className="space-y-2 pt-1">
                <label className="flex items-center gap-2 font-medium text-slate-700 cursor-pointer">
                  <input 
                    type="checkbox" 
                    checked={sandbox.has_skill_training || sandbox.edp_undertaking}
                    onChange={(e) => setSandbox({ ...sandbox, has_skill_training: e.target.checked, edp_undertaking: e.target.checked })}
                    className="w-4 h-4 rounded text-emerald-600 accent-emerald-600 cursor-pointer"
                  />
                  <span>10-Day EDP Training / Undertaking Completed</span>
                </label>

                <div>
                  <label className="font-bold text-slate-700 block mb-1">Industry Type / Sector</label>
                  <select 
                    value={sandbox.industry_sector}
                    onChange={(e) => setSandbox({ ...sandbox, industry_sector: e.target.value })}
                    className="w-full p-2 rounded-xl border border-slate-200 font-semibold bg-slate-50 focus:ring-2 focus:ring-emerald-500 focus:bg-white outline-none"
                  >
                    <option value="food_processing">Food Processing &amp; Agro</option>
                    <option value="textiles_apparel">Textiles &amp; Garments</option>
                    <option value="engineering_it">Engineering &amp; IT Services</option>
                    <option value="handicrafts_artisan">Handicrafts &amp; Village Crafts</option>
                    <option value="tobacco_bidi_liquor">❌ Tobacco / Liquor (Negative List)</option>
                    <option value="meat_slaughter">❌ Meat Slaughter (Negative List)</option>
                  </select>
                </div>
              </div>

            </div>

            {/* Real-Time Mathematical Output Breakdown */}
            <div className="p-4 rounded-2xl bg-gradient-to-br from-slate-900 to-indigo-950 text-white space-y-4 border border-slate-800">
              
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-slate-300 uppercase tracking-wider">Rule Engine Match</span>
                <span className={`px-2.5 py-1 rounded-full text-xs font-black ${
                  matchPercentage >= 80 ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' : 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
                }`}>
                  {matchPercentage}% Score ({earnedScore}/{totalPossibleWeight})
                </span>
              </div>

              {/* Progress bar */}
              <div className="w-full bg-slate-800 rounded-full h-2.5 overflow-hidden">
                <div 
                  className={`h-full transition-all duration-500 rounded-full ${
                    matchPercentage >= 80 ? 'bg-emerald-400' : matchPercentage >= 50 ? 'bg-amber-400' : 'bg-rose-500'
                  }`}
                  style={{ width: `${matchPercentage}%` }}
                />
              </div>

              {/* Statutory PMEGP Breakdown Table */}
              <div className="space-y-2 text-xs border-t border-slate-800/80 pt-3">
                <div className="flex justify-between py-1 border-b border-slate-800/50">
                  <span className="text-slate-400">Category Track:</span>
                  <span className="font-bold text-amber-300">{isSpecialDemographic ? 'Special Beneficiary' : 'General Beneficiary'}</span>
                </div>
                <div className="flex justify-between py-1 border-b border-slate-800/50">
                  <span className="text-slate-400">Govt Margin Subsidy ({subsidyPct}%):</span>
                  <span className="font-black text-emerald-400 font-mono">₹{calculatedMaxSubsidyAmount.toLocaleString('en-IN')}</span>
                </div>
                <div className="flex justify-between py-1 border-b border-slate-800/50">
                  <span className="text-slate-400">Mandatory Promoter Equity ({ownContributionReq}%):</span>
                  <span className="font-bold text-slate-200 font-mono">₹{calculatedPromoterEquity.toLocaleString('en-IN')}</span>
                </div>
                <div className="flex justify-between py-1">
                  <span className="text-slate-400">Bank Loan Required:</span>
                  <span className="font-bold text-indigo-300 font-mono">₹{calculatedBankLoanAmount.toLocaleString('en-IN')}</span>
                </div>
              </div>

              {/* Individual Rule Verdicts List */}
              <div className="space-y-1.5 pt-2 border-t border-slate-800/80">
                <span className="text-[10px] uppercase font-bold text-slate-400 block tracking-wider">Rule Evaluation Matrix</span>
                <div className="max-h-40 overflow-y-auto space-y-1.5 pr-1 text-[11px]">
                  {evaluationResults.map(({ rule, result }) => (
                    <div 
                      key={rule.id}
                      className={`flex items-center justify-between p-1.5 rounded-lg ${
                        !rule.is_active ? 'bg-slate-800/30 text-slate-500' : result.passed ? 'bg-emerald-950/40 text-emerald-300' : 'bg-rose-950/40 text-rose-300'
                      }`}
                    >
                      <div className="flex items-center gap-1.5 truncate">
                        {!rule.is_active ? (
                          <span className="w-3.5 h-3.5 text-slate-500 font-mono text-[10px]">○</span>
                        ) : result.passed ? (
                          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                        ) : (
                          <XCircle className="w-3.5 h-3.5 text-rose-400 shrink-0" />
                        )}
                        <span className="truncate font-medium">{rule.name}</span>
                      </div>
                      <span className="font-mono font-bold shrink-0 text-[10px]">
                        {!rule.is_active ? 'DISABLED' : result.passed ? `+${rule.weight}%` : '0%'}
                      </span>
                    </div>
                  ))}
                </div>
              </div>

            </div>

          </div>

        </div>

      </div>

      {/* Modal for ADD / EDIT Rule */}
      {modalOpen && activeRule && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto">
          <div className="bg-white rounded-3xl max-w-2xl w-full p-6 sm:p-8 shadow-2xl border border-slate-100 space-y-6 my-8 animate-in fade-in zoom-in-95">
            
            <div className="flex items-center justify-between pb-4 border-b border-slate-100">
              <div className="flex items-center gap-2.5">
                <div className="p-2 rounded-xl bg-emerald-100 text-emerald-800">
                  <Sliders className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="font-black text-slate-900 text-lg">
                    {modalMode === 'add' ? 'Add New Rule to Engine' : `Edit Rule: ${activeRule.code}`}
                  </h3>
                  <p className="text-xs text-slate-500">Target Scheme: {activeRule.scheme}</p>
                </div>
              </div>
              <button 
                onClick={() => setModalOpen(false)}
                className="text-slate-400 hover:text-slate-700 font-bold p-1 rounded-lg hover:bg-slate-100 cursor-pointer"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleSaveRule} className="space-y-4 text-xs">
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="font-bold text-slate-700 block mb-1">Scheme Identifier</label>
                  <select 
                    value={activeRule.scheme}
                    onChange={(e) => setActiveRule({ ...activeRule, scheme: e.target.value, code: `${e.target.value}_RULE_${String(rules.length + 1).padStart(2, '0')}` })}
                    className="w-full p-2.5 rounded-xl border border-slate-200 font-semibold bg-slate-50 focus:bg-white outline-none focus:ring-2 focus:ring-emerald-500"
                  >
                    {INITIAL_SCHEMES.map(s => (
                      <option key={s.code} value={s.code}>{s.code} - {s.name.split(' ')[0]}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="font-bold text-slate-700 block mb-1">Rule Identifier Code</label>
                  <input 
                    type="text" 
                    value={activeRule.code}
                    onChange={(e) => setActiveRule({ ...activeRule, code: e.target.value })}
                    className="w-full p-2.5 rounded-xl border border-slate-200 font-mono font-bold bg-slate-50 focus:bg-white outline-none focus:ring-2 focus:ring-emerald-500"
                    required
                  />
                </div>
              </div>

              <div>
                <label className="font-bold text-slate-700 block mb-1">Rule Name</label>
                <input 
                  type="text" 
                  placeholder="e.g. Special Category Subsidy Gate"
                  value={activeRule.name}
                  onChange={(e) => setActiveRule({ ...activeRule, name: e.target.value })}
                  className="w-full p-2.5 rounded-xl border border-slate-200 font-semibold bg-slate-50 focus:bg-white outline-none focus:ring-2 focus:ring-emerald-500"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="font-bold text-slate-700 block mb-1">Target Demographic / Segment</label>
                  <input 
                    type="text" 
                    placeholder="e.g. SC / ST / OBC / Women"
                    value={activeRule.target || ''}
                    onChange={(e) => setActiveRule({ ...activeRule, target: e.target.value })}
                    className="w-full p-2.5 rounded-xl border border-slate-200 font-medium bg-slate-50 focus:bg-white outline-none focus:ring-2 focus:ring-emerald-500"
                  />
                </div>

                <div>
                  <label className="font-bold text-slate-700 block mb-1">Rule Category / Type</label>
                  <select 
                    value={activeRule.rule_type}
                    onChange={(e) => setActiveRule({ ...activeRule, rule_type: e.target.value })}
                    className="w-full p-2.5 rounded-xl border border-slate-200 font-semibold bg-slate-50 focus:bg-white outline-none focus:ring-2 focus:ring-emerald-500"
                  >
                    <option value="Target Subsidy Gate">Target Subsidy Gate</option>
                    <option value="Statutory Quantum Cap">Statutory Quantum Cap</option>
                    <option value="Legal Eligibility Filter">Legal Eligibility Filter</option>
                    <option value="Academic Prerequisite">Academic Prerequisite</option>
                    <option value="Margin Money Compliance">Margin Money Compliance</option>
                    <option value="Weighted Metric">Weighted Metric</option>
                    <option value="Negative List Filter">Negative List Filter</option>
                  </select>
                </div>
              </div>

              {/* Mathematical Predicate */}
              <div>
                <label className="font-bold text-slate-700 block mb-1">
                  Mathematical Condition Expression (Python / JS syntax)
                </label>
                <textarea 
                  rows="3"
                  placeholder="e.g. user.social_category in ['SC','ST','OBC'] or user.gender == 'female'"
                  value={activeRule.condition}
                  onChange={(e) => setActiveRule({ ...activeRule, condition: e.target.value })}
                  className="w-full p-2.5 rounded-xl border border-slate-200 font-mono text-xs text-emerald-800 bg-slate-50 focus:bg-white outline-none focus:ring-2 focus:ring-emerald-500"
                  required
                />
              </div>

              {/* Weight & Status */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="font-bold text-slate-700 block mb-1">Rule Weight ({activeRule.weight}%)</label>
                  <input 
                    type="range" 
                    min="5" 
                    max="50" 
                    step="5"
                    value={activeRule.weight}
                    onChange={(e) => setActiveRule({ ...activeRule, weight: Number(e.target.value) })}
                    className="w-full accent-emerald-600 h-2 bg-slate-200 rounded-lg cursor-pointer"
                  />
                </div>

                <div>
                  <label className="font-bold text-slate-700 block mb-1">Initial State</label>
                  <div className="flex items-center gap-4 pt-1">
                    <label className="flex items-center gap-2 font-semibold text-slate-700 cursor-pointer">
                      <input 
                        type="radio" 
                        name="is_active" 
                        checked={activeRule.is_active === true}
                        onChange={() => setActiveRule({ ...activeRule, is_active: true })}
                        className="text-emerald-600 accent-emerald-600"
                      />
                      <span>Active</span>
                    </label>
                    <label className="flex items-center gap-2 font-semibold text-slate-700 cursor-pointer">
                      <input 
                        type="radio" 
                        name="is_active" 
                        checked={activeRule.is_active === false}
                        onChange={() => setActiveRule({ ...activeRule, is_active: false })}
                        className="text-slate-500 accent-slate-500"
                      />
                      <span>Disabled</span>
                    </label>
                  </div>
                </div>
              </div>

              {/* Statutory Note */}
              <div>
                <label className="font-bold text-slate-700 block mb-1">Gazette / Ministry Statutory Policy Citation</label>
                <input 
                  type="text" 
                  placeholder="e.g. As per KVIC Guidelines 2022 revised norms Section 4(a)"
                  value={activeRule.statutory_note || ''}
                  onChange={(e) => setActiveRule({ ...activeRule, statutory_note: e.target.value })}
                  className="w-full p-2.5 rounded-xl border border-slate-200 font-medium bg-slate-50 focus:bg-white outline-none focus:ring-2 focus:ring-emerald-500"
                />
              </div>

              {/* Failure Template */}
              <div>
                <label className="font-bold text-slate-700 block mb-1">Failure Diagnostic Message</label>
                <input 
                  type="text" 
                  placeholder="e.g. Applicant does not qualify for Special Category Subsidy bracket."
                  value={activeRule.failure_msg || ''}
                  onChange={(e) => setActiveRule({ ...activeRule, failure_msg: e.target.value })}
                  className="w-full p-2.5 rounded-xl border border-slate-200 font-medium bg-slate-50 focus:bg-white outline-none focus:ring-2 focus:ring-emerald-500"
                />
              </div>

              {/* Buttons */}
              <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setModalOpen(false)}
                  className="px-4 py-2 rounded-xl text-slate-600 font-bold hover:bg-slate-100 transition-colors cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-black shadow-lg shadow-emerald-600/20 transition-all cursor-pointer"
                >
                  {modalMode === 'add' ? 'Create Rule' : 'Save Changes'}
                </button>
              </div>

            </form>
          </div>
        </div>
      )}

    </div>
  );
}
