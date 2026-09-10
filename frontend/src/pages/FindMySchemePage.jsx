import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Sparkles, ArrowRight, ArrowLeft, CheckCircle2, User, MapPin, 
  Briefcase, DollarSign, FileCheck, ShieldCheck, GraduationCap, Hammer, Store, Info 
} from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { useApplication } from '../context/ApplicationContext';
import { locationsAPI } from '../services/api';
import StepProgressIndicator from '../components/StepProgressIndicator';

export default function FindMySchemePage() {
  const { t, currentLanguage } = useLanguage();
  const { 
    application, 
    updateApplication, 
    updateLoanAmount, 
    submitRequirements 
  } = useApplication();
  const navigate = useNavigate();

  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Dynamic States & Districts
  const [statesList, setStatesList] = useState([]);
  const [districtsList, setDistrictsList] = useState([]);
  const [loadingDistricts, setLoadingDistricts] = useState(false);

  // Form State initialized directly from single Application source of truth
  const [formData, setFormData] = useState({
    // Step 1: Category & Demographics
    full_name: application.full_name || 'Beneficiary Candidate',
    age: application.age || 28,
    gender: application.gender || 'female',
    social_category: (application.category && application.category !== 'General' && application.category !== 'OBC') ? application.category : 'SC',
    religion: application.religion || 'hindu',
    is_differently_abled: application.is_differently_abled || false,

    // Step 2: Location (Dynamic Country -> State -> District)
    country: 'India',
    state: application.state || 'Tamil Nadu',
    district: application.district || 'Tiruvallur',
    area_type: application.area_type || 'rural',
    pincode: application.pincode || '602001',

    // Step 3: Purpose & Conditional Sector
    purpose: application.purpose || 'Start a Business',
    business_type: application.business_type || 'manufacturing',
    business_stage: application.business_stage || 'new',
    industry_sector: application.industry_sector || 'food_processing',
    education_qualification: application.education_qualification || 'graduate',
    course: application.course || '',
    institution: application.institution || '',
    education_cost: application.education_cost || 0,
    artisan_trade: 'Carpenter / Wood Craft',
    is_artisan: application.is_artisan || false,
    is_street_vendor: application.is_street_vendor || false,
    has_skill_training: application.has_skill_training !== undefined ? application.has_skill_training : true,
    has_udyam_registration: application.has_udyam_registration !== undefined ? application.has_udyam_registration : true,
    gstin: application.gstin || '',

    // Step 4: Single Loan Amount & Project Financials
    required_loan: application.loanAmount || 1200000,
    project_cost: application.project_cost || 1500000,
    own_contribution: application.own_contribution || 300000,
    annual_income: application.annual_income || 180000,
    annual_family_income: application.annual_family_income || 180000,
  });

  // Load States list on mount
  useEffect(() => {
    locationsAPI.getStates()
      .then(res => {
        if (res.data && res.data.length > 0) {
          setStatesList(res.data);
        }
      })
      .catch(err => console.warn('Could not load states', err));
  }, []);

  // Fetch dynamic districts when state changes
  useEffect(() => {
    if (formData.state) {
      setLoadingDistricts(true);
      locationsAPI.getDistricts(formData.state)
        .then(res => {
          const list = res.data?.districts || [];
          setDistrictsList(list);
          if (list.length > 0 && (!formData.district || !list.includes(formData.district))) {
            setFormData(prev => ({ ...prev, district: list[0] }));
            updateApplication({ state: formData.state, district: list[0] });
          }
        })
        .catch(err => {
          console.warn('Could not load districts for state', formData.state, err);
          setDistrictsList([]);
        })
        .finally(() => setLoadingDistricts(false));
    }
  }, [formData.state]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    const newVal = type === 'checkbox' ? checked : (type === 'number' ? Number(value) : value);
    
    setFormData(prev => {
      const updated = { ...prev, [name]: newVal };
      
      // Keep loan amounts synchronized
      if (name === 'required_loan') {
        updateLoanAmount(Number(value));
      }
      return updated;
    });
  };

  const handleNext = () => {
    if (step < 4) setStep(step + 1);
  };

  const handleBack = () => {
    if (step > 1) setStep(step - 1);
  };

  /**
   * Final submission of requirements:
   * Redirects strictly to DOCUMENT VERIFICATION before eligibility is evaluated!
   */
  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // 1. Synchronize requirements with application context
      updateApplication({
        ...formData,
        loanAmount: formData.required_loan,
        category: formData.social_category,
      });
      submitRequirements(formData);

      // 2. Strict Workflow Order: Redirect to Document Verification first!
      navigate('/documents');
    } catch (err) {
      console.error(err);
      setError('Failed to save requirements. Please retry.');
    } finally {
      setLoading(false);
    }
  };

  const steps = [
    { num: 1, title: '1. Demographics', icon: <User className="w-4 h-4" /> },
    { num: 2, title: '2. Dynamic Location', icon: <MapPin className="w-4 h-4" /> },
    { num: 3, title: '3. Purpose & Sector', icon: <Briefcase className="w-4 h-4" /> },
    { num: 4, title: '4. Loan & Financials', icon: <DollarSign className="w-4 h-4" /> },
  ];

  return (
    <div className="max-w-3xl mx-auto py-8 px-4 sm:px-6">
      <StepProgressIndicator currentStep={2} />

      {/* Wizard Header */}
      <div className="text-center mb-8">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold mb-2">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Intelligent Scheme Requirement Intake</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-black text-slate-900">Find My Scheme</h1>
        <p className="text-xs sm:text-sm text-slate-500 mt-1">
          Answer tailored dynamic questions to identify eligible Central and State initiatives.
        </p>
      </div>

      {/* Step Progress Indicator */}
      <div className="mb-8">
        <div className="flex justify-between items-center relative">
          <div className="absolute top-1/2 left-0 right-0 h-1 bg-slate-200 -translate-y-1/2 z-0"></div>
          <div 
            className="absolute top-1/2 left-0 h-1 bg-emerald-500 -translate-y-1/2 z-0 transition-all duration-300"
            style={{ width: `${((step - 1) / 3) * 100}%` }}
          ></div>

          {steps.map((s) => (
            <div key={s.num} className="relative z-10 flex flex-col items-center">
              <div 
                className={`w-9 h-9 rounded-full flex items-center justify-center font-bold text-xs transition-all ${
                  step === s.num
                    ? 'bg-emerald-600 text-white ring-4 ring-emerald-100 scale-110 shadow-md'
                    : step > s.num
                    ? 'bg-emerald-500 text-white'
                    : 'bg-white border-2 border-slate-300 text-slate-500'
                }`}
              >
                {step > s.num ? <CheckCircle2 className="w-4 h-4" /> : s.icon}
              </div>
              <span className={`text-[11px] font-semibold mt-1.5 hidden sm:block ${step >= s.num ? 'text-slate-900' : 'text-slate-400'}`}>
                {s.title}
              </span>
            </div>
          ))}
        </div>
      </div>

      {error && (
        <div className="mb-6 p-3.5 bg-red-50 border border-red-200 text-red-700 rounded-xl text-xs">
          {error}
        </div>
      )}

      {/* Step Content Container */}
      <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm">
        {/* Step 1: Category & Demographics */}
        {step === 1 && (
          <div className="space-y-5 animate-fadeIn">
            <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
              <User className="w-5 h-5 text-emerald-600" />
              <span>Step 1: Target Category & Demographics</span>
            </h2>
            <p className="text-xs text-slate-500">
              Only supported marginalized beneficiary categories are presented for affirmative subsidy calculation.
            </p>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Target Marginalized Category
                </label>
                <select
                  name="social_category"
                  value={formData.social_category}
                  onChange={handleChange}
                  className="w-full px-3 py-2.5 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:outline-none bg-slate-50 font-medium"
                >
                  <option value="SC">Scheduled Caste (SC)</option>
                  <option value="ST">Scheduled Tribe (ST)</option>
                  <option value="Minority">Minority (Muslim/Christian/Sikh/Buddhist/Jain/Parsi)</option>
                  <option value="Woman">Women / Special Category</option>
                  <option value="Divyangjan">Specially Abled / Divyangjan</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Gender</label>
                <select
                  name="gender"
                  value={formData.gender}
                  onChange={handleChange}
                  className="w-full px-3 py-2.5 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:outline-none bg-slate-50"
                >
                  <option value="female">Female / Woman</option>
                  <option value="male">Male</option>
                  <option value="transgender">Transgender</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Age (Years)</label>
                <input
                  type="number"
                  name="age"
                  min="16"
                  max="80"
                  value={formData.age}
                  onChange={handleChange}
                  className="w-full px-3 py-2.5 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Educational Qualification</label>
                <select
                  name="education_qualification"
                  value={formData.education_qualification}
                  onChange={handleChange}
                  className="w-full px-3 py-2.5 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:outline-none bg-slate-50"
                >
                  <option value="graduate">Graduate / Post-Graduate</option>
                  <option value="12th">12th Standard Passed</option>
                  <option value="8th">8th Standard Passed</option>
                  <option value="below_8th">Below 8th Standard / Literate</option>
                </select>
              </div>
            </div>

            <div className="pt-2">
              <label className="inline-flex items-center gap-2 text-xs font-semibold text-slate-700 cursor-pointer">
                <input
                  type="checkbox"
                  name="is_differently_abled"
                  checked={formData.is_differently_abled}
                  onChange={handleChange}
                  className="w-4 h-4 text-emerald-600 rounded"
                />
                <span>Specially Abled Person (PwD / Divyangjan &gt; 40%)</span>
              </label>
            </div>
          </div>
        )}

        {/* Step 2: Dynamic Location (Country -> State -> District) */}
        {step === 2 && (
          <div className="space-y-5 animate-fadeIn">
            <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
              <MapPin className="w-5 h-5 text-emerald-600" />
              <span>Step 2: Dynamic Dependent Location</span>
            </h2>
            <p className="text-xs text-slate-500">
              Districts update dynamically from the verified government registry based on your selected state.
            </p>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Country</label>
                <input
                  type="text"
                  disabled
                  value="India"
                  className="w-full px-3 py-2.5 text-sm border border-slate-200 bg-slate-100 text-slate-600 rounded-xl"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">State / Union Territory</label>
                <select
                  name="state"
                  value={formData.state}
                  onChange={handleChange}
                  className="w-full px-3 py-2.5 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:outline-none bg-white font-medium"
                >
                  {statesList.length > 0 ? (
                    statesList.map(st => (
                      <option key={st} value={st}>{st}</option>
                    ))
                  ) : (
                    <>
                      <option value="Tamil Nadu">Tamil Nadu</option>
                      <option value="Maharashtra">Maharashtra</option>
                      <option value="Karnataka">Karnataka</option>
                      <option value="Kerala">Kerala</option>
                      <option value="Delhi">Delhi</option>
                      <option value="Gujarat">Gujarat</option>
                    </>
                  )}
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  District {loadingDistricts && <span className="text-[10px] text-emerald-600">(Loading...)</span>}
                </label>
                <select
                  name="district"
                  value={formData.district}
                  onChange={handleChange}
                  disabled={loadingDistricts || districtsList.length === 0}
                  className="w-full px-3 py-2.5 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:outline-none bg-white disabled:opacity-50 font-medium"
                >
                  {districtsList.length > 0 ? (
                    districtsList.map(dist => (
                      <option key={dist} value={dist}>{dist}</option>
                    ))
                  ) : (
                    <option value="">No districts available</option>
                  )}
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Area Classification</label>
                <select
                  name="area_type"
                  value={formData.area_type}
                  onChange={handleChange}
                  className="w-full px-3 py-2.5 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:outline-none bg-white"
                >
                  <option value="rural">Rural (Eligible for 35% PMEGP Subsidy Quota)</option>
                  <option value="urban">Urban (Eligible for 25% PMEGP Subsidy Quota)</option>
                </select>
              </div>
            </div>
          </div>
        )}

        {/* Step 3: Purpose & Conditional Sector Questions */}
        {step === 3 && (
          <div className="space-y-5 animate-fadeIn">
            <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
              <Briefcase className="w-5 h-5 text-emerald-600" />
              <span>Step 3: Purpose & Tailored Sector Questions</span>
            </h2>
            <p className="text-xs text-slate-500">
              Questions adapt dynamically based on whether you are launching a business, studying, or practicing a traditional craft.
            </p>

            {/* Purpose Selector */}
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">What is your primary purpose?</label>
              <select
                name="purpose"
                value={formData.purpose}
                onChange={handleChange}
                className="w-full px-3 py-2.5 text-sm font-bold border border-emerald-500 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:outline-none bg-emerald-50/40 text-emerald-950"
              >
                <option value="Start a Business">Start a New Business / Enterprise (Greenfield)</option>
                <option value="Expand Existing Business">Expand / Modernize Existing Business</option>
                <option value="Higher Education">Higher Education Loan / Student Venture (ASIIM)</option>
                <option value="Traditional Craft">Traditional Artisan / PM Vishwakarma</option>
                <option value="Street Vending">Street Vending / PM SVANidhi Microcredit</option>
              </select>
            </div>

            {/* CONDITIONAL SUB-FORM: Business & Micro-Enterprise */}
            {(formData.purpose === 'Start a Business' || formData.purpose === 'Expand Existing Business') && (
              <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200 space-y-4">
                <div className="flex items-center gap-2 text-xs font-bold text-slate-800">
                  <Briefcase className="w-4 h-4 text-emerald-600" />
                  <span>Business Enterprise Details</span>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">Business Nature</label>
                    <select
                      name="business_type"
                      value={formData.business_type}
                      onChange={handleChange}
                      className="w-full px-3 py-2.5 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:outline-none bg-white"
                    >
                      <option value="manufacturing">Manufacturing (Limit up to ₹50 Lakh)</option>
                      <option value="service">Service Unit (Limit up to ₹20 Lakh)</option>
                      <option value="trading">Trading / Retail</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">Business Stage</label>
                    <select
                      name="business_stage"
                      value={formData.business_stage}
                      onChange={handleChange}
                      className="w-full px-3 py-2.5 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:outline-none bg-white"
                    >
                      <option value="new">New Enterprise (Greenfield)</option>
                      <option value="expansion">Existing Unit (Modernization/Expansion)</option>
                    </select>
                  </div>
                </div>

                <div className="space-y-2 pt-1">
                  <label className="inline-flex items-center gap-2 text-xs font-semibold text-slate-700 cursor-pointer">
                    <input
                      type="checkbox"
                      name="has_skill_training"
                      checked={formData.has_skill_training}
                      onChange={handleChange}
                      className="w-4 h-4 text-emerald-600 rounded"
                    />
                    <span>Has 2-Week EDP / Skill Training Certificate</span>
                  </label>

                  <label className="inline-flex items-center gap-2 text-xs font-semibold text-slate-700 cursor-pointer block">
                    <input
                      type="checkbox"
                      name="has_udyam_registration"
                      checked={formData.has_udyam_registration}
                      onChange={handleChange}
                      className="w-4 h-4 text-emerald-600 rounded"
                    />
                    <span>Has Udyam MSME Registration Certificate</span>
                  </label>
                </div>
              </div>
            )}

            {/* CONDITIONAL SUB-FORM: Higher Education / Student Venture */}
            {formData.purpose === 'Higher Education' && (
              <div className="p-4 bg-blue-50 rounded-2xl border border-blue-200 space-y-4">
                <div className="flex items-center gap-2 text-xs font-bold text-blue-900">
                  <GraduationCap className="w-4 h-4 text-blue-600" />
                  <span>Education & Student Innovation Parameters</span>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">Target Course / Degree</label>
                    <input
                      type="text"
                      name="course"
                      placeholder="e.g. B.Tech / M.Tech / MBA / Startup Innovation"
                      value={formData.course}
                      onChange={handleChange}
                      className="w-full px-3 py-2.5 text-sm border border-slate-300 rounded-xl bg-white"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">Institution Name</label>
                    <input
                      type="text"
                      name="institution"
                      placeholder="e.g. National Institute of Technology"
                      value={formData.institution}
                      onChange={handleChange}
                      className="w-full px-3 py-2.5 text-sm border border-slate-300 rounded-xl bg-white"
                    />
                  </div>
                </div>
              </div>
            )}

            {/* CONDITIONAL SUB-FORM: Traditional Craft / Artisan */}
            {formData.purpose === 'Traditional Craft' && (
              <div className="p-4 bg-amber-50 rounded-2xl border border-amber-200 space-y-4">
                <div className="flex items-center gap-2 text-xs font-bold text-amber-900">
                  <Hammer className="w-4 h-4 text-amber-600" />
                  <span>PM Vishwakarma Traditional Craft Details</span>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">Recognized Traditional Trade</label>
                  <select
                    name="artisan_trade"
                    value={formData.artisan_trade}
                    onChange={handleChange}
                    className="w-full px-3 py-2.5 text-sm border border-slate-300 rounded-xl bg-white font-medium"
                  >
                    <option value="Carpenter / Wood Craft">Carpenter (Suthar)</option>
                    <option value="Blacksmith / Iron Work">Blacksmith (Lohar)</option>
                    <option value="Potter / Terracotta">Potter (Kumhaar)</option>
                    <option value="Sculptor / Stone Carver">Sculptor (Moortikar)</option>
                    <option value="Cobbler / Leather Artisan">Cobbler (Charmakar)</option>
                    <option value="Mason / Building Construction">Mason (Raajmistri)</option>
                    <option value="Tailor / Garments">Tailor (Darzi)</option>
                    <option value="Basket / Mat / Broom Maker">Basket / Mat Maker</option>
                  </select>
                  <p className="text-[10px] text-amber-800 mt-1">Eligible for ₹15,000 modern toolkit voucher + ₹3 Lakh credit at 5% interest.</p>
                </div>
              </div>
            )}

            {/* CONDITIONAL SUB-FORM: Street Vending */}
            {formData.purpose === 'Street Vending' && (
              <div className="p-4 bg-teal-50 rounded-2xl border border-teal-200 space-y-3">
                <div className="flex items-center gap-2 text-xs font-bold text-teal-900">
                  <Store className="w-4 h-4 text-teal-600" />
                  <span>PM SVANidhi Street Vending Micro-Credit</span>
                </div>
                <p className="text-xs text-teal-800">
                  Offers collateral-free working capital loan of ₹10k, ₹20k, and ₹50k with 7% interest subsidy and cashback for UPI transactions.
                </p>
              </div>
            )}
          </div>
        )}

        {/* Step 4: Single Loan Amount & Project Financials */}
        {step === 4 && (
          <div className="space-y-5 animate-fadeIn">
            <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
              <DollarSign className="w-5 h-5 text-emerald-600" />
              <span>Step 4: Single Loan Amount & Financial Parameters</span>
            </h2>
            <p className="text-xs text-slate-500">
              The loan amount below is the single source of truth across all matching, EMI calculation, and partner assignment stages.
            </p>

            <div className="space-y-4 pt-2">
              <div className="p-4 bg-emerald-50 rounded-2xl border-2 border-emerald-300 space-y-2">
                <div className="flex justify-between items-center text-xs font-bold text-slate-800">
                  <span>Required Loan Amount</span>
                  <span className="text-emerald-800 font-black text-lg font-mono">
                    ₹{Number(formData.required_loan).toLocaleString('en-IN')}
                  </span>
                </div>
                <input
                  type="number"
                  name="required_loan"
                  min="10000"
                  max="50000000"
                  step="25000"
                  value={formData.required_loan}
                  onChange={handleChange}
                  className="w-full px-3 py-2 text-sm border border-emerald-500 rounded-xl focus:ring-2 focus:ring-emerald-500 bg-white font-mono font-bold text-emerald-900"
                />
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">Total Project Cost (₹)</label>
                  <input
                    type="number"
                    name="project_cost"
                    value={formData.project_cost}
                    onChange={handleChange}
                    className="w-full px-3 py-2.5 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:outline-none font-mono"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">Promoter Margin / Own Contribution (₹)</label>
                  <input
                    type="number"
                    name="own_contribution"
                    value={formData.own_contribution}
                    onChange={handleChange}
                    className="w-full px-3 py-2.5 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:outline-none font-mono"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Annual Family Income (₹)</label>
                <input
                  type="number"
                  name="annual_family_income"
                  value={formData.annual_family_income}
                  onChange={handleChange}
                  className="w-full px-3 py-2.5 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:outline-none font-mono"
                />
              </div>

              <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl flex items-center gap-2 text-xs text-slate-600">
                <Info className="w-4 h-4 text-slate-400 shrink-0" />
                <span>
                  Next Step: You will be redirected to <strong>Document Verification</strong> to verify required certificates before calculating statutory scheme eligibility.
                </span>
              </div>
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex justify-between items-center mt-8 pt-6 border-t border-slate-100">
          {step > 1 ? (
            <button
              type="button"
              onClick={handleBack}
              className="inline-flex items-center gap-1.5 px-5 py-2.5 border border-slate-300 text-slate-700 rounded-xl text-xs font-bold hover:bg-slate-50 transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Previous</span>
            </button>
          ) : (
            <div />
          )}

          {step < 4 ? (
            <button
              type="button"
              onClick={handleNext}
              className="inline-flex items-center gap-1.5 px-6 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-xs font-bold shadow-md shadow-emerald-600/20 transition-all"
            >
              <span>Next Step</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          ) : (
            <button
              type="button"
              onClick={handleSubmit}
              disabled={loading}
              className="inline-flex items-center gap-2 px-8 py-3 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white rounded-xl text-sm font-black shadow-lg shadow-emerald-600/25 transition-all disabled:opacity-50"
            >
              <FileCheck className="w-4 h-4" />
              <span>{loading ? 'Saving Requirements...' : 'Confirm & Proceed to Document Verification'}</span>
              <ArrowRight className="w-4 h-4 ml-1" />
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
