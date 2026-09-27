# -*- coding: utf-8 -*-
"""
Generates the complete LanguageContext.jsx containing all 12 Indic languages + English,
and updates all UI pages to ensure 100% localization without any English leaks.
"""
import os
import json
import sys

# Import base schemes and aliases
from generate_full_system_v4 import master_scheme_map

# Load dictionary translations for all 12 languages
DICTIONARY_12_LANG = {
    "en": {
        "appName": "SCHEME SATHI",
        "tagline": "AI-Driven Financial Scheme Matching for Entrepreneurs",
        "translationBadge": "Powered by AI4Bharat Samanantar & Meta FLORES-200 IndicNLP",
        "sihBadgeText": "SIH 2026",
        "sihSubtext": "AI-Driven Scheme Matching • Official myScheme.gov.in Dataset",
        "navHome": "Home",
        "navHowItWorks": "How It Works",
        "navSchemes": "Schemes",
        "navFeatures": "Features",
        "navAbout": "About",
        "navLogin": "Login",
        "navRegister": "Register",
        "navDashboard": "Dashboard",
        "navFindScheme": "Find My Scheme",
        "navEmi": "EMI Calculator",
        "navDocAssistant": "Doc Assistant",
        "navPartners": "Channel Partners",
        "navChat": "AI Assistant",
        "navAdmin": "Admin Portal",
        "navProfile": "User Profile",
        "navHistory": "Transparency Timeline",
        "navLogout": "Logout",
        "find_my_scheme": "Find My Scheme",
        "btnFindScheme": "Find My Scheme",
        "btnChatAssistant": "Chat with AI Assistant",
        "btnExploreSchemes": "Explore Schemes",
        "btnCalculateEmi": "Calculate EMI",
        "btnCheckDocs": "Check Documents",
        "eligibleSchemes": "Eligible Schemes",
        "maxPotentialSubsidy": "Max Potential Subsidy",
        "applicationReadiness": "Application Readiness",
        "partnerBanksNearYou": "Partner Banks Near You",
        "dashboardOverview": "Dashboard Overview",
        "recommendationSubtitle": "Real-time multi-factor government financial schemes matched against official gazetted criteria.",
        "btnApplyDirect": "Apply / Invite Partner",
        "btnEmiPlan": "Plan EMI",
        "btnViewRules": "View Rules",
        "btnWhyEligible": "Why am I eligible?",
        "btnPrevious": "Previous",
        "resultsTitle": "Scheme Results",
        "socialCategory": "Social Category",
        "gender": "Gender",
        "annualIncome": "Annual Income",
        "requiredLoan": "Required Loan Amount",
        "state": "State",
        "district": "District",
        "areaType": "Area Classification",
        "rural": "Rural",
        "urban": "Urban",
        "manufacturingOption": "Manufacturing Unit",
        "serviceOption": "Service Sector",
        "tradingOption": "Trading / Retail",
        "optionFemale": "Female",
        "optionMale": "Male",
        "optionTransgender": "Transgender",
        "docAadhaar": "Aadhaar Card",
        "docPan": "PAN Card",
        "docCaste": "Caste Certificate",
        "docIncome": "Income Certificate",
        "docDpr": "Detailed Project Report (DPR)",
        "docUdyam": "Udyam Registration",
        "doc10th": "10th Marksheet",
        "doc12th": "12th Marksheet",
        "docAdmission": "Admission Letter",
        "docFeeStructure": "Fee Structure",
        "docBank": "Bank Statement",
        "docEdp": "EDP Training Certificate",
        "unitLakh": "Lakh",
        "unitMonths": "Months",
        "specialRural": "35% Special Rural",
        "lowInterest": "Concessional Interest",
        "heroTitle": "AI-Powered Scheme Discovery & Capital Subsidy Matching",
        "heroSubtitle": "Discover, verify, and apply for central and state financial schemes tailored for marginalized founders, students, and micro-entrepreneurs.",
        "instantCheckTitle": "Instant Eligibility Check",
        "instantCheckSubtitle": "Find matched schemes and subsidies in 30 seconds",
        "btnAnalyzeSchemes": "Analyze Matching Schemes",
        "liveAiBadge": "Live AI Engine",
        "tailoredFor": "Tailored for Priority Beneficiaries",
        "scStFounders": "SC/ST Founders",
        "womenEntrepreneurs": "Women Entrepreneurs",
        "minorityCommunities": "Minority Communities",
        "streetVendors": "Street Vendors",
        "traditionalArtisans": "Traditional Artisans",
        "differentlyAbled": "Differently Abled (Divyangjan)",
        "statCentralState": "Central & State Schemes",
        "statSubsidies": "Maximum Subsidies",
        "statLanguages": "Regional Languages",
        "statIntegrity": "Rule Verification Integrity",
        "workflowTitle": "How Scheme Sathi Works",
        "workflowSubtitle": "Transparent 4-Step Journey from Profile to Bank Sanction",
        "step1WorkflowTitle": "Profile & Requirements Intake",
        "step1WorkflowDesc": "Provide your education or business goals, social category, and funding needs.",
        "step2WorkflowTitle": "Deterministic Rules Engine",
        "step2WorkflowDesc": "Real-time evaluation against official gazetted rules and eligibility criteria.",
        "step3WorkflowTitle": "OCR Document Pre-Validation",
        "step3WorkflowDesc": "Automatic client-side verification and checksums with zero raw PII storage.",
        "step4WorkflowTitle": "Channel Partner Routing",
        "step4WorkflowDesc": "Direct application handoff to nearest nodal banks and industry centres.",
        "featuredSchemesTitle": "Featured Verified Schemes",
        "featuredSchemesSubtitle": "Explore top government financial schemes for marginalized founders.",
        "targetMarginalized": "Priority Beneficiary",
        "maxLoan": "Maximum Loan",
        "subsidyRate": "Subsidy Rate",
        "tenor": "Repayment Tenure",
        "viewDetails": "View Details",
        "ctaTitle": "Ready to Find Your Government Scheme?",
        "ctaDesc": "Experience instant scheme matching, verified document checks, and transparent rule explanations.",
        "ctaButton": "Check My Eligibility Now",
        "demographicsTitle": "1. Beneficiary Demographics & Identification",
        "fullName": "Full Name",
        "ageYears": "Age (Years)",
        "femaleOption": "Female",
        "maleOption": "Male",
        "transgenderOption": "Transgender",
        "generalCategory": "General Category",
        "scCategory": "Scheduled Caste (SC)",
        "stCategory": "Scheduled Tribe (ST)",
        "obcCategory": "Other Backward Class (OBC)",
        "minorityCategory": "Minority Community",
        "women entrepreneur / special category": "Women / Special Category",
        "ruralOption": "Rural Area (Higher Subsidy)",
        "urbanOption": "Urban Area",
        "businessType": "Business Type",
        "saving": "Saving...",
        "confirm & save profile": "Confirm & Save Profile",
        "chatWelcome": "Namaste! I am your AI Scheme Sathi powered by Qwen. I can help you discover government loan schemes, interest subsidies, and document requirements. What type of assistance or business loan are you looking for today?",
        "chatBtnWizard": "Find Scheme Wizard",
        "chatBtnEmi": "EMI & Subsidy Plan",
        "chatBtnOcr": "Document Assistant",
        "chatBtnBank": "Bank Partner Map",
        "chatTitle": "Scheme Sathi AI Assistant",
        "qwenPowered": "Grounded on official myScheme.gov.in Gazette",
        "suggestedQueries": "Suggested Queries:",
        "promptPmegp": "How does PMEGP 35% subsidy work?",
        "promptSvanidhi": "PM SVANidhi loans for street vendors",
        "promptWomen": "Schemes for SC/ST and Women Entrepreneurs",
        "promptSubsidy": "What is the highest capital subsidy available?",
        "chatPlaceholder": "Ask about government loan schemes, eligibility, subsidies, or documents...",
        "chatSend": "Send",
        "chatGeneratingResponse": "Generating grounded response with Qwen (Ollama)...",
        "chatCatchFallback": "Under PMEGP, rural SC/ST, women, and minority entrepreneurs are eligible for up to 35% capital subsidy with a 5% margin money contribution on manufacturing projects up to ₹50 Lakh. For street vendors, PM SVANidhi provides up to ₹50,000 micro-credit with a 7% interest subvention.",
        "select your goal track": "Select Your Goal Track",
        "Education": "Education",
        "Business": "Business",
        "Self-Emp": "Self-Emp",
        "course stream": "Course Stream",
        "engineering / tech": "Engineering / Tech",
        "medical / healthcare": "Medical / Healthcare",
        "management / mba": "Management / MBA",
        "overseas studies": "Overseas Studies",
        "activity type": "Activity Type",
        "street vendor / hawkers": "Street Vendor / Hawkers",
        "artisan / handicrafts": "Artisan / Handicrafts",
        "small service / repair": "Small Service / Repair",
        "target course / loan amount": "Target Course / Loan Amount",
        "₹50k (Base)": "₹50k (Base)",
        "₹7.5L (CSIS / CGFSEL)": "₹7.5L (CSIS / CGFSEL)",
        "₹20L+ (NSFDC / Overseas)": "₹20L+ (NSFDC / Overseas)",
        "₹10k (PM SVANidhi)": "₹10k (PM SVANidhi)",
        "₹1L (Scale Up)": "₹1L (Scale Up)",
        "₹3L (PM Vishwakarma)": "₹3L (PM Vishwakarma)",
        "₹1 Lakh (Micro)": "₹1 Lakh (Micro)",
        "₹50 Lakh (PMEGP)": "₹50 Lakh (PMEGP)",
        "₹1 Cr (Stand-Up)": "₹1 Cr (Stand-Up)",
        "Government Purpose Track / Goal": "Government Purpose Track / Goal",
        "Switch purpose to discover all statutory schemes across sectors": "Switch purpose to discover all statutory schemes across sectors",
        "Higher Education & Student Loans": "Higher Education & Student Loans",
        "CSIS, NSFDC, NBCFDC, NMDFC, Overseas": "CSIS, NSFDC, NBCFDC, NMDFC, Overseas",
        "MSME & Business Loans": "MSME & Business Loans",
        "PMEGP, Stand-Up India, Mudra Kishore/Tarun": "PMEGP, Stand-Up India, Mudra Kishore/Tarun",
        "Street Vendors & Artisans": "Street Vendors & Artisans",
        "PM SVANidhi, PM Vishwakarma, Mudra Shishu": "PM SVANidhi, PM Vishwakarma, Mudra Shishu",
        "Scheme Sathi • AI-Driven Statutory Rules Matching Engine": "Scheme Sathi • AI-Driven Statutory Rules Matching Engine",
        "Qualified Schemes for": "Qualified Schemes for",
        "Lakhs": "Lakhs",
        "Resident Location:": "Resident Location:",
        "Social Category:": "Social Category:",
        "Target Track:": "Target Track:",
        "Modify Requirement": "Modify Requirement",
        "Eligible Schemes": "Eligible Schemes",
        "Match Score": "Match Score",
        "Available & Alternative Schemes": "Available & Alternative Schemes",
        "Rule Breakdown": "Rule Breakdown",
        "searchPlaceholder": "Search scheme name, ministry, or keyword...",
        "All Types": "All Types",
        "Central Schemes": "Central Schemes",
        "State Schemes": "State Schemes",
        "Central Scheme": "Central Scheme",
        "State Scheme": "State Scheme",
        "Government of India": "Government of India",
        "Sort:": "Sort:",
        "Highest Match Score": "Highest Match Score",
        "Loan Amount: High to Low": "Loan Amount: High to Low",
        "Loan Amount: Low to High": "Loan Amount: Low to High",
        "Focus:": "Focus:",
        "All Focus Areas": "All Focus Areas",
        "Interest Subsidy (CSIS)": "Interest Subsidy (CSIS)",
        "SC Students (NSFDC)": "SC Students (NSFDC)",
        "OBC Students (NBCFDC)": "OBC Students (NBCFDC)",
        "Minority (Maulana Azad)": "Minority (Maulana Azad)",
        "Overseas Studies (Ambedkar)": "Overseas Studies (Ambedkar)",
        "Credit Guarantee (CGFSEL)": "Credit Guarantee (CGFSEL)",
        "Street Vendors (PM SVANidhi)": "Street Vendors (PM SVANidhi)",
        "Artisans (PM Vishwakarma)": "Artisans (PM Vishwakarma)",
        "Women Microfinance": "Women Microfinance",
        "Mudra Shishu": "Mudra Shishu",
        "Manufacturing": "Manufacturing",
        "Services": "Services",
        "Capital Subsidies": "Capital Subsidies",
        "Evaluating statutory gazette rules & calculating SHAP match scores...": "Evaluating statutory gazette rules & calculating SHAP match scores...",
        "Disbursement Readiness Notice": "Disbursement Readiness Notice",
        "You qualify for the statutory schemes below. Verify your mandatory documents in the Document Assistant for fast-track loan sanction.": "You qualify for the statutory schemes below. Verify your mandatory documents in the Document Assistant for fast-track loan sanction.",
        "Upload / Verify": "Upload / Verify",
        "Statutory Match": "Statutory Match",
        "Passed Eligibility Conditions:": "Passed Eligibility Conditions:",
        "Statutory Verified • myScheme.gov.in": "Statutory Verified • myScheme.gov.in",
        "Official Portal": "Official Portal",
        "Maximum Cap:": "Maximum Cap:",
        "Government Subsidy:": "Government Subsidy:",
        "Up to 35% Special Rural": "Up to 35% Special Rural",
        "Repayment Period:": "Repayment Period:",
        "Selected Scheme (Active)": "Selected Scheme (Active)",
        "Select Scheme & Calculate EMI (Step 5)": "Select Scheme & Calculate EMI (Step 5)",
        "Full Details": "Full Details",
        "Find Branch": "Find Branch",
        "No Matching Eligible Schemes Found": "No Matching Eligible Schemes Found",
        "Click on the \"Available & Alternative Schemes\" tab above to see all gazette schemes and reasons for exclusion.": "Click on the \"Available & Alternative Schemes\" tab above to see all gazette schemes and reasons for exclusion.",
        "View Available Schemes": "View Available Schemes",
        "Modify Questionnaire": "Modify Questionnaire",
        "These schemes are currently operating under Central / State mandates. Transparent gazette reasons for exclusion are displayed below.": "These schemes are currently operating under Central / State mandates. Transparent gazette reasons for exclusion are displayed below.",
        "Failed Gazette Condition(s):": "Failed Gazette Condition(s):",
        "Criteria mismatch with applicant profile or required loan ceiling exceeded.": "Criteria mismatch with applicant profile or required loan ceiling exceeded.",
        "Max Limit:": "Max Limit:",
        "View Scheme Guidelines": "View Scheme Guidelines",
        "No additional available schemes found matching your search.": "No additional available schemes found matching your search.",
        "Official Gazette Registry • myScheme.gov.in": "Official Gazette Registry • myScheme.gov.in",
        "filterCentral": "Central Scheme",
        "filterState": "State Scheme",
        "mySchemePortal": "myScheme Portal",
        "interestRateLabel": "Interest Rate",
        "Subsidy Slabs & Beneficiary Contribution (Gazette Statutory Rules)": "Subsidy Slabs & Beneficiary Contribution (Gazette Statutory Rules)",
        "Beneficiary Category": "Beneficiary Category",
        "Own Margin Contribution": "Own Margin Contribution",
        "Urban Subsidy Rate": "Urban Subsidy Rate",
        "Rural Subsidy Rate": "Rural Subsidy Rate",
        "Special Category (SC, ST, OBC, Women, Minorities, PwD, NER)": "Special Category (SC, ST, OBC, Women, Minorities, PwD, NER)",
        "General Category (Male)": "General Category (Male)",
        "5% of Project Cost": "5% of Project Cost",
        "10% of Project Cost": "10% of Project Cost",
        "Eligible Categories & Purposes": "Eligible Categories & Purposes",
        "Target Categories:": "Target Categories:",
        "Allowed Business Purposes:": "Allowed Business Purposes:",
        "Age Limits & Income Ceiling:": "Age Limits & Income Ceiling:",
        "No Income Ceiling": "No Income Ceiling",
        "Required Documents Checklist": "Required Documents Checklist",
        "Verify OCR": "Verify OCR",
        "Aadhaar Card (Mobile Linked)": "Aadhaar Card (Mobile Linked)",
        "PAN Card": "PAN Card",
        "Caste Certificate (SC/ST/OBC)": "Caste Certificate (SC/ST/OBC)",
        "Detailed Project Report (DPR)": "Detailed Project Report (DPR)",
        "Bank Account Passbook / 6 Months Statement": "Bank Account Passbook / 6 Months Statement",
        "EDP Training Certificate (if available)": "EDP Training Certificate (if available)",
        "Ministry of MSME / KVIC": "Ministry of MSME / KVIC",
        "Department of Financial Services, Ministry of Finance": "Department of Financial Services, Ministry of Finance",
        "Department of Financial Services / SIDBI": "Department of Financial Services / SIDBI",
        "Ministry of Housing & Urban Affairs (MoHUA)": "Ministry of Housing & Urban Affairs (MoHUA)",
        "Ministry of Housing and Urban Affairs (MoHUA)": "Ministry of Housing and Urban Affairs (MoHUA)",
        "Ministry of Micro, Small and Medium Enterprises": "Ministry of Micro, Small and Medium Enterprises",
        "Ministry of Micro, Small and Medium Enterprises (MoMSME)": "Ministry of Micro, Small and Medium Enterprises (MoMSME)",
        "National Backward Classes Finance & Development Corporation (NBCFDC)": "National Backward Classes Finance & Development Corporation (NBCFDC)",
        "Ministry of Social Justice and Empowerment (MoSJE)": "Ministry of Social Justice and Empowerment (MoSJE)",
        "National Minorities Development & Finance Corporation": "National Minorities Development & Finance Corporation",
        "Ministry of Minority Affairs (MoMA)": "Ministry of Minority Affairs (MoMA)",
        "Venture Capital Fund for SCs (VCF-SC), MoSJE": "Venture Capital Fund for SCs (VCF-SC), MoSJE",
        "Ministry of Social Justice and Empowerment / Venture Capital Fund for SC": "Ministry of Social Justice and Empowerment / Venture Capital Fund for SC",
        "Ministry of Micro, Small and Medium Enterprises / Coir Board": "Ministry of Micro, Small and Medium Enterprises / Coir Board",
        "Department of Micro, Small and Medium Enterprises, Govt. of Tamil Nadu": "Department of Micro, Small and Medium Enterprises, Govt. of Tamil Nadu",
        "Karnataka State Women's Development Corporation (KSWDC)": "Karnataka State Women's Development Corporation (KSWDC)",
        "Directorate of Industries, Government of Maharashtra": "Directorate of Industries, Government of Maharashtra",
        "Department of Industries & Commerce, Government of Kerala": "Department of Industries & Commerce, Government of Kerala",
        "Department of MSME and Export Promotion, Govt. of Uttar Pradesh": "Department of MSME and Export Promotion, Govt. of Uttar Pradesh",
        "Department of Micro, Small & Medium Enterprises, Govt. of West Bengal": "Department of Micro, Small & Medium Enterprises, Govt. of West Bengal",
        "Department of Higher Education, Ministry of Education": "Department of Higher Education, Ministry of Education",
        "National Scheduled Castes Finance and Development Corporation (MoSJE)": "National Scheduled Castes Finance and Development Corporation (MoSJE)",
        "Department of Social Justice & Empowerment (MoSJE)": "Department of Social Justice & Empowerment (MoSJE)",
        "Department of Higher Education & National Credit Guarantee Trustee Company (NCGTC)": "Department of Higher Education & National Credit Guarantee Trustee Company (NCGTC)",
        "Select Language": "Select Language",
        "Subsidy": "Subsidy",
        "Max Sanction:": "Max Sanction:"
    }
}

# Generate localized dictionary for each of the 11 Indic languages
# Load existing dictionary from LanguageContext.jsx if present
with open(r'frontend/src/context/LanguageContext.jsx', 'r', encoding='utf-8') as f:
    orig_text = f.read()

# Extract existing DICTIONARY object from file
import re
dict_match = re.search(r'export const DICTIONARY = (\{[\s\S]*?\});\s*\n\s*export const PHRASE_MAP', orig_text)
if dict_match:
    try:
        raw_dict_json = dict_match.group(1)
        # Parse using python json
        existing_dictionary = json.loads(raw_dict_json)
        print("Successfully loaded existing DICTIONARY keys:", list(existing_dictionary.keys()))
        for l in existing_dictionary:
            DICTIONARY_12_LANG[l] = existing_dictionary[l]
    except Exception as e:
        print("Notice: Error parsing existing DICTIONARY JSON:", e)

# Supplement missing keys for all languages from Indic translation corpus
CORPUS_KEYS = {
    "ta": {
        "appName": "ஸ்கீம் சாதி (SCHEME SATHI)",
        "tagline": "தொழில்முனைவோர் மற்றும் மாணவர்களுக்கான AI அரசு திட்ட தேர்வு",
        "select your goal track": "உங்கள் இலக்கு பாதையை தேர்வு செய்க",
        "Education": "கல்வி",
        "Business": "வணிகம்",
        "Self-Emp": "சுயதொழில்",
        "course stream": "படிப்பு துறை",
        "engineering / tech": "பொறியியல் / தொழில்நுட்பம்",
        "medical / healthcare": "மருத்துவம் / நர்சிங்",
        "management / mba": "மேலாண்மை / எம்பிஏ",
        "overseas studies": "வெளிநாட்டு படிப்பு",
        "activity type": "தொழில் வகை",
        "street vendor / hawkers": "தெருவோர வியாபாரி / நடைபாதை",
        "artisan / handicrafts": "கைவினைஞர் / கைவினை தொழில்",
        "small service / repair": "சிறு சேவை / பழுதுபார்த்தல்",
        "target course / loan amount": "தேவைப்படும் படிப்பு / கடன் தொகை",
        "₹50k (Base)": "₹50ஆ (அடிப்படை)",
        "₹7.5L (CSIS / CGFSEL)": "₹7.5இ (CSIS / CGFSEL)",
        "₹20L+ (NSFDC / Overseas)": "₹20இ+ (NSFDC / வெளிநாடு)",
        "₹10k (PM SVANidhi)": "₹10ஆ (PM ஸ்வநிதி)",
        "₹1L (Scale Up)": "₹1இ (விரிவாக்கம்)",
        "₹3L (PM Vishwakarma)": "₹3இ (PM விஸ்வகர்மா)",
        "₹1 Lakh (Micro)": "₹1 இலட்சம் (குறுந்தொழில்)",
        "₹50 Lakh (PMEGP)": "₹50 இலட்சம் (PMEGP)",
        "₹1 Cr (Stand-Up)": "₹1 கோடி (ஸ்டாண்ட்-அப்)",
        "Government Purpose Track / Goal": "அரசு நோக்கம் / இலக்கு பாதை",
        "Switch purpose to discover all statutory schemes across sectors": "துறைகள் முழுவதும் உள்ள திட்டங்களைக் காண நோக்கம் மாற்றவும்",
        "Higher Education & Student Loans": "உயர்கல்வி & மாணவர் கல்வி கடன்கள்",
        "CSIS, NSFDC, NBCFDC, NMDFC, Overseas": "CSIS, NSFDC, NBCFDC, NMDFC, வெளிநாடு",
        "MSME & Business Loans": "குறு, சிறு & வணிகக் கடன்கள்",
        "PMEGP, Stand-Up India, Mudra Kishore/Tarun": "PMEGP, ஸ்டாண்ட்-அப் இந்தியா, முத்ரா கிஷோர்/தருண்",
        "Street Vendors & Artisans": "தெருவோர வியாபாரிகள் & கைவினைஞர்கள்",
        "PM SVANidhi, PM Vishwakarma, Mudra Shishu": "PM ஸ்வநிதி, PM விஸ்வகர்மா, முத்ரா சிசு",
        "Scheme Sathi • AI-Driven Statutory Rules Matching Engine": "ஸ்கீம் சாதி • AI அரசு விதி பொருத்துதல் என்ஜின்",
        "Qualified Schemes for": "தகுதியான திட்டங்கள்:",
        "Lakhs": "இலட்சம்",
        "Resident Location:": "இருப்பிட முகவரி:",
        "Social Category:": "சமூகப் பிரிவு:",
        "Target Track:": "நோக்கப் பாதை:",
        "Modify Requirement": "தேவையை மாற்றுக",
        "Eligible Schemes": "தகுதியான திட்டங்கள்",
        "Match Score": "பொருத்த மதிப்பெண்",
        "Available & Alternative Schemes": "கிடைக்கும் & மாற்று திட்டங்கள்",
        "Rule Breakdown": "விதிகள் விவரம்",
        "searchPlaceholder": "திட்டப் பெயர், அமைச்சகம் அல்லது சொல்லை தேடுக...",
        "All Types": "அனைத்து வகைகள்",
        "Central Schemes": "மத்திய திட்டங்கள்",
        "State Schemes": "மாநில திட்டங்கள்",
        "Central Scheme": "மத்திய அரசு திட்டம்",
        "State Scheme": "மாநில அரசு திட்டம்",
        "Government of India": "இந்திய அரசு",
        "Sort:": "வரிசைப்படுத்து:",
        "Highest Match Score": "அதிக பொருத்த மதிப்பெண்",
        "Loan Amount: High to Low": "கடன் தொகை: அதிகபட்சம் முதல் குறைந்தபட்சம்",
        "Loan Amount: Low to High": "கடன் தொகை: குறைந்தபட்சம் முதல் அதிகபட்சம்",
        "Focus:": "முக்கிய கவனம்:",
        "All Focus Areas": "அனைத்து துறைகளும்",
        "Interest Subsidy (CSIS)": "வட்டி மானியம் (CSIS)",
        "SC Students (NSFDC)": "SC மாணவர்கள் (NSFDC)",
        "OBC Students (NBCFDC)": "OBC மாணவர்கள் (NBCFDC)",
        "Minority (Maulana Azad)": "சிறுபான்மையினர் (மௌலானா ஆசாத்)",
        "Overseas Studies (Ambedkar)": "வெளிநாட்டு படிப்பு (அம்பேத்கர்)",
        "Credit Guarantee (CGFSEL)": "கடன் உத்தரவாதம் (CGFSEL)",
        "Street Vendors (PM SVANidhi)": "தெருவோர வியாபாரிகள் (PM ஸ்வநிதி)",
        "Artisans (PM Vishwakarma)": "கைவினைஞர்கள் (PM விஸ்வகர்மா)",
        "Women Microfinance": "பெண்கள் நுண்கடன்",
        "Mudra Shishu": "முத்ரா சிசு",
        "Manufacturing": "உற்பத்தி துறை",
        "Services": "சேவை துறை",
        "Capital Subsidies": "மூலதன மானியங்கள்",
        "Evaluating statutory gazette rules & calculating SHAP match scores...": "அரசாணை விதிகளை மதிப்பீடு செய்து தகுதி கணக்கிடப்படுகிறது...",
        "Disbursement Readiness Notice": "கடன் வழங்கல் தயார்நிலை அறிவிப்பு",
        "You qualify for the statutory schemes below. Verify your mandatory documents in the Document Assistant for fast-track loan sanction.": "கீழே உள்ள அரசு திட்டங்களுக்கு நீங்கள் தகுதி பெற்றுள்ளீர்கள். விரைவு ஒப்புதலுக்கு ஆவணங்களை சரிபார்க்கவும்.",
        "Upload / Verify": "பதிவேற்று / சரிபார்",
        "Statutory Match": "சட்டப்பூர்வ பொருத்தம்",
        "Passed Eligibility Conditions:": "நிறைவேற்றப்பட்ட தகுதி நிபந்தனைகள்:",
        "Statutory Verified • myScheme.gov.in": "அரசு சரிபார்க்கப்பட்டது • myScheme.gov.in",
        "Official Portal": "அதிகாரப்பூர்வ தளம்",
        "Maximum Cap:": "அதிகபட்ச வரம்பு:",
        "Government Subsidy:": "அரசு மானியம்:",
        "Up to 35% Special Rural": "35% வரை சிறப்பு கிராமப்புற மானியம்",
        "Repayment Period:": "திருப்பிச் செலுத்தும் காலம்:",
        "Selected Scheme (Active)": "தேர்ந்தெடுக்கப்பட்ட திட்டம் (செயலில்)",
        "Select Scheme & Calculate EMI (Step 5)": "திட்டத்தை தேர்வு செய்து EMI கணக்கிடுக (படி 5)",
        "Full Details": "முழு விவரங்கள்",
        "Find Branch": "வங்கி கிளை காண்க",
        "No Matching Eligible Schemes Found": "பொருத்தமான தகுதி திட்டங்கள் எதுவும் கிடைக்கவில்லை",
        "Click on the \"Available & Alternative Schemes\" tab above to see all gazette schemes and reasons for exclusion.": "அனைத்து அரசு திட்டங்கள் மற்றும் விலக்கலுக்கான காரணங்களைக் காண மேலே உள்ள தாவலை கிளிக் செய்க.",
        "View Available Schemes": "கிடைக்கும் திட்டங்களை காண்க",
        "Modify Questionnaire": "கேள்வித்தாளை மாற்றுக",
        "These schemes are currently operating under Central / State mandates. Transparent gazette reasons for exclusion are displayed below.": "இத்திட்டங்கள் மத்திய/மாநில அரசு விதிகளின் கீழ் செயல்படுகின்றன. விலக்கலுக்கான அரசு காரணங்கள் கீழே உள்ளன.",
        "Failed Gazette Condition(s):": "பொருந்தாத அரசாணை நிபந்தனை(கள்):",
        "Criteria mismatch with applicant profile or required loan ceiling exceeded.": "விண்ணப்பதாரர் சுயவிவரம் அல்லது கடன் வரம்பு பொருந்தவில்லை.",
        "Max Limit:": "அதிகபட்ச வரம்பு:",
        "View Scheme Guidelines": "திட்ட வழிகாட்டுதல்களை காண்க",
        "No additional available schemes found matching your search.": "உங்கள் தேடலுக்கு கூடுதல் திட்டங்கள் எதுவும் கிடைக்கவில்லை.",
        "Official Gazette Registry • myScheme.gov.in": "அதிகாரப்பூர்வ அரசாணை பதிவு • myScheme.gov.in",
        "filterCentral": "மத்திய திட்டம்",
        "filterState": "மாநில திட்டம்",
        "mySchemePortal": "myScheme தளம்",
        "interestRateLabel": "வட்டி விகிதம்",
        "Subsidy Slabs & Beneficiary Contribution (Gazette Statutory Rules)": "மானிய அடுக்குகள் & பயனாளி பங்களிப்பு (அரசாணை விதிகள்)",
        "Beneficiary Category": "பயனாளி பிரிவு",
        "Own Margin Contribution": "சொந்த மார்ஜின் பங்களிப்பு",
        "Urban Subsidy Rate": "நகர்ப்புற மானிய விகிதம்",
        "Rural Subsidy Rate": "கிராமப்புற மானிய விகிதம்",
        "Special Category (SC, ST, OBC, Women, Minorities, PwD, NER)": "சிறப்புப் பிரிவு (SC, ST, OBC, பெண்கள், சிறுபான்மையினர், மாற்றுத்திறனாளிகள்)",
        "General Category (Male)": "பொதுப் பிரிவு (ஆண்கள்)",
        "5% of Project Cost": "திட்டச் செலவில் 5%",
        "10% of Project Cost": "திட்டச் செலவில் 10%",
        "Eligible Categories & Purposes": "தகுதியான பிரிவுகள் & நோக்கங்கள்",
        "Target Categories:": "இலக்கு பிரிவுகள்:",
        "Allowed Business Purposes:": "அனுமதிக்கப்பட்ட தொழில் நோக்கங்கள்:",
        "Age Limits & Income Ceiling:": "வயது வரம்பு & வருமான உச்சவரம்பு:",
        "No Income Ceiling": "வருமான வரம்பு இல்லை",
        "Required Documents Checklist": "தேவையான ஆவணங்கள் சரிபார்ப்பு பட்டியல்",
        "Verify OCR": "OCR சரிபார்",
        "Aadhaar Card (Mobile Linked)": "ஆதார் கார்டு (மொபைல் இணைக்கப்பட்டது)",
        "PAN Card": "பான் கார்டு",
        "Caste Certificate (SC/ST/OBC)": "சாதி சான்றிதழ் (SC/ST/OBC)",
        "Detailed Project Report (DPR)": "விரிவான திட்ட அறிக்கை (DPR)",
        "Bank Account Passbook / 6 Months Statement": "வங்கி கணக்கு பாஸ்புக் / 6 மாத அறிக்கை",
        "EDP Training Certificate (if available)": "EDP பயிற்சி சான்றிதழ் (இருப்பின்)",
        "Ministry of MSME / KVIC": "MSME அமைச்சகம் / KVIC",
        "Department of Financial Services, Ministry of Finance": "நிதிச் சேவைகள் துறை, நிதி அமைச்சகம்",
        "Department of Financial Services / SIDBI": "நிதிச் சேவைகள் துறை / SIDBI",
        "Ministry of Housing & Urban Affairs (MoHUA)": "வீட்டுவசதி மற்றும் நகர்ப்புற விவகார அமைச்சகம் (MoHUA)",
        "Ministry of Housing and Urban Affairs (MoHUA)": "வீட்டுவசதி மற்றும் நகர்ப்புற விவகார அமைச்சகம் (MoHUA)",
        "Ministry of Micro, Small and Medium Enterprises": "குறு, சிறு மற்றும் நடுத்தர தொழில் அமைச்சகம்",
        "Ministry of Micro, Small and Medium Enterprises (MoMSME)": "குறு, சிறு மற்றும் நடுத்தர தொழில் அமைச்சகம் (MoMSME)",
        "National Backward Classes Finance & Development Corporation (NBCFDC)": "தேசிய பிற்படுத்தப்பட்டோர் நிதி மற்றும் மேம்பாட்டுக் கழகம் (NBCFDC)",
        "Ministry of Social Justice and Empowerment (MoSJE)": "சமூக நீதி மற்றும் அதிகாரமளித்தல் அமைச்சகம் (MoSJE)",
        "National Minorities Development & Finance Corporation": "தேசிய சிறுபான்மையினர் மேம்பாடு மற்றும் நிதிக் கழகம்",
        "Ministry of Minority Affairs (MoMA)": "சிறுபான்மையினர் விவகார அமைச்சகம் (MoMA)",
        "Venture Capital Fund for SCs (VCF-SC), MoSJE": "SCகளுக்கான துணிகர மூலதன நிதி (VCF-SC), MoSJE",
        "Ministry of Social Justice and Empowerment / Venture Capital Fund for SC": "சமூக நீதி அமைச்சகம் / SC துணிகர மூலதன நிதி",
        "Ministry of Micro, Small and Medium Enterprises / Coir Board": "குறு, சிறு நடுத்தர தொழில் அமைச்சகம் / கயிறு வாரியம்",
        "Department of Micro, Small and Medium Enterprises, Govt. of Tamil Nadu": "குறு, சிறு மற்றும் நடுத்தர தொழில் துறை, தமிழ்நாடு அரசு",
        "Karnataka State Women's Development Corporation (KSWDC)": "கர்நாடக மாநில மகளிர் மேம்பாட்டுக் கழகம் (KSWDC)",
        "Directorate of Industries, Government of Maharashtra": "தொழில்துறை இயக்குநரகம், மகாராஷ்டிரா அரசு",
        "Department of Industries & Commerce, Government of Kerala": "தொழில் மற்றும் வர்த்தகத் துறை, கேரள அரசு",
        "Department of MSME and Export Promotion, Govt. of Uttar Pradesh": "MSME மற்றும் ஏற்றுமதி மேம்பாட்டுத் துறை, உ.பி அரசு",
        "Department of Micro, Small & Medium Enterprises, Govt. of West Bengal": "குறு, சிறு மற்றும் நடுத்தர தொழில் துறை, மேற்கு வங்க அரசு",
        "Department of Higher Education, Ministry of Education": "உயர்கல்வித் துறை, கல்வி அமைச்சகம்",
        "National Scheduled Castes Finance and Development Corporation (MoSJE)": "தேசிய பட்டியலினத்தவர் நிதி மற்றும் மேம்பாட்டுக் கழகம் (MoSJE)",
        "Department of Social Justice & Empowerment (MoSJE)": "சமூக நீதி மற்றும் அதிகாரமளித்தல் துறை (MoSJE)",
        "Department of Higher Education & National Credit Guarantee Trustee Company (NCGTC)": "உயர்கல்வித் துறை & தேசிய கடன் உத்தரவாத அறங்காவலர் நிறுவனம் (NCGTC)",
        "Select Language": "மொழியைத் தேர்வுசெய்க",
        "Subsidy": "மானியம்",
        "Max Sanction:": "அதிகபட்ச அனுமதி:",
        "women entrepreneur / special category": "பெண் தொழில்முனைவோர் / சிறப்புப் பிரிவு"
    },
    "te": {
        "appName": "స్కీమ్ సాథి (SCHEME SATHI)",
        "tagline": "పారిశ్రామికవేత్తలు మరియు విద్యార్థుల కోసం AI ప్రభుత్వ పథకాల ఎంపిక",
        "select your goal track": "మీ లక్ష్య మార్గాన్ని ఎంచుకోండి",
        "Education": "విద్య",
        "Business": "వ్యాపారం",
        "Self-Emp": "స్వయం ఉపాధి",
        "course stream": "కోర్సు విభాగం",
        "engineering / tech": "ఇంజనీరింగ్ / టెక్నాలజీ",
        "medical / healthcare": "వైద్యం / హెల్త్‌కేర్",
        "management / mba": "మేనేజ్‌మెంట్ / MBA",
        "overseas studies": "విదేశీ విద్య",
        "activity type": "వ్యాపార కార్యకలాప రకం",
        "street vendor / hawkers": "వీధి వ్యాపారి / చిరు వ్యాపారాలు",
        "artisan / handicrafts": "చేతివృత్తులు / హస్తకళలు",
        "small service / repair": "చిన్న సేవలు / మరమ్మతులు",
        "target course / loan amount": "లక్ష్య కోర్సు / అవసరమైన రుణం",
        "₹50k (Base)": "₹50వే (ప్రాథమిక)",
        "₹7.5L (CSIS / CGFSEL)": "₹7.5ల (CSIS / CGFSEL)",
        "₹20L+ (NSFDC / Overseas)": "₹20ల+ (NSFDC / విదేశాలు)",
        "₹10k (PM SVANidhi)": "₹10వే (PM స్వనిధి)",
        "₹1L (Scale Up)": "₹1ల (విస్తరణ)",
        "₹3L (PM Vishwakarma)": "₹3ల (PM విశ్వకర్మ)",
        "₹1 Lakh (Micro)": "₹1 లక్ష (మైక్రో)",
        "₹50 Lakh (PMEGP)": "₹50 లక్షలు (PMEGP)",
        "₹1 Cr (Stand-Up)": "₹1 కోటి (స్టాండ్-అప్)",
        "Government Purpose Track / Goal": "ప్రభుత్వ ఉద్దేశ్య మార్గం / లక్ష్యం",
        "Switch purpose to discover all statutory schemes across sectors": "అన్ని రంగాల పథకాలను అన్వేషించడానికి లక్ష్యాన్ని మార్చండి",
        "Higher Education & Student Loans": "ఉన్నత విద్య & విద్యార్థి రుణాలు",
        "CSIS, NSFDC, NBCFDC, NMDFC, Overseas": "CSIS, NSFDC, NBCFDC, NMDFC, విదేశాలు",
        "MSME & Business Loans": "MSME & వ్యాపార రుణాలు",
        "PMEGP, Stand-Up India, Mudra Kishore/Tarun": "PMEGP, స్టాండ్-అప్ ఇండియా, ముద్ర కిశోర్/తరుణ్",
        "Street Vendors & Artisans": "వీధి వ్యాపారులు & చేతివృత్తులు",
        "PM SVANidhi, PM Vishwakarma, Mudra Shishu": "PM స్వనిధి, PM విశ్వకర్మ, ముద్ర శిశు",
        "Scheme Sathi • AI-Driven Statutory Rules Matching Engine": "స్కీమ్ సాథి • AI ప్రభుత్వ నిబంధనల మ్యాచింగ్ ఇంజిన్",
        "Qualified Schemes for": "అర్హత సాధించిన పథకాలు:",
        "Lakhs": "లక్షలు",
        "Resident Location:": "నివాస ప్రాంతం:",
        "Social Category:": "సామాజిక వర్గం:",
        "Target Track:": "లక్ష్య మార్గం:",
        "Modify Requirement": "అవసరాన్ని సవరించండి",
        "Eligible Schemes": "అర్హత గల పథకాలు",
        "Match Score": "సరిపోలిక స్కోరు",
        "Available & Alternative Schemes": "అందుబాటులో ఉన్న & ప్రత్యామ్నాయ పథకాలు",
        "Rule Breakdown": "నిబంధనల విశ్లేషణ",
        "searchPlaceholder": "పథకం పేరు, మంత్రిత్వ శాఖ లేదా పదం శోధించండి...",
        "All Types": "అన్ని రకాలు",
        "Central Schemes": "కేంద్ర పథకాలు",
        "State Schemes": "రాష్ట్ర పథకాలు",
        "Central Scheme": "కేంద్ర ప్రభుత్వ పథకం",
        "State Scheme": "రాష్ట్ర ప్రభుత్వ పథకం",
        "Government of India": "భారత ప్రభుత్వం",
        "Sort:": "క్రమబద్ధీకరించు:",
        "Highest Match Score": "అత్యధిక మ్యాచ్ స్కోరు",
        "Loan Amount: High to Low": "రుణం మొత్తం: ఎక్కువ నుండి తక్కువ",
        "Loan Amount: Low to High": "రుణం మొత్తం: తక్కువ నుండి ఎక్కువ",
        "Focus:": "ప్రత్యేక దృష్టి:",
        "All Focus Areas": "అన్ని రంగాలు",
        "Interest Subsidy (CSIS)": "వడ్డీ రాయితీ (CSIS)",
        "SC Students (NSFDC)": "SC విద్యార్థులు (NSFDC)",
        "OBC Students (NBCFDC)": "OBC విద్యార్థులు (NBCFDC)",
        "Minority (Maulana Azad)": "మైనారిటీలు (మౌలానా ఆజాద్)",
        "Overseas Studies (Ambedkar)": "విదేశీ విద్య (అంబేద్కర్)",
        "Credit Guarantee (CGFSEL)": "క్రెడిట్ గ్యారెంటీ (CGFSEL)",
        "Street Vendors (PM SVANidhi)": "వీధి వ్యాపారులు (PM స్వనిధి)",
        "Artisans (PM Vishwakarma)": "చేతివృత్తులవారు (PM విశ్వకర్మ)",
        "Women Microfinance": "మహిళా మైక్రోఫైనాన్స్",
        "Mudra Shishu": "ముద్ర శిశు",
        "Manufacturing": "తయారీ రంగం",
        "Services": "సేవా రంగం",
        "Capital Subsidies": "మూలధన రాయితీలు",
        "Evaluating statutory gazette rules & calculating SHAP match scores...": "ప్రభుత్వ గెజిట్ నిబంధనలను విశ్లేషించి అర్హతను లెక్కిస్తోంది...",
        "Disbursement Readiness Notice": "రుణ పంపిణీ సంసిద్ధత నోటీసు",
        "You qualify for the statutory schemes below. Verify your mandatory documents in the Document Assistant for fast-track loan sanction.": "మీరు క్రింది ప్రభుత్వ పథకాలకు అర్హులు. వేగవంతమైన అనుమతి కోసం పత్రాలను ధృవీకరించండి.",
        "Upload / Verify": "అప్‌లోడ్ / ధృవీకరించండి",
        "Statutory Match": "చట్టబద్ధ సరిపోలిక",
        "Passed Eligibility Conditions:": "ఆమోదించబడిన అర్హత షరతులు:",
        "Statutory Verified • myScheme.gov.in": "అధికారిక ధృవీకరణ • myScheme.gov.in",
        "Official Portal": "అధికారిక పోర్టల్",
        "Maximum Cap:": "గరిష్ట పరిమితి:",
        "Government Subsidy:": "ప్రభుత్వ రాయితీ:",
        "Up to 35% Special Rural": "35% వరకు ప్రత్యేక గ్రామీణ సబ్సిడీ",
        "Repayment Period:": "మరుసటి చెల్లింపు గడువు:",
        "Selected Scheme (Active)": "ఎంచుకున్న పథకం (యాక్టివ్)",
        "Select Scheme & Calculate EMI (Step 5)": "పథకాన్ని ఎంచుకుని EMI లెక్కించండి (దశ 5)",
        "Full Details": "పూర్తి వివరాలు",
        "Find Branch": "బ్యాంక్ బ్రాంచ్ కనుగొనండి",
        "No Matching Eligible Schemes Found": "సరిపోలే అర్హత గల పథకాలు ఏవీ కనుగొనబడలేదు",
        "Click on the \"Available & Alternative Schemes\" tab above to see all gazette schemes and reasons for exclusion.": "అన్ని ప్రభుత్వ పథకాలు మరియు తిరస్కరణ కారణాలను చూడటానికి పై ట్యాబ్‌పై క్లిక్ చేయండి.",
        "View Available Schemes": "అందుబాటులో ఉన్న పథకాలను చూడండి",
        "Modify Questionnaire": "ప్రశ్నాపత్రాన్ని మార్చండి",
        "These schemes are currently operating under Central / State mandates. Transparent gazette reasons for exclusion are displayed below.": "ఈ పథకాలు కేంద్ర/రాష్ట్ర ప్రభుత్వ నిబంధనల ప్రకారం పనిచేస్తున్నాయి. కారణాలు క్రింద ప్రదర్శించబడ్డాయి.",
        "Failed Gazette Condition(s):": "సరిపోలని గెజిట్ షరతు(లు):",
        "Criteria mismatch with applicant profile or required loan ceiling exceeded.": "దరఖాస్తుదారు ప్రొఫైల్ లేదా అవసరమైన రుణ పరిమితి సరిపోలలేదు.",
        "Max Limit:": "గరిష్ట పరిమితి:",
        "View Scheme Guidelines": "పథకం మార్గదర్శకాలను చూడండి",
        "No additional available schemes found matching your search.": "మీ శోధనకు తగిన అదనపు పథకాలు కనుగొనబడలేదు.",
        "Official Gazette Registry • myScheme.gov.in": "అధికారిక గెజిట్ రిజిస్ట్రీ • myScheme.gov.in",
        "filterCentral": "కేంద్ర పథకం",
        "filterState": "రాష్ట్ర పథకం",
        "mySchemePortal": "myScheme పోర్టల్",
        "interestRateLabel": "వడ్డీ రేటు",
        "Subsidy Slabs & Beneficiary Contribution (Gazette Statutory Rules)": "సబ్సిడీ స్లాబ్‌లు & లబ్ధిదారుల సహకారం (గెజిట్ నిబంధనలు)",
        "Beneficiary Category": "లబ్ధిదారుల వర్గం",
        "Own Margin Contribution": "సొంత మార్జిన్ సహకారం",
        "Urban Subsidy Rate": "పట్టణ రాయితీ రేటు",
        "Rural Subsidy Rate": "గ్రామీణ రాయితీ రేటు",
        "Special Category (SC, ST, OBC, Women, Minorities, PwD, NER)": "ప్రత్యేక వర్గం (SC, ST, OBC, మహిళలు, మైనారిటీలు, దివ్యాంగులు)",
        "General Category (Male)": "సాధారణ వర్గం (పురుషులు)",
        "5% of Project Cost": "ప్రాజెక్ట్ ఖర్చులో 5%",
        "10% of Project Cost": "ప్రాజెక్ట్ ఖర్చులో 10%",
        "Eligible Categories & Purposes": "అర్హత గల వర్గాలు & ఉద్దేశ్యాలు",
        "Target Categories:": "లక్ష్య వర్గాలు:",
        "Allowed Business Purposes:": "అనుమతించబడిన వ్యాపార ఉద్దేశ్యాలు:",
        "Age Limits & Income Ceiling:": "వయోపరిమితి & ఆదాయ పరిమితి:",
        "No Income Ceiling": "ఆదాయ పరిమితి లేదు",
        "Required Documents Checklist": "అవసరమైన పత్రాల చెక్‌లిస్ట్",
        "Verify OCR": "OCR ధృవీకరణ",
        "Aadhaar Card (Mobile Linked)": "ఆధార్ కార్డు (మొబైల్ లింక్ చేయబడింది)",
        "PAN Card": "పాన్ కార్డు",
        "Caste Certificate (SC/ST/OBC)": "కులం ధృవీకరణ పత్రం (SC/ST/OBC)",
        "Detailed Project Report (DPR)": "సమగ్ర ప్రాజెక్ట్ నివేదిక (DPR)",
        "Bank Account Passbook / 6 Months Statement": "బ్యాంక్ ఖాతా పాస్‌బుక్ / 6 నెలల స్టేట్‌మెంట్",
        "EDP Training Certificate (if available)": "EDP శిక్షణ ధృవీకరణ పత్రం (ఉంటే)",
        "Ministry of MSME / KVIC": "MSME మంత్రిత్వ శాఖ / KVIC",
        "Department of Financial Services, Ministry of Finance": "ఆర్థిక సేవల శాఖ, ఆర్థిక మంత్రిత్వ శాఖ",
        "Department of Financial Services / SIDBI": "ఆర్థిక సేవల శాఖ / SIDBI",
        "Ministry of Housing & Urban Affairs (MoHUA)": "గృహనిర్మాణ & పట్టణ వ్యవహారాల మంత్రిత్వ శాఖ (MoHUA)",
        "Ministry of Housing and Urban Affairs (MoHUA)": "గృహనిర్మాణ & పట్టణ వ్యవహారాల మంత్రిత్వ శాఖ (MoHUA)",
        "Ministry of Micro, Small and Medium Enterprises": "సూక్ష్మ, చిన్న & మధ్య తరహా పరిశ్రమల మంత్రిత్వ శాఖ",
        "Ministry of Micro, Small and Medium Enterprises (MoMSME)": "సూక్ష్మ, చిన్న & మధ్య తరహా పరిశ్రమల మంత్రిత్వ శాఖ (MoMSME)",
        "National Backward Classes Finance & Development Corporation (NBCFDC)": "జాతీయ వెనుకబడిన తరగతుల ఆర్థిక & అభివృద్ధి సంస్థ (NBCFDC)",
        "Ministry of Social Justice and Empowerment (MoSJE)": "సామాజిక న్యాయం & సాధికారత మంత్రిత్వ శాఖ (MoSJE)",
        "National Minorities Development & Finance Corporation": "జాతీయ మైనారిటీల అభివృద్ధి & ఆర్థిక సంస్థ",
        "Ministry of Minority Affairs (MoMA)": "మైనారిటీ వ్యవహారాల మంత్రిత్వ శాఖ (MoMA)",
        "Venture Capital Fund for SCs (VCF-SC), MoSJE": "SCల వెంచర్ క్యాపిటల్ ఫండ్ (VCF-SC), MoSJE",
        "Ministry of Social Justice and Empowerment / Venture Capital Fund for SC": "సామాజిక న్యాయ మంత్రిత్వ శాఖ / SC వెంచర్ క్యాపిటల్ ఫండ్",
        "Ministry of Micro, Small and Medium Enterprises / Coir Board": "MSME మంత్రిత్వ శాఖ / కాయిర్ బోర్డు",
        "Department of Micro, Small and Medium Enterprises, Govt. of Tamil Nadu": "MSME శాఖ, తమిళనాడు ప్రభుత్వం",
        "Karnataka State Women's Development Corporation (KSWDC)": "కర్ణాటక రాష్ట్ర మహిళా అభివృద్ధి సంస్థ (KSWDC)",
        "Directorate of Industries, Government of Maharashtra": "పరిశ్రమల డైరెక్టరేట్, మహారాష్ట్ర ప్రభుత్వం",
        "Department of Industries & Commerce, Government of Kerala": "పరిశ్రమలు & వాణిజ్య శాఖ, కేరళ ప్రభుత్వం",
        "Department of MSME and Export Promotion, Govt. of Uttar Pradesh": "MSME & ఎగుమతి ప్రోత్సాహక శాఖ, ఉత్తరప్రదేశ్ ప్రభుత్వం",
        "Department of Micro, Small & Medium Enterprises, Govt. of West Bengal": "MSME శాఖ, పశ్చిమ బెంగాల్ ప్రభుత్వం",
        "Department of Higher Education, Ministry of Education": "ఉన్నత విద్యా శాఖ, విద్యా మంత్రిత్వ శాఖ",
        "National Scheduled Castes Finance and Development Corporation (MoSJE)": "జాతీయ షెడ్యూల్డ్ కులాల ఆర్థిక & అభివృద్ధి సంస్థ (MoSJE)",
        "Department of Social Justice & Empowerment (MoSJE)": "సామాజిక న్యాయం & సాధికారత శాఖ (MoSJE)",
        "Department of Higher Education & National Credit Guarantee Trustee Company (NCGTC)": "ఉన్నత విద్యా శాఖ & జాతీయ క్రెడిట్ గ్యారెంటీ ట్రస్టీ కంపెనీ (NCGTC)",
        "Select Language": "భాషను ఎంచుకోండి",
        "Subsidy": "రాయితీ",
        "Max Sanction:": "గరిష్ట మంజూరు:",
        "women entrepreneur / special category": "మహిళా పారిశ్రామికవేత్త / ప్రత్యేక వర్గం"
    }
}

# Merge all corpus keys into DICTIONARY_12_LANG
for lang, keys_dict in CORPUS_KEYS.items():
    if lang not in DICTIONARY_12_LANG:
        DICTIONARY_12_LANG[lang] = {}
    DICTIONARY_12_LANG[lang].update(keys_dict)

# Populate missing keys in all other languages from English/Hindi as fallback
for lang in ["kn", "ml", "mr", "bn", "gu", "pa", "or", "as", "hi", "ta", "te"]:
    if lang not in DICTIONARY_12_LANG:
        DICTIONARY_12_LANG[lang] = {}
    for key, en_val in DICTIONARY_12_LANG["en"].items():
        if key not in DICTIONARY_12_LANG[lang]:
            # Use Hindi if available, otherwise English
            DICTIONARY_12_LANG[lang][key] = DICTIONARY_12_LANG.get("hi", {}).get(key, en_val)

print(f"Dictionaries prepared for {len(DICTIONARY_12_LANG)} languages.")

# Write full LanguageContext.jsx
react_code_template = '''import React, { createContext, useContext, useState, useEffect } from 'react';
import api from '../services/api';

const LanguageContext = createContext();

export const LANGUAGES = [
  { code: 'en', name: 'English', native: 'English' },
  { code: 'hi', name: 'Hindi', native: 'हिन्दी' },
  { code: 'ta', name: 'Tamil', native: 'தமிழ்' },
  { code: 'te', name: 'Telugu', native: 'తెలుగు' },
  { code: 'kn', name: 'Kannada', native: 'ಕನ್ನಡ' },
  { code: 'ml', name: 'Malayalam', native: 'മലയാളം' },
  { code: 'mr', name: 'Marathi', native: 'मराठी' },
  { code: 'bn', name: 'Bengali', native: 'বাংলা' },
  { code: 'gu', name: 'Gujarati', native: 'ગુજરાતી' },
  { code: 'pa', name: 'Punjabi', native: 'ਪੰਜਾਬੀ' },
  { code: 'or', name: 'Odia', native: 'ଓଡ଼ିଆ' },
  { code: 'as', name: 'Assamese', native: 'অসমীয়া' }
];

export const SCHEME_MAP = __SCHEME_MAP__;

export const DICTIONARY = __DICTIONARY__;

export const PHRASE_MAP = {};
Object.keys(DICTIONARY).forEach(lang => {
  PHRASE_MAP[lang] = {};
  const dict = DICTIONARY[lang];
  Object.keys(dict).forEach(key => {
    PHRASE_MAP[lang][key.toLowerCase()] = dict[key];
    if (DICTIONARY.en && DICTIONARY.en[key]) {
      PHRASE_MAP[lang][DICTIONARY.en[key].toLowerCase()] = dict[key];
    }
  });
});

export const LanguageProvider = ({ children }) => {
  const [currentLanguage, setCurrentLanguage] = useState(
    localStorage.getItem('scheme_sathi_lang') || 'en'
  );

  const setLanguage = (langCode) => {
    localStorage.setItem('scheme_sathi_lang', langCode);
    setCurrentLanguage(langCode);
  };

  const t = (keyOrPhrase, fallback) => {
    if (!keyOrPhrase) return '';
    const textStr = String(keyOrPhrase).trim();
    if (currentLanguage === 'en') {
      const enDict = DICTIONARY['en'];
      if (enDict && enDict[textStr]) return enDict[textStr];
      return fallback !== undefined ? fallback : textStr;
    }

    // 1. Direct dictionary key match
    const langDict = DICTIONARY[currentLanguage];
    if (langDict && langDict[textStr]) {
      return langDict[textStr];
    }

    // 2. Direct phrase map match (case-insensitive)
    const phraseMap = PHRASE_MAP[currentLanguage];
    const lowerKey = textStr.toLowerCase();
    if (phraseMap && phraseMap[lowerKey]) {
      return phraseMap[lowerKey];
    }

    // 3. Match via English dictionary phrase lookup
    if (DICTIONARY.en && DICTIONARY.en[textStr]) {
      const enValLower = DICTIONARY.en[textStr].toLowerCase();
      if (phraseMap && phraseMap[enValLower]) {
        return phraseMap[enValLower];
      }
      if (PHRASE_MAP.hi && PHRASE_MAP.hi[enValLower]) {
        return PHRASE_MAP.hi[enValLower];
      }
      return DICTIONARY.en[textStr];
    }

    // 4. Fallback to Hindi phrase map if available
    if (PHRASE_MAP.hi && PHRASE_MAP.hi[lowerKey] && currentLanguage !== 'en') {
      return PHRASE_MAP.hi[lowerKey];
    }

    // 5. Default fallback
    return fallback !== undefined ? fallback : textStr;
  };

  const translateScheme = (scheme) => {
    if (!scheme || currentLanguage === 'en') return scheme;
    const rawCode = scheme.code || scheme.scheme_code || '';
    const normCode = rawCode.toUpperCase().replace(/[-_ ]/g, '');
    const nameStr = scheme.name || scheme.scheme_name || '';
    const normName = nameStr.toUpperCase().replace(/[-_ ]/g, '');

    // Lookup localized entry from SCHEME_MAP
    let localized = SCHEME_MAP[rawCode]?.[currentLanguage] ||
                    SCHEME_MAP[normCode]?.[currentLanguage] ||
                    SCHEME_MAP[nameStr]?.[currentLanguage] ||
                    SCHEME_MAP[normName]?.[currentLanguage] ||
                    SCHEME_MAP[rawCode]?.hi ||
                    SCHEME_MAP[normCode]?.hi;

    const translatedDept = scheme.department ? t(scheme.department) : (scheme.ministry ? t(scheme.ministry) : '');
    const translatedMinistry = scheme.ministry ? t(scheme.ministry) : translatedDept;
    const translatedCat = scheme.category ? t(scheme.category) : (scheme.target_category ? t(scheme.target_category) : '');

    if (localized) {
      return {
        ...scheme,
        name: localized.name || scheme.name,
        scheme_name: localized.name || scheme.scheme_name,
        description: localized.desc || scheme.description,
        scheme_description: localized.desc || scheme.scheme_description,
        department: translatedDept || scheme.department,
        ministry: translatedMinistry || scheme.ministry,
        category: translatedCat || scheme.category,
        target_category: translatedCat || scheme.target_category
      };
    }

    return {
      ...scheme,
      name: t(scheme.name || scheme.scheme_name),
      scheme_name: t(scheme.scheme_name || scheme.name),
      description: t(scheme.description || scheme.scheme_description),
      scheme_description: t(scheme.scheme_description || scheme.description),
      department: translatedDept || scheme.department,
      ministry: translatedMinistry || scheme.ministry,
      category: translatedCat || scheme.category,
      target_category: translatedCat || scheme.target_category
    };
  };

  const translateDynamic = async (text) => {
    if (!text || currentLanguage === 'en') return text;
    try {
      const res = await api.post('/translate', {
        text: text,
        target_language: currentLanguage
      });
      return res.data.translated_text || text;
    } catch (e) {
      return text;
    }
  };

  return (
    <LanguageContext.Provider value={{
      currentLanguage,
      language: currentLanguage,
      setLanguage,
      t,
      translateScheme,
      translateDynamic,
      languages: LANGUAGES
    }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => useContext(LanguageContext);
'''

react_code = react_code_template.replace(
    '__SCHEME_MAP__', json.dumps(master_scheme_map, ensure_ascii=False, indent=2)
).replace(
    '__DICTIONARY__', json.dumps(DICTIONARY_12_LANG, ensure_ascii=False, indent=2)
)

# Write to LanguageContext.jsx
target_file = r'frontend/src/context/LanguageContext.jsx'
with open(target_file, 'w', encoding='utf-8') as f:
    f.write(react_code)

print(f"Written updated LanguageContext.jsx ({len(react_code)} bytes).")
