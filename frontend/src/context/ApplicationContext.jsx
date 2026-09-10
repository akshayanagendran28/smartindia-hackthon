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

const getDefaultApplicationForUser = (user, profile) => {
  const pType = profile?.purpose_type || 'EDUCATION';
  const isEdu = pType === 'EDUCATION';
  
  return {
    purpose_type: pType,
    purposeType: pType,
    loanAmount: profile?.required_loan || profile?.required_loan_amount || (isEdu ? 450000 : 1200000),
    required_loan: profile?.required_loan || profile?.required_loan_amount || (isEdu ? 450000 : 1200000),
    required_loan_amount: profile?.required_loan || profile?.required_loan_amount || (isEdu ? 450000 : 1200000),
    
    full_name: profile?.full_name || user?.full_name || '',
    age: profile?.age || (isEdu ? 20 : 28),
    gender: profile?.gender || 'female',
    category: profile?.category || profile?.social_category || 'General',
    social_category: profile?.social_category || profile?.category || 'General',
    religion: profile?.religion || 'hindu',
    is_differently_abled: profile?.is_differently_abled || false,

    country: 'India',
    state: profile?.state || profile?.location_state || user?.state || 'Tamil Nadu',
    district: profile?.district || profile?.location_district || user?.district || 'Chennai',
    location_state: profile?.state || profile?.location_state || user?.state || 'Tamil Nadu',
    location_district: profile?.district || profile?.location_district || user?.district || 'Chennai',
    area_type: profile?.area_type || 'rural',
    pincode: profile?.pincode || '600001',

    // Education Track Specifics
    current_education_level: profile?.current_education_level || '12th Pass',
    course_type: profile?.course_type || 'Technical / Engineering (B.Tech / B.E / M.Tech)',
    institution_type: profile?.institution_type || 'NAAC / AICTE / UGC Approved Govt/Aided College',
    admission_status: profile?.admission_status || 'Confirmed Admission (Offer / Allotment Letter in Hand)',
    annual_course_fee: profile?.annual_course_fee || 120000,
    course_duration_years: profile?.course_duration_years || 4,

    // General Financials
    annual_income: profile?.annual_income || profile?.annual_family_income || (isEdu ? 220000 : 180000),
    annual_family_income: profile?.annual_family_income || profile?.annual_income || (isEdu ? 220000 : 180000),

    // Business Track Specifics
    purpose: isEdu ? 'Higher Education' : (profile?.purpose || 'Start a Business'),
    business_type: isEdu ? 'education' : (profile?.business_type || 'manufacturing'),
    business_stage: profile?.business_stage || 'New Greenfield Enterprise',
    industry_sector: profile?.industry_sector || (isEdu ? 'education' : 'food_processing'),
    project_cost: profile?.project_cost || (isEdu ? 480000 : 1500000),
    own_contribution: profile?.own_contribution || (isEdu ? 30000 : 300000),
    existing_turnover: profile?.existing_turnover || 0,
    has_skill_training: profile?.has_skill_training || false,
    has_udyam_registration: profile?.has_udyam_registration || false,
    has_gst: profile?.has_gst || false,
    gstin: profile?.gstin || '',
    is_artisan: profile?.is_artisan || false,
    is_street_vendor: profile?.is_street_vendor || false,

    // Workflow Gates & Selections
    isProfileConfirmed: profile?.profile_completed || false,
    selectedScheme: null,
    verifiedDocKeys: [], // Initial state has 0 verified documents for new users
    allDocumentsVerified: false,
  };
};

export const ApplicationProvider = ({ children }) => {
  const { user, profile } = useAuth();
  const userKey = user?.id ? `user_${user.id}` : (user?.email ? `email_${user.email}` : 'guest');
  
  const [application, setApplication] = useState(() => {
    try {
      const saved = localStorage.getItem(`scheme_sathi_app_${userKey}`);
      if (saved) {
        return JSON.parse(saved);
      }
    } catch (e) {}
    return getDefaultApplicationForUser(user, profile);
  });

  const [workflowStage, setWorkflowStage] = useState(() => {
    return localStorage.getItem(`scheme_sathi_stage_${userKey}`) || WORKFLOW_STAGES.PROFILE_DRAFT;
  });

  // Re-synchronize application state whenever active user changes
  useEffect(() => {
    try {
      const saved = localStorage.getItem(`scheme_sathi_app_${userKey}`);
      if (saved) {
        setApplication(JSON.parse(saved));
      } else {
        const freshApp = getDefaultApplicationForUser(user, profile);
        setApplication(freshApp);
      }
    } catch (e) {
      setApplication(getDefaultApplicationForUser(user, profile));
    }
  }, [user?.id, user?.email]);

  // Keep localStorage updated with active user application state
  useEffect(() => {
    try {
      if (userKey) {
        localStorage.setItem(`scheme_sathi_app_${userKey}`, JSON.stringify(application));
        localStorage.setItem(`scheme_sathi_stage_${userKey}`, workflowStage);
      }
    } catch (e) {}
  }, [application, workflowStage, userKey]);

  // Sync profile when auth profile loads
  useEffect(() => {
    if (profile && profile.profile_completed) {
      setApplication(prev => ({
        ...prev,
        full_name: profile.full_name || prev.full_name,
        category: profile.category || profile.social_category || prev.category,
        social_category: profile.social_category || profile.category || prev.social_category,
        state: profile.state || profile.location_state || prev.state,
        district: profile.district || profile.location_district || prev.district,
        location_state: profile.state || profile.location_state || prev.location_state,
        location_district: profile.district || profile.location_district || prev.location_district,
        purpose_type: profile.purpose_type || prev.purpose_type,
        purposeType: profile.purpose_type || prev.purposeType,
        loanAmount: profile.required_loan || profile.required_loan_amount || prev.loanAmount,
        required_loan: profile.required_loan || profile.required_loan_amount || prev.required_loan,
        required_loan_amount: profile.required_loan || profile.required_loan_amount || prev.required_loan_amount,
        project_cost: profile.project_cost || prev.project_cost,
        annual_income: profile.annual_income || profile.annual_family_income || prev.annual_income,
        annual_family_income: profile.annual_family_income || profile.annual_income || prev.annual_family_income,
        isProfileConfirmed: true
      }));
    }
  }, [profile]);

  const updatePurposeType = (newPurpose) => {
    const pType = (newPurpose || 'EDUCATION').toUpperCase();
    setApplication(prev => {
      let specificDefaults = {};
      if (pType === 'EDUCATION') {
        specificDefaults = {
          age: 20,
          current_education_level: '12th Pass',
          course_type: 'Technical / Engineering (B.Tech / B.E / M.Tech)',
          institution_type: 'NAAC / AICTE / UGC Approved Govt/Aided College',
          admission_status: 'Confirmed Admission (Offer / Allotment Letter in Hand)',
          annual_course_fee: 120000,
          course_duration_years: 4,
          loanAmount: 450000,
          required_loan: 450000,
          required_loan_amount: 450000,
          project_cost: 480000,
          annual_family_income: 250000,
          annual_income: 250000,
          purpose: 'Higher Education',
          business_type: 'education',
          is_artisan: false,
          is_street_vendor: false,
          has_udyam_registration: false,
        };
      } else if (pType === 'SELF_EMPLOYMENT') {
        specificDefaults = {
          age: 32,
          loanAmount: 50000,
          required_loan: 50000,
          required_loan_amount: 50000,
          project_cost: 50000,
          annual_family_income: 95000,
          annual_income: 95000,
          purpose: 'Self Employment',
          business_type: 'street_vendor',
          is_artisan: false,
          is_street_vendor: true,
          has_udyam_registration: false,
        };
      } else {
        specificDefaults = {
          age: 29,
          loanAmount: 1200000,
          required_loan: 1200000,
          required_loan_amount: 1200000,
          project_cost: 1500000,
          annual_family_income: 180000,
          annual_income: 180000,
          purpose: 'Start a Business',
          business_type: 'manufacturing',
          business_stage: 'New Greenfield Enterprise',
          is_artisan: false,
          is_street_vendor: false,
          has_udyam_registration: true,
        };
      }

      return {
        ...prev,
        purpose_type: pType,
        purposeType: pType,
        ...specificDefaults,
        selectedScheme: null,
        verifiedDocKeys: [],
        allDocumentsVerified: false,
      };
    });
  };

  const updateLoanAmount = (amount) => {
    const num = Number(amount) || 0;
    setApplication(prev => ({
      ...prev,
      loanAmount: num,
      required_loan: num,
      required_loan_amount: num,
    }));
  };

  const updateApplication = (fields) => {
    setApplication(prev => ({
      ...prev,
      ...fields,
      purpose_type: fields.purpose_type || fields.purposeType || prev.purpose_type,
      purposeType: fields.purpose_type || fields.purposeType || prev.purposeType,
      loanAmount: fields.loanAmount || fields.required_loan || fields.required_loan_amount || prev.loanAmount,
      category: fields.social_category || fields.category || prev.category,
      social_category: fields.social_category || fields.category || prev.social_category,
    }));
  };

  const confirmAndSaveProfile = async (profileData) => {
    try {
      const dataToSave = { ...application, ...profileData };
      const res = await profileAPI.updateProfile({
        full_name: dataToSave.full_name,
        age: Number(dataToSave.age) || 28,
        gender: dataToSave.gender,
        category: dataToSave.social_category || dataToSave.category || 'General',
        social_category: dataToSave.social_category || dataToSave.category || 'General',
        annual_family_income: Number(dataToSave.annual_family_income) || 250000,
        annual_income: Number(dataToSave.annual_income) || 250000,
        purpose_type: dataToSave.purpose_type || 'EDUCATION',
        purpose: dataToSave.purpose || (dataToSave.purpose_type === 'EDUCATION' ? 'Higher Education' : 'Start a Business'),
        required_loan_amount: Number(dataToSave.loanAmount || dataToSave.required_loan) || 450000,
        required_loan: Number(dataToSave.loanAmount || dataToSave.required_loan) || 450000,
        project_cost: Number(dataToSave.project_cost) || 500000,
        state: dataToSave.state || 'Tamil Nadu',
        district: dataToSave.district || 'Chennai',
        location_state: dataToSave.state || 'Tamil Nadu',
        location_district: dataToSave.district || 'Chennai',
        area_type: dataToSave.area_type || 'rural',
        business_type: dataToSave.business_type || (dataToSave.purpose_type === 'EDUCATION' ? 'education' : 'manufacturing'),
        is_artisan: dataToSave.is_artisan || false,
        is_street_vendor: dataToSave.is_street_vendor || false,
        has_udyam_registration: dataToSave.has_udyam_registration || false,
      });

      setApplication(prev => ({
        ...prev,
        ...dataToSave,
        isProfileConfirmed: true
      }));
      setWorkflowStage(WORKFLOW_STAGES.PROFILE_CONFIRMED);
      return res.data;
    } catch (err) {
      setApplication(prev => ({
        ...prev,
        ...profileData,
        isProfileConfirmed: true
      }));
      setWorkflowStage(WORKFLOW_STAGES.PROFILE_CONFIRMED);
      return profileData;
    }
  };

  const recordDocumentVerified = (docType) => {
    setApplication(prev => {
      const existing = prev.verifiedDocKeys || [];
      const updated = existing.includes(docType) ? existing : [...existing, docType];
      return {
        ...prev,
        verifiedDocKeys: updated
      };
    });
  };

  const setAllDocumentsVerified = (status) => {
    setApplication(prev => ({
      ...prev,
      allDocumentsVerified: Boolean(status)
    }));
    if (status) {
      setWorkflowStage(WORKFLOW_STAGES.DOCUMENTS_VERIFIED);
    }
  };

  const selectScheme = (scheme) => {
    setApplication(prev => ({
      ...prev,
      selectedScheme: scheme
    }));
    setWorkflowStage(WORKFLOW_STAGES.SCHEME_SELECTED);
  };

  return (
    <ApplicationContext.Provider value={{
      application,
      purposeType: application.purpose_type || application.purposeType || 'EDUCATION',
      loanAmount: application.loanAmount || 450000,
      workflowStage,
      isProfileConfirmed: application.isProfileConfirmed,
      selectedScheme: application.selectedScheme,
      verifiedDocKeys: application.verifiedDocKeys || [],
      allDocumentsVerified: application.allDocumentsVerified || false,
      updatePurposeType,
      updateLoanAmount,
      updateApplication,
      confirmAndSaveProfile,
      recordDocumentVerified,
      setAllDocumentsVerified,
      selectScheme,
      setWorkflowStage,
    }}>
      {children}
    </ApplicationContext.Provider>
  );
};

export const useApplication = () => useContext(ApplicationContext);
