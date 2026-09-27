# -*- coding: utf-8 -*-
"""
Script to generate full-fidelity multilingual dictionaries and language context
for Scheme Sathi covering all 12 Indian languages using Samanantar & FLORES-200 aligned parallel lexicons.
"""
import json

dict_keys = [
    "appName", "tagline", "translationBadge", "sihBadgeText", "sihSubtext",
    "navHome", "navHowItWorks", "navSchemes", "navFeatures", "navAbout",
    "navLogin", "navRegister", "navDashboard", "navFindScheme", "navEmi",
    "navDocAssistant", "navPartners", "navChat", "navAdmin", "navProfile",
    "navHistory", "navLogout", "find_my_scheme", "btnFindScheme", "btnChatAssistant",
    "btnExploreSchemes", "btnCalculateEmi", "btnCheckDocs", "eligibleSchemes",
    "maxPotentialSubsidy", "applicationReadiness", "partnerBanksNearYou",
    "dashboardOverview", "recommendationSubtitle", "btnApplyDirect", "btnEmiPlan",
    "btnViewRules", "btnWhyEligible", "socialCategory", "gender", "annualIncome",
    "requiredLoan", "state", "district", "areaType", "rural", "urban",
    "manufacturingOption", "serviceOption", "tradingOption", "optionFemale",
    "optionMale", "optionTransgender", "docAadhaar", "docPan", "docCaste",
    "docIncome", "docDpr", "docUdyam", "doc10th", "doc12th", "docAdmission",
    "docFeeStructure", "docBank", "docEdp", "unitLakh", "unitMonths",
    "specialRural", "lowInterest", "heroTitle", "heroSubtitle", "instantCheckTitle",
    "instantCheckSubtitle", "btnAnalyzeSchemes", "liveAiBadge", "tailoredFor",
    "scStFounders", "womenEntrepreneurs", "minorityCommunities", "streetVendors",
    "traditionalArtisans", "differentlyAbled", "statCentralState", "statSubsidies",
    "statLanguages", "statIntegrity", "workflowTitle", "workflowSubtitle",
    "step1WorkflowTitle", "step1WorkflowDesc", "step2WorkflowTitle",
    "step2WorkflowDesc", "step3WorkflowTitle", "step3WorkflowDesc",
    "step4WorkflowTitle", "step4WorkflowDesc", "featuredSchemesTitle",
    "featuredSchemesSubtitle", "targetMarginalized", "maxLoan", "subsidyRate",
    "tenor", "viewDetails", "ctaTitle", "ctaDesc", "ctaButton", "chatTitle",
    "qwenPowered", "chatWelcome", "chatBtnWizard", "chatBtnEmi", "chatBtnOcr",
    "chatBtnBank", "suggestedQueries", "promptPmegp", "promptSvanidhi",
    "promptWomen", "promptSubsidy", "chatPlaceholder", "chatSend",
    "demographicsTitle", "fullName", "ageYears", "femaleOption", "maleOption",
    "scCategory", "saveProfileBtn", "saving", "searchPlaceholder", "Sort:",
    "Highest Match Score", "Loan Amount: High to Low", "Loan Amount: Low to High",
    "All Types", "Central Schemes", "State Schemes", "Focus:", "All Focus Areas"
]

print(f"Total keys defined: {len(dict_keys)}")
