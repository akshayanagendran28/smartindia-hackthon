from fastapi import APIRouter, Query
from typing import Optional, List, Dict, Any

router = APIRouter(prefix="/questions", tags=["Dynamic Questions"])

PURPOSE_OPTIONS = [
    {
        "id": "EDUCATION",
        "title": "Education & Student Loans",
        "subtitle": "Interest subsidies (CSIS), collateral-free higher education loans (CGFSEL), and concessional credit (NSFDC/NBCFDC/NMDFC)",
        "badge": "Central & State Education Schemes",
        "icon": "AcademicCapIcon"
    },
    {
        "id": "BUSINESS",
        "title": "Business & Enterprise Setup / Expansion",
        "subtitle": "PMEGP up to 35% subsidy, Stand-Up India up to ₹1 Cr, State CMEGP/NEEDS capital grants",
        "badge": "Credit-Linked Subsidies",
        "icon": "BuildingStorefrontIcon"
    },
    {
        "id": "SELF_EMPLOYMENT",
        "title": "Self-Employment, Artisans & Vendors",
        "subtitle": "PM SVANidhi 7% interest subsidy, PM Vishwakarma toolkit & ₹3L loans, Mudra Shishu zero-collateral micro-credit",
        "badge": "Micro-Credit & Toolkits",
        "icon": "WrenchScrewdriverIcon"
    }
]

QUESTIONNAIRES = {
    "EDUCATION": [
        {
            "id": "age",
            "label": "Applicant Age (Years)",
            "type": "number",
            "min": 16,
            "max": 60,
            "default": 20,
            "required": True,
            "help_text": "Age of the student applying for the education scheme (typically 17-35 years)."
        },
        {
            "id": "gender",
            "label": "Gender",
            "type": "select",
            "options": [
                {"value": "female", "label": "Female (Eligible for special girl student interest concessions)"},
                {"value": "male", "label": "Male"},
                {"value": "other", "label": "Other / Transgender"}
            ],
            "default": "female",
            "required": True
        },
        {
            "id": "category",
            "label": "Social Category",
            "type": "select",
            "options": [
                {"value": "General", "label": "General (Eligible for CSIS & CGFSEL)"},
                {"value": "EWS", "label": "Economically Weaker Section (EWS - CSIS / Ambedkar)"},
                {"value": "OBC", "label": "Other Backward Class (OBC / Non-Creamy Layer - NBCFDC / Ambedkar)"},
                {"value": "SC", "label": "Scheduled Caste (SC - NSFDC Concessional Rate 3.5%-4%)"},
                {"value": "ST", "label": "Scheduled Tribe (ST - Concessional Education Rate)"},
                {"value": "Minority", "label": "Minority (Muslim, Christian, Sikh, Buddhist, Jain, Parsi - NMDFC 3%)"}
            ],
            "default": "General",
            "required": True
        },
        {
            "id": "annual_family_income",
            "label": "Annual Family Income (₹)",
            "type": "number",
            "min": 0,
            "max": 5000000,
            "default": 250000,
            "required": True,
            "help_text": "Total gross annual income of parents/family. CSIS subsidy requires ≤ ₹4.5 Lakh; NBCFDC/NSFDC requires ≤ ₹3 Lakh."
        },
        {
            "id": "current_education_level",
            "label": "Highest Completed Qualification",
            "type": "select",
            "options": [
                {"value": "12th Pass", "label": "12th Standard / Higher Secondary (Pass)"},
                {"value": "10th Pass", "label": "10th Standard / Matriculation"},
                {"value": "Diploma", "label": "Polytechnic / Diploma"},
                {"value": "Undergraduate", "label": "Undergraduate Degree (Graduated)"},
                {"value": "Postgraduate", "label": "Postgraduate Degree"}
            ],
            "default": "12th Pass",
            "required": True
        },
        {
            "id": "course_type",
            "label": "Course / Degree Admitted or Applying For",
            "type": "select",
            "options": [
                {"value": "Technical / Engineering (B.Tech / B.E / M.Tech)", "label": "Technical / Engineering (B.Tech / B.E / M.Tech)"},
                {"value": "Medical / Dental / Nursing / Pharma (MBBS / BDS / B.Pharm)", "label": "Medical / Dental / Nursing / Pharma (MBBS / BDS / B.Pharm)"},
                {"value": "Management / Business (MBA / PGDM)", "label": "Management / Business (MBA / PGDM)"},
                {"value": "Professional / Law / CA / ICWA / CS", "label": "Professional / Law / CA / ICWA / CS"},
                {"value": "Overseas Masters / Ph.D.", "label": "Overseas Higher Education (Masters / Ph.D. abroad)"},
                {"value": "Degree in Sciences / Commerce / Arts", "label": "Degree in Sciences / Commerce / Arts (B.Sc / B.Com / B.A)"},
                {"value": "Polytechnic / Recognized Diploma", "label": "Polytechnic / Recognized Technical Diploma"}
            ],
            "default": "Technical / Engineering (B.Tech / B.E / M.Tech)",
            "required": True
        },
        {
            "id": "institution_type",
            "label": "Institution Type",
            "type": "select",
            "options": [
                {"value": "Premier Govt (IIT/IIM/NIT/AIIMS/Central Univ)", "label": "Premier Govt Institute (IIT / IIM / NIT / AIIMS / Central Univ)"},
                {"value": "NAAC / AICTE / UGC Approved Govt/Aided College", "label": "NAAC / AICTE / UGC Approved Govt / Aided College"},
                {"value": "Private Recognized University / College", "label": "Private Recognized University / College"},
                {"value": "Overseas / International University", "label": "Overseas / International University"}
            ],
            "default": "NAAC / AICTE / UGC Approved Govt/Aided College",
            "required": True
        },
        {
            "id": "admission_status",
            "label": "Admission Status",
            "type": "select",
            "options": [
                {"value": "Confirmed Admission (Offer / Allotment Letter in Hand)", "label": "Confirmed Admission (Offer / Allotment Letter in Hand)"},
                {"value": "Entrance Exam Cleared / Counseling Pending", "label": "Entrance Exam Cleared / Counseling Pending"},
                {"value": "Currently Enrolled (Pursuing 2nd/3rd/4th Year)", "label": "Currently Enrolled (Pursuing 2nd/3rd/4th Year)"}
            ],
            "default": "Confirmed Admission (Offer / Allotment Letter in Hand)",
            "required": True
        },
        {
            "id": "annual_course_fee",
            "label": "Annual Tuition & Institutional Fees (₹)",
            "type": "number",
            "min": 10000,
            "max": 3000000,
            "default": 120000,
            "required": True,
            "help_text": "Annual fee charged by the college/university as per official fee breakdown."
        },
        {
            "id": "course_duration_years",
            "label": "Course Duration (Years)",
            "type": "select",
            "options": [
                {"value": 1, "label": "1 Year (Postgraduate / Diploma)"},
                {"value": 2, "label": "2 Years (Masters / MBA / M.Tech)"},
                {"value": 3, "label": "3 Years (General Degree / BCA / BBA / B.Sc)"},
                {"value": 4, "label": "4 Years (B.Tech / B.E / B.Pharm)"},
                {"value": 5, "label": "5 Years (MBBS / Integrated Dual Degree / LLB)"}
            ],
            "default": 4,
            "required": True
        },
        {
            "id": "required_loan_amount",
            "label": "Total Required Education Loan Amount (₹)",
            "type": "number",
            "min": 25000,
            "max": 4000000,
            "default": 450000,
            "required": True,
            "help_text": "Calculated total financial assistance required for tuition, hostel, books, and equipment. CGFSEL covers up to ₹7.5L collateral-free."
        },
        {
            "id": "location_state",
            "label": "Permanent Resident State",
            "type": "state_select",
            "default": "Maharashtra",
            "required": True
        },
        {
            "id": "location_district",
            "label": "Permanent Resident District",
            "type": "district_select",
            "depends_on": "location_state",
            "default": "Mumbai",
            "required": True
        }
    ],

    "BUSINESS": [
        {
            "id": "age",
            "label": "Applicant Age (Years)",
            "type": "number",
            "min": 18,
            "max": 75,
            "default": 29,
            "required": True,
            "help_text": "Minimum age is 18 years for PMEGP, Stand-Up India, and State MSME schemes."
        },
        {
            "id": "gender",
            "label": "Gender",
            "type": "select",
            "options": [
                {"value": "female", "label": "Female (Special Priority & Higher Subsidy up to 35%)"},
                {"value": "male", "label": "Male"},
                {"value": "other", "label": "Other / Transgender"}
            ],
            "default": "female",
            "required": True
        },
        {
            "id": "category",
            "label": "Social Category",
            "type": "select",
            "options": [
                {"value": "General", "label": "General (15%-25% PMEGP Subsidy)"},
                {"value": "OBC", "label": "Other Backward Class (OBC - Up to 35% Subsidy)"},
                {"value": "SC", "label": "Scheduled Caste (SC - Stand-Up India / NSSH / 35% PMEGP)"},
                {"value": "ST", "label": "Scheduled Tribe (ST - Stand-Up India / NSSH / 35% PMEGP)"},
                {"value": "Minority", "label": "Minority (NMDFC / 35% PMEGP Special Category)"},
                {"value": "Divyangjan", "label": "Person with Disability (Divyangjan - Special Category)"}
            ],
            "default": "General",
            "required": True
        },
        {
            "id": "annual_family_income",
            "label": "Annual Household Income (₹)",
            "type": "number",
            "min": 0,
            "max": 10000000,
            "default": 350000,
            "required": True,
            "help_text": "PMEGP & Stand-Up India have NO income cap; State schemes may prioritize specific income bands."
        },
        {
            "id": "education_qualification",
            "label": "Highest Education Qualification",
            "type": "select",
            "options": [
                {"value": "below_8th", "label": "Below 8th Standard"},
                {"value": "8th", "label": "8th Pass (Eligible for PMEGP Manufacturing up to ₹10L / Service ₹5L)"},
                {"value": "10th", "label": "10th Pass (High School Pass)"},
                {"value": "12th", "label": "12th Pass / Intermediate / ITI"},
                {"value": "graduate", "label": "Graduate / Post-Graduate / Professional Degree (NEEDS/MMYSY eligible)"}
            ],
            "default": "10th",
            "required": True
        },
        {
            "id": "business_stage",
            "label": "Enterprise Status",
            "type": "select",
            "options": [
                {"value": "New Greenfield Enterprise", "label": "New Greenfield Enterprise (Proposed / First Time Setup)"},
                {"value": "Existing Enterprise Expansion", "label": "Existing Enterprise Expansion (Modernization / Scaling)"}
            ],
            "default": "New Greenfield Enterprise",
            "required": True
        },
        {
            "id": "business_type",
            "label": "Industry / Enterprise Sector",
            "type": "select",
            "options": [
                {"value": "manufacturing", "label": "Manufacturing Unit (Machinery, Production, Food Processing - Up to ₹50 Lakh)"},
                {"value": "service", "label": "Service Enterprise (Repair, IT, Logistics, Healthcare, Hospitality - Up to ₹20 Lakh)"},
                {"value": "trading", "label": "Trading / Wholesale / Retail (Stand-Up India / State Schemes)"},
                {"value": "artisan", "label": "Handicrafts / Handlooms / Agro-Processing"}
            ],
            "default": "manufacturing",
            "required": True
        },
        {
            "id": "has_udyam_registration",
            "label": "Do you hold MSME Udyam Registration?",
            "type": "boolean",
            "default": False,
            "help_text": "Required for existing business credit lines and National SC-ST Hub support."
        },
        {
            "id": "has_gst",
            "label": "Do you have GST Registration?",
            "type": "boolean",
            "default": False
        },
        {
            "id": "gstin",
            "label": "GSTIN (GST Identification Number)",
            "type": "text",
            "depends_on": "has_gst",
            "dependency_value": True,
            "help_text": "15-digit GSTIN for verification."
        },
        {
            "id": "existing_turnover",
            "label": "Annual Business Turnover (₹)",
            "type": "number",
            "depends_on": "business_stage",
            "dependency_value": "Existing Enterprise Expansion",
            "default": 0,
            "help_text": "Last financial year turnover for existing units."
        },
        {
            "id": "project_cost",
            "label": "Total Estimated Project Cost (₹)",
            "type": "number",
            "min": 50000,
            "max": 50000000,
            "default": 1500000,
            "required": True,
            "help_text": "Includes plant, machinery, civil works, and initial working capital."
        },
        {
            "id": "required_loan_amount",
            "label": "Bank Loan Quantum Required (₹)",
            "type": "number",
            "min": 50000,
            "max": 50000000,
            "default": 1200000,
            "required": True,
            "help_text": "Total loan sought after deducting your own margin money contribution."
        },
        {
            "id": "own_contribution",
            "label": "Beneficiary Own Contribution (Margin Money) (₹)",
            "type": "number",
            "min": 0,
            "max": 10000000,
            "default": 150000,
            "required": True,
            "help_text": "5% for Special Categories (SC/ST/OBC/Women/Minority); 10% for General."
        },
        {
            "id": "has_skill_training",
            "label": "Have you completed EDP / Entrepreneurship Skill Training?",
            "type": "boolean",
            "default": False,
            "help_text": "Mandatory before 2nd installment under PMEGP and NEEDS schemes."
        },
        {
            "id": "location_state",
            "label": "Project / Unit State",
            "type": "state_select",
            "default": "Maharashtra",
            "required": True
        },
        {
            "id": "location_district",
            "label": "Project / Unit District",
            "type": "district_select",
            "depends_on": "location_state",
            "default": "Mumbai",
            "required": True
        },
        {
            "id": "area_type",
            "label": "Project Location Classification",
            "type": "select",
            "options": [
                {"value": "rural", "label": "Rural Area (Higher PMEGP Subsidy: 25% General / 35% Special)"},
                {"value": "urban", "label": "Urban Area (PMEGP Subsidy: 15% General / 25% Special)"}
            ],
            "default": "rural",
            "required": True
        }
    ],

    "SELF_EMPLOYMENT": [
        {
            "id": "age",
            "label": "Applicant Age (Years)",
            "type": "number",
            "min": 18,
            "max": 70,
            "default": 32,
            "required": True
        },
        {
            "id": "gender",
            "label": "Gender",
            "type": "select",
            "options": [
                {"value": "female", "label": "Female (Special access to Mahila Samridhi & Udyogini)"},
                {"value": "male", "label": "Male"},
                {"value": "other", "label": "Other"}
            ],
            "default": "female",
            "required": True
        },
        {
            "id": "category",
            "label": "Social Category",
            "type": "select",
            "options": [
                {"value": "General", "label": "General"},
                {"value": "OBC", "label": "Other Backward Class (OBC - Mahila Samridhi / NBCFDC 4%)"},
                {"value": "SC", "label": "Scheduled Caste (SC - Udyogini 50% subsidy / Vishwakarma)"},
                {"value": "ST", "label": "Scheduled Tribe (ST - Udyogini 50% subsidy / Vishwakarma)"},
                {"value": "Minority", "label": "Minority (NMDFC Micro Loan)"},
                {"value": "Divyangjan", "label": "Person with Disability (Divyangjan)"}
            ],
            "default": "OBC",
            "required": True
        },
        {
            "id": "annual_family_income",
            "label": "Annual Household Income (₹)",
            "type": "number",
            "min": 0,
            "max": 2000000,
            "default": 120000,
            "required": True,
            "help_text": "Mahila Samridhi requires ≤ ₹3.0 Lakh/year; PM SVANidhi has no ceiling for certified vendors."
        },
        {
            "id": "business_type",
            "label": "Self-Employment Trade / Activity",
            "type": "select",
            "options": [
                {"value": "street_vendor", "label": "Street Vendor / Hawker / Cart Operator (PM SVANidhi 7% Subvention)"},
                {"value": "artisan", "label": "Traditional Artisan / Craftsman (PM Vishwakarma Toolkit + 5% Loan)"},
                {"value": "service", "label": "Repair Shop / Tailoring / Beauty / Local Services (Mudra Shishu / Karma Sathi)"},
                {"value": "trading", "label": "Micro Retail / Small Kirana / Vegetable Vending"},
                {"value": "manufacturing", "label": "Cottage Production / Papad / Pickles / Handicrafts"}
            ],
            "default": "street_vendor",
            "required": True
        },
        {
            "id": "is_street_vendor",
            "label": "Are you an Urban / Rural Street Vendor with ULB Survey or LoR?",
            "type": "boolean",
            "default": True,
            "help_text": "Enables PM SVANidhi 1st tranche (₹10,000) with 7% interest subsidy and cashback."
        },
        {
            "id": "is_artisan",
            "label": "Are you registered or working in one of 18 traditional Vishwakarma trades?",
            "type": "boolean",
            "default": False,
            "help_text": "Enables PM Vishwakarma ₹15,000 modern toolkit grant and ₹3 Lakh 5% credit."
        },
        {
            "id": "required_loan_amount",
            "label": "Micro Credit / Working Capital Required (₹)",
            "type": "number",
            "min": 5000,
            "max": 300000,
            "default": 20000,
            "required": True,
            "help_text": "₹10,000-₹50,000 for SVANidhi / Mudra Shishu; up to ₹3,00,000 for PM Vishwakarma / Karma Sathi."
        },
        {
            "id": "location_state",
            "label": "Resident State",
            "type": "state_select",
            "default": "Maharashtra",
            "required": True
        },
        {
            "id": "location_district",
            "label": "Resident District",
            "type": "district_select",
            "depends_on": "location_state",
            "default": "Mumbai",
            "required": True
        },
        {
            "id": "area_type",
            "label": "Area Type",
            "type": "select",
            "options": [
                {"value": "urban", "label": "Urban Local Body (Municipal / Town Area)"},
                {"value": "rural", "label": "Gram Panchayat / Rural Area"}
            ],
            "default": "urban",
            "required": True
        }
    ]
}

@router.get("/purposes")
def get_purpose_options() -> List[Dict[str, Any]]:
    """Return verified purpose categories with scheme coverage."""
    return PURPOSE_OPTIONS

@router.get("")
def get_dynamic_questions(
    purpose_type: Optional[str] = Query("BUSINESS", description="User track: EDUCATION, BUSINESS, or SELF_EMPLOYMENT")
) -> Dict[str, Any]:
    """
    Return dynamic, purpose-specific questions.
    Filters out all irrelevant questions (e.g., GSTIN/DPR/Turnover for Education, Academic details for Business).
    """
    p_type = purpose_type.upper() if purpose_type else "BUSINESS"
    if p_type not in QUESTIONNAIRES:
        p_type = "BUSINESS"
        
    return {
        "purpose_type": p_type,
        "questions": QUESTIONNAIRES[p_type],
        "total_questions": len(QUESTIONNAIRES[p_type]),
        "purpose_info": next((p for p in PURPOSE_OPTIONS if p["id"] == p_type), None)
    }
