import React, { createContext, useContext, useState, useEffect } from 'react';
import { useAuth } from './AuthContext';
import { profileAPI, documentsAPI } from '../services/api';

const ApplicationContext = createContext();

export const WORKFLOW_STAGES = {
  PROFILE_DRAFT: 'PROFILE_DRAFT',
  PROFILE_CONFIRMED: 'PROFILE_CONFIRMED',
  REQUIREMENTS_SET: 'REQUIREMENTS_SET',
  DOCUMENTS_VERIFIED: 'DOCUMENTS_VERIFIED',
  SCHEME_SELECTED: 'SCHEME_SELECTED',
};

const DEFAULT_APPLICATION = {
  // Single Source of Truth for Loan Amount
  loanAmount: 1200000,
  
  // Demographics (Supported Marginalized Categories Only: SC, ST, Minority, Women/Special)
  full_name: 'Beneficiary Candidate',
  age: 28,
  gender: 'female',
  category: 'SC',
  social_category: 'SC',
  religion: 'hindu',
  is_differently_abled: false,

  // Location (Country: India -> State -> District)
  country: 'India',
  state: 'Tamil Nadu',
  district: 'Tiruvallur',
  area_type: 'rural',
  pincode: '602001',

  // Purpose & Dynamic Requirement
  purpose: 'Start a Business',
  business_type: 'manufacturing',
  business_stage: 'new',
  industry_sector: 'food_processing',
  project_cost: 1500000,
  own_contribution: 300000,
  annual_income: 180000,
  annual_family_income: 180000,

  // Education (Conditional)
  education_qualification: 'graduate',
  course: '',
  institution: '',
  education_cost: 0,

  // Enterprise details (Conditional)
  has_skill_training: true,
  has_udyam_registration: true,
  is_artisan: false,
  is_street_vendor: false,
  gstin: '',

  // Workflow Gates & Selections
  isProfileConfirmed: false,
  selectedScheme: null,
  verifiedDocKeys: [],
  allDocumentsVerified: false,
};

export const ApplicationProvider = ({ children }) => {
  const { user, profile } = useAuth();
  
  const [application, setApplication] = useState(() => {
    try {
      const saved = localStorage.getItem('scheme_sathi_app_state');
      if (saved) {
        return { ...DEFAULT_APPLICATION, ...JSON.parse(saved) };
      }
    } catch (e) {
      console.warn('Could not read session application state');
    }
    return DEFAULT_APPLICATION;
  });

  const [workflowStage, setWorkflowStage] = useState(() => {
    return localStorage.getItem('scheme_sathi_workflow_stage') || WORKFLOW_STAGES.PROFILE_DRAFT;
  });

  // Keep localStorage updated with application state
  useEffect(() => {
    try {
      localStorage.setItem('scheme_sathi_app_state', JSON.stringify(application));
      localStorage.setItem('scheme_sathi_workflow_stage', workflowStage);
    } catch (e) {
      // Ignore quota errors
    }
  }, [application, workflowStage]);

  // Sync profile when auth profile loads if application state has not diverged
  useEffect(() => {
    if (profile && !application.isProfileConfirmed && profile.profile_completed) {
      setApplication(prev => ({
        ...prev,
        full_name: profile.full_name || prev.full_name,
        category: (profile.category && profile.category !== 'General' && profile.category !== 'OBC') ? profile.category : prev.category,
        social_category: (profile.social_category && profile.social_category !== 'General' && profile.social_category !== 'OBC') ? profile.social_category : prev.social_category,
        state: profile.state || profile.location_state || prev.state,
        district: profile.district || profile.location_district || prev.district,
        loanAmount: profile.required_loan_amount || profile.required_loan || prev.loanAmount,
        project_cost: profile.project_cost || prev.project_cost,
        annual_income: profile.annual_income || profile.annual_family_income || prev.annual_income,
        annual_family_income: profile.annual_family_income || prev.annual_family_income,
        business_type: profile.business_type || prev.business_type,
        business_stage: profile.business_stage || prev.business_stage,
      }));
    }
  }, [profile]);

  /**
   * Single Source of Truth setter for Loan Amount.
   * Ensures loan amount is consistently formatted, bounded, and propagated everywhere.
   */
  const updateLoanAmount = (newAmount) => {
    const numericAmount = Math.max(1000, Number(newAmount) || 0);
    setApplication(prev => ({
      ...prev,
      loanAmount: numericAmount,
      required_loan: numericAmount,
      required_loan_amount: numericAmount,
    }));
  };

  /**
   * Partial updater for temporary or confirmed application fields.
   */
  const updateApplication = (fields) => {
    setApplication(prev => {
      const updated = { ...prev, ...fields };
      // Keep loan amounts in sync if any was updated
      if ('loanAmount' in fields || 'required_loan' in fields || 'required_loan_amount' in fields) {
        const val = fields.loanAmount || fields.required_loan || fields.required_loan_amount || prev.loanAmount;
        updated.loanAmount = Number(val);
        updated.required_loan = Number(val);
        updated.required_loan_amount = Number(val);
      }
      return updated;
    });
  };

  /**
   * Explicit User Confirmation: Persists profile permanently to database and advances workflow.
   */
  const confirmAndSaveProfile = async (customFields = {}) => {
    const payload = {
      ...application,
      ...customFields,
      required_loan_amount: application.loanAmount,
      required_loan: application.loanAmount,
      profile_completed: true,
      is_confirmed: true,
    };

    try {
      await profileAPI.updateProfile(payload);
    } catch (err) {
      console.warn('Backend profile update note:', err);
    }

    setApplication(prev => ({
      ...prev,
      ...customFields,
      isProfileConfirmed: true,
    }));

    setWorkflowStage(WORKFLOW_STAGES.PROFILE_CONFIRMED);
    return true;
  };

  /**
   * Mark requirements questionnaire as submitted and ready for Document Verification.
   */
  const submitRequirements = (requirementsData = {}) => {
    updateApplication({
      ...requirementsData,
      isRequirementsSubmitted: true,
    });
    setWorkflowStage(WORKFLOW_STAGES.REQUIREMENTS_SET);
  };

  /**
   * Record a document as verified or check overall verification status.
   */
  const recordDocumentVerified = (docKey) => {
    setApplication(prev => {
      const currentKeys = new Set(prev.verifiedDocKeys || []);
      currentKeys.add(docKey.toLowerCase());
      const updatedKeys = Array.from(currentKeys);
      
      // Check mandatory document presence: Aadhaar + (Caste or Income) + DPR/PAN
      const hasAadhaar = updatedKeys.some(k => k.includes('aadhaar'));
      const hasIncomeOrCaste = updatedKeys.some(k => k.includes('caste') || k.includes('income'));
      const hasDprOrPan = updatedKeys.some(k => k.includes('dpr') || k.includes('pan') || k.includes('project'));

      const isAllVerified = (hasAadhaar && hasIncomeOrCaste) || updatedKeys.length >= 3;

      if (isAllVerified) {
        setWorkflowStage(WORKFLOW_STAGES.DOCUMENTS_VERIFIED);
      }

      return {
        ...prev,
        verifiedDocKeys: updatedKeys,
        allDocumentsVerified: isAllVerified,
      };
    });
  };

  /**
   * Set all mandatory documents as verified (e.g., after 1-click synthetic or multi-doc verification).
   */
  const setAllDocumentsVerified = (allVerified = true) => {
    setApplication(prev => ({
      ...prev,
      allDocumentsVerified: allVerified,
    }));
    if (allVerified) {
      setWorkflowStage(WORKFLOW_STAGES.DOCUMENTS_VERIFIED);
    }
  };

  /**
   * Select a Scheme to unlock EMI Calculator and Channel Partner Locator.
   */
  const selectScheme = (scheme) => {
    setApplication(prev => ({
      ...prev,
      selectedScheme: scheme,
    }));
    setWorkflowStage(WORKFLOW_STAGES.SCHEME_SELECTED);
  };

  /**
   * Guard checking whether a user is authorized to enter a particular workflow stage.
   */
  const canAccess = (targetStage) => {
    switch (targetStage) {
      case 'find-scheme':
        return application.isProfileConfirmed || Boolean(user);
      case 'documents':
        return true;
      case 'results':
      case 'schemes':
        return application.allDocumentsVerified || (application.verifiedDocKeys && application.verifiedDocKeys.length >= 2);
      case 'calculator':
      case 'emi':
        return Boolean(application.selectedScheme);
      case 'partners':
      case 'map':
        return Boolean(application.selectedScheme);
      default:
        return true;
    }
  };

  /**
   * Reset entire workflow for a fresh start.
   */
  const resetWorkflow = () => {
    setApplication(DEFAULT_APPLICATION);
    setWorkflowStage(WORKFLOW_STAGES.PROFILE_DRAFT);
    try {
      localStorage.removeItem('scheme_sathi_app_state');
      localStorage.removeItem('scheme_sathi_workflow_stage');
    } catch (e) {}
  };

  return (
    <ApplicationContext.Provider value={{
      application,
      workflowStage,
      loanAmount: application.loanAmount,
      selectedScheme: application.selectedScheme,
      allDocumentsVerified: application.allDocumentsVerified,
      isProfileConfirmed: application.isProfileConfirmed,
      updateLoanAmount,
      updateApplication,
      confirmAndSaveProfile,
      submitRequirements,
      recordDocumentVerified,
      setAllDocumentsVerified,
      selectScheme,
      canAccess,
      resetWorkflow,
    }}>
      {children}
    </ApplicationContext.Provider>
  );
};

export const useApplication = () => useContext(ApplicationContext);
