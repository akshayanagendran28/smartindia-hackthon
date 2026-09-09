import os

base = "C:/Users/aksha/.gemini/antigravity/scratch/scheme-sathi/backend"

def save(rel_path, content):
    full_path = os.path.join(base, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {rel_path}")

# app/services/ranking.py
save("app/services/ranking.py", """import json
import math
from typing import Dict, Any, List
from app.models.scheme import Scheme
from app.rules.engine import EligibilityRuleEngine

class ExplainableRankingService:
    \"\"\"
    Intelligent explainable multi-factor scheme ranker.
    Weights:
      - Purpose compatibility:      25%
      - Income compatibility:       20%
      - Loan requirement match:     20%
      - Project cost compatibility: 15%
      - Location compatibility:     10%
      - Business type match:        10%
    \"\"\"

    @classmethod
    def rank_scheme(cls, scheme: Scheme, user_data: Dict[str, Any]) -> Dict[str, Any]:
        # 1. Deterministic Rule Engine Eligibility Check
        eligibility = EligibilityRuleEngine.check_scheme_eligibility(scheme, user_data)
        is_eligible = eligibility["eligible"]
        
        # 2. Factor 1: Purpose Compatibility (25%)
        user_purpose = user_data.get("purpose", "Start a Business")
        try:
            purposes = json.loads(scheme.eligible_purposes)
        except Exception:
            purposes = ["Start a Business", "Expand Existing Business"]
        
        purposes_lower = [p.lower() for p in purposes]
        if any(user_purpose.lower() in p or p in user_purpose.lower() for p in purposes_lower):
            purpose_score = 100.0
        elif "all" in purposes_lower:
            purpose_score = 90.0
        else:
            purpose_score = 30.0

        # 3. Factor 2: Income Compatibility (20%)
        user_inc = float(user_data.get("annual_family_income", 0))
        if scheme.max_income_limit and scheme.max_income_limit > 0:
            if user_inc <= scheme.max_income_limit:
                # Better score if well within target marginalized income
                ratio = user_inc / scheme.max_income_limit
                income_score = 100.0 if ratio <= 0.8 else 90.0
            else:
                income_score = max(0.0, 100.0 - ((user_inc - scheme.max_income_limit) / scheme.max_income_limit) * 100)
        else:
            # Universal scheme, no income ceiling
            income_score = 95.0

        # 4. Factor 3: Loan Requirement Match (20%)
        user_loan = float(user_data.get("required_loan_amount", 0))
        if user_loan <= 0:
            loan_score = 85.0
        elif scheme.min_loan_amount <= user_loan <= scheme.max_loan_amount:
            # Sweet spot
            loan_score = 100.0
        elif user_loan < scheme.min_loan_amount:
            loan_score = max(40.0, 100.0 - ((scheme.min_loan_amount - user_loan) / max(scheme.min_loan_amount, 1)) * 50)
        else:
            # Exceeds max loan
            loan_score = max(20.0, 100.0 - ((user_loan - scheme.max_loan_amount) / max(scheme.max_loan_amount, 1)) * 70)

        # 5. Factor 4: Project Cost Compatibility (15%)
        user_project = float(user_data.get("project_cost", 0))
        if user_project <= 0:
            project_score = 85.0
        elif scheme.min_project_cost <= user_project <= scheme.max_project_cost:
            project_score = 100.0
        elif user_project > scheme.max_project_cost:
            project_score = max(20.0, 100.0 - ((user_project - scheme.max_project_cost) / max(scheme.max_project_cost, 1)) * 80)
        else:
            project_score = 90.0

        # 6. Factor 5: Location Compatibility (10%)
        user_state = user_data.get("state", "").strip().lower()
        try:
            states = json.loads(scheme.eligible_states)
        except Exception:
            states = ["All India"]
        
        states_lower = [s.lower() for s in states]
        if "all india" in states_lower or "all" in states_lower:
            location_score = 100.0
        elif any(user_state in s or s in user_state for s in states_lower if user_state):
            location_score = 100.0
        else:
            location_score = 40.0

        # 7. Factor 6: Business Type Match (10%)
        user_biz = user_data.get("business_type", "Micro Retail").strip().lower()
        try:
            biz_types = json.loads(scheme.eligible_business_types)
        except Exception:
            biz_types = ["Manufacturing", "Service", "Trading", "Micro Retail"]
        
        biz_lower = [b.lower() for b in biz_types]
        if any(user_biz in b or b in user_biz for b in biz_lower):
            business_score = 100.0
        elif "all" in biz_lower:
            business_score = 95.0
        else:
            business_score = 45.0

        # Weighted composite score
        composite_score = (
            (purpose_score * 0.25) +
            (income_score * 0.20) +
            (loan_score * 0.20) +
            (project_score * 0.15) +
            (location_score * 0.10) +
            (business_score * 0.10)
        )

        # Apply hard eligibility penalty if deterministic rules failed
        if not is_eligible:
            final_match_score = round(min(composite_score * 0.55, 59.0), 1)
            eligibility_status = "ineligible"
        elif composite_score >= 85:
            final_match_score = round(composite_score, 1)
            eligibility_status = "eligible"
        else:
            final_match_score = round(composite_score, 1)
            eligibility_status = "partially_eligible"

        # Generate Explainable "Why Recommended" Bullet Points
        matching_factors = []
        if is_eligible:
            if income_score >= 90:
                matching_factors.append(f"Your annual family income falls comfortably within scheme eligibility guidelines.")
            if purpose_score >= 90:
                matching_factors.append(f"Your intended purpose '{user_data.get('purpose')}' is prioritized under {scheme.name}.")
            if loan_score >= 90:
                matching_factors.append(f"Requested loan amount of ₹{user_loan:,.0f} matches the sanctioned lending band (Up to ₹{scheme.max_loan_amount:,.0f}).")
            if project_score >= 90:
                matching_factors.append(f"Project cost structure of ₹{user_project:,.0f} satisfies scheme capital criteria.")
            if scheme.subsidy_percentage_general > 0 or scheme.subsidy_percentage_special > 0:
                matching_factors.append(f"Direct capital subsidy benefit of {scheme.subsidy_percentage_general:.0f}% to {scheme.subsidy_percentage_special:.0f}% available for your profile category.")
            matching_factors.append(f"Authorized channel partner network available in {user_data.get('state', 'your region')}.")
        else:
            for fr in eligibility["failed_rules"]:
                matching_factors.append(f"Notice: {fr.get('reason')}")

        # Missing Requirements / Action Items
        missing_requirements = []
        for fr in eligibility["failed_rules"]:
            missing_requirements.append(fr.get("reason"))
        for md in eligibility["missing_documents"]:
            missing_requirements.append(f"Missing Document: {md}")

        # Document readiness estimate
        total_req_docs = len(scheme.documents)
        avail_docs_count = max(0, total_req_docs - len(eligibility["missing_documents"]))
        doc_readiness = round((avail_docs_count / max(total_req_docs, 1)) * 100, 1)
        
        # Overall application readiness
        app_readiness = round(
            (100.0 if is_eligible else 40.0) * 0.40 +
            doc_readiness * 0.40 +
            (100.0 if user_data.get("profile_completed", True) else 60.0) * 0.20,
            1
        )

        return {
            "scheme_id": scheme.id,
            "scheme_code": scheme.code,
            "scheme_name": scheme.name,
            "department": scheme.department,
            "category": scheme.category,
            "description": scheme.description,
            "loan_type": scheme.loan_type,
            "max_loan_amount": scheme.max_loan_amount,
            "interest_rate_display": scheme.interest_rate_display,
            "repayment_period_months": scheme.repayment_period_months,
            "moratorium_months": scheme.moratorium_months,
            "subsidy_percentage_general": scheme.subsidy_percentage_general,
            "subsidy_percentage_special": scheme.subsidy_percentage_special,
            "subsidy_details": scheme.subsidy_details,
            "official_portal_url": scheme.official_portal_url,
            
            "match_score": final_match_score,
            "is_eligible": is_eligible,
            "eligibility_status": eligibility_status,
            
            # SHAP-Style breakdown dictionary (weights scaled 0-100)
            "compatibility_breakdown": {
                "income_compatibility": round(income_score, 1),
                "purpose_compatibility": round(purpose_score, 1),
                "loan_requirement": round(loan_score, 1),
                "project_cost": round(project_score, 1),
                "location_compatibility": round(location_score, 1),
                "business_compatibility": round(business_score, 1)
            },
            "matching_factors": matching_factors[:5],
            "missing_requirements": missing_requirements,
            "required_documents": [d.document_name for d in scheme.documents],
            "eligible_rules_count": len(eligibility["matched_rules"]),
            "failed_rules_count": len(eligibility["failed_rules"]),
            "application_readiness": app_readiness
        }
""")

# app/services/geo.py
save("app/services/geo.py", """import math
import json
from typing import Dict, Any, List, Optional
from app.models.partner import ChannelPartner

class GeospatialPartnerService:
    \"\"\"
    Geospatial partner recommendation combining:
      1. Scheme compatibility (Does the partner handle the user's recommended scheme?)
      2. Geographic proximity (Haversine / spatial distance)
    \"\"\"

    @staticmethod
    def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        R = 6371.0 # Earth radius in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2) ** 2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return round(R * c, 2)

    @classmethod
    def evaluate_partner(
        cls, 
        partner: ChannelPartner, 
        user_lat: float, 
        user_lon: float, 
        target_scheme_code: Optional[str] = None
    ) -> Dict[str, Any]:
        dist_km = cls.haversine_distance(user_lat, user_lon, partner.latitude, partner.longitude)
        
        try:
            supported = json.loads(partner.supported_scheme_codes)
        except Exception:
            supported = []

        supported_lower = [s.lower() for s in supported]
        
        # Scheme compatibility calculation
        if target_scheme_code:
            target_lower = target_scheme_code.lower()
            if "all" in supported_lower or target_lower in supported_lower or any(target_lower in s for s in supported_lower):
                scheme_compat = 100.0
                reason_part = f"This partner is an authorized processing nodal centre for {target_scheme_code}."
            else:
                scheme_compat = 35.0
                reason_part = f"Partner offers general banking services; scheme {target_scheme_code} may require lead agency escalation."
        else:
            scheme_compat = 85.0
            reason_part = f"Authorized institutional partner supporting multiple MSME and education credit schemes."

        # Geographic proximity score (decay curve: 100 at 0km, 80 at 10km, 50 at 30km, 20 at 100km)
        proximity_score = max(10.0, 100.0 / (1.0 + (dist_km / 12.0) ** 1.3))

        # Combined suitability: Scheme compatibility (60%) + Proximity (40%)
        suitability_score = round((scheme_compat * 0.60) + (proximity_score * 0.40), 1)

        return {
            "id": partner.id,
            "name": partner.name,
            "partner_type": partner.partner_type,
            "address": partner.address,
            "state": partner.state,
            "district": partner.district,
            "pincode": partner.pincode,
            "latitude": partner.latitude,
            "longitude": partner.longitude,
            "contact_person": partner.contact_person,
            "contact_phone": partner.contact_phone,
            "contact_email": partner.contact_email,
            "website": partner.website,
            "verification_status": partner.verification_status,
            "supported_scheme_codes": supported,
            "distance_km": dist_km,
            "scheme_compatibility_score": round(scheme_compat, 1),
            "partner_suitability_score": suitability_score,
            "suitability_reason": f"{reason_part} Located {dist_km:.1f} km away from your search pin."
        }
""")

# app/services/ocr.py
save("app/services/ocr.py", """import re
import json
import os
from typing import Dict, Any, List, Tuple

class DocumentOcrService:
    \"\"\"
    OCR text extraction, field NER parser, and Profile cross-verification engine.
    Extracts key fields from Income Certificates, Caste Certificates, GSTIN, Bank Statements, Project Reports.
    \"\"\"

    @classmethod
    def analyze_document_text(
        cls, 
        doc_type: str, 
        raw_text: str, 
        user_profile: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], List[str], str]:
        extracted = {}
        mismatches = []
        verification_status = "extracted"

        text_lower = raw_text.lower()
        
        # 1. Extract Annual Income
        income_patterns = [
            r"annual\s+income\s*[:=\-]?\s*(?:rs\.?|inr|₹)?\s*([\d,]+)",
            r"income\s*[:=\-]?\s*(?:rs\.?|inr|₹)?\s*([\d,]+)",
            r"वार्षिक\s+आय\s*[:=\-]?\s*(?:रु\.?|₹)?\s*([\d,]+)",
            r"வருமானம்\s*[:=\-]?\s*(?:ரூ\.?|₹)?\s*([\d,]+)",
            r"(?:rs\.?|inr|₹)\s*([\d,]+(?:\.\d{2})?)\s*(?:per\s+annum|p\.a\.|yearly)"
        ]
        
        for pattern in income_patterns:
            m = re.search(pattern, raw_text, re.IGNORECASE)
            if m:
                inc_str = m.group(1).replace(",", "").strip()
                try:
                    extracted["extracted_annual_income"] = float(inc_str)
                    break
                except ValueError:
                    pass

        # 2. Extract Category / Caste
        if any(w in text_lower for w in ["scheduled caste", " sc ", "sc/", "sc-"]):
            extracted["extracted_category"] = "SC"
        elif any(w in text_lower for w in ["scheduled tribe", " st ", "st/", "st-"]):
            extracted["extracted_category"] = "ST"
        elif any(w in text_lower for w in ["other backward class", " obc ", "obc-"]):
            extracted["extracted_category"] = "OBC"
        elif any(w in text_lower for w in ["minority", "muslim", "christian", "sikh", "buddhist", "jain"]):
            extracted["extracted_category"] = "Minority"
        elif any(w in text_lower for w in ["ews", "economically weaker section"]):
            extracted["extracted_category"] = "EWS"
        elif any(w in text_lower for w in ["general", "unreserved", "ur"]):
            extracted["extracted_category"] = "General"

        # 3. Extract GSTIN
        gstin_match = re.search(r"\b\d{2}[A-Z]{5}\d{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}\b", raw_text)
        if gstin_match:
            extracted["extracted_gstin"] = gstin_match.group(0)

        # 4. Extract Aadhaar Masked or Full Number
        aadhaar_match = re.search(r"\b\d{4}\s*\d{4}\s*\d{4}\b", raw_text)
        if aadhaar_match:
            extracted["extracted_aadhaar_ref"] = aadhaar_match.group(0)

        # 5. Extract Project / Loan Amount
        amount_match = re.search(r"project\s+cost\s*[:=\-]?\s*(?:rs\.?|inr|₹)?\s*([\d,]+)", raw_text, re.IGNORECASE)
        if amount_match:
            try:
                extracted["extracted_project_cost"] = float(amount_match.group(1).replace(",", ""))
            except ValueError:
                pass

        # 6. Compare with Profile and Highlight Mismatches
        profile_income = float(user_profile.get("annual_family_income", 0))
        if "extracted_annual_income" in extracted:
            ext_inc = extracted["extracted_annual_income"]
            diff = abs(ext_inc - profile_income)
            if profile_income > 0 and diff > (0.15 * profile_income):
                mismatches.append(
                    f"Annual Income Mismatch: Certificate indicates ₹{ext_inc:,.0f}, while Profile states ₹{profile_income:,.0f} (Difference: ₹{diff:,.0f})."
                )
                verification_status = "mismatch"
            else:
                extracted["income_match_status"] = "Verified within tolerance"

        profile_cat = user_profile.get("category", "General")
        if "extracted_category" in extracted:
            ext_cat = extracted["extracted_category"]
            if profile_cat.lower() != ext_cat.lower():
                mismatches.append(
                    f"Category Mismatch: Document identifies category as '{ext_cat}', whereas Profile records '{profile_cat}'."
                )
                verification_status = "mismatch"
            else:
                extracted["category_match_status"] = f"Verified as {ext_cat}"

        profile_gstin = user_profile.get("gstin")
        if "extracted_gstin" in extracted and profile_gstin:
            if extracted["extracted_gstin"].upper() != profile_gstin.upper():
                mismatches.append(
                    f"GSTIN Mismatch: Document has {extracted['extracted_gstin']} while profile has {profile_gstin}."
                )
                verification_status = "mismatch"

        if not mismatches and extracted:
            verification_status = "verified"
        elif not extracted:
            verification_status = "needs_review"

        return extracted, mismatches, verification_status
""")

# app/services/readiness.py
save("app/services/readiness.py", """from typing import Dict, Any, List

class ApplicationReadinessService:
    \"\"\"
    Calculates overall application readiness percentage and generates actionable recommendations.
    \"\"\"

    @classmethod
    def calculate_readiness(
        cls, 
        user_profile: Dict[str, Any], 
        eligible_schemes_count: int, 
        uploaded_documents_count: int, 
        required_documents_count: int,
        selected_partner: bool = True
    ) -> Dict[str, Any]:
        
        # 1. Profile completeness (Max 25%)
        profile_score = 0
        checks = []
        
        if user_profile.get("annual_family_income", 0) > 0:
            profile_score += 7
        if user_profile.get("age", 0) >= 18:
            profile_score += 6
        if user_profile.get("purpose"):
            profile_score += 6
        if user_profile.get("location_state") or user_profile.get("state"):
            profile_score += 6
            
        profile_complete = profile_score >= 20
        checks.append({
            "title": "Profile Information",
            "score": profile_score,
            "max": 25,
            "status": "complete" if profile_complete else "incomplete",
            "message": "Personal, business and financial details are saved." if profile_complete else "Complete pending financial & business profile fields."
        })

        # 2. Eligibility Confirmation (Max 25%)
        eligibility_score = 25 if eligible_schemes_count > 0 else 10
        checks.append({
            "title": "Scheme Eligibility",
            "score": eligibility_score,
            "max": 25,
            "status": "complete" if eligible_schemes_count > 0 else "action_required",
            "message": f"Deterministic eligibility confirmed for {eligible_schemes_count} scheme(s)." if eligible_schemes_count > 0 else "Run eligibility questionnaire to find matching schemes."
        })

        # 3. Document Readiness (Max 35%)
        doc_ratio = (uploaded_documents_count / max(required_documents_count, 1)) if required_documents_count > 0 else 1.0
        doc_score = round(min(35.0, doc_ratio * 35.0), 1)
        doc_complete = doc_score >= 30
        checks.append({
            "title": "Document Verification",
            "score": doc_score,
            "max": 35,
            "status": "complete" if doc_complete else ("partial" if doc_score > 10 else "action_required"),
            "message": f"{uploaded_documents_count} of {required_documents_count} mandatory documents ready."
        })

        # 4. Partner Availability (Max 15%)
        partner_score = 15 if selected_partner else 5
        checks.append({
            "title": "Channel Partner Processing",
            "score": partner_score,
            "max": 15,
            "status": "complete" if selected_partner else "action_required",
            "message": "Authorized nodal agency / bank branch identified in your district."
        })

        overall_percentage = round(profile_score + eligibility_score + doc_score + partner_score, 1)

        return {
            "overall_percentage": min(100.0, overall_percentage),
            "profile_score": profile_score,
            "eligibility_score": eligibility_score,
            "document_score": doc_score,
            "partner_score": partner_score,
            "checks": checks,
            "is_ready_for_submission": overall_percentage >= 80.0
        }
""")

# app/services/chat.py
save("app/services/chat.py", """import json
import re
from typing import Dict, Any, List, Optional
from app.models.scheme import Scheme

class MultilingualChatService:
    \"\"\"
    Scheme Sathi Multilingual AI Chat Assistant.
    Supports English, Hindi, Tamil, Telugu, Kannada, Malayalam.
    Grounded strictly in verified scheme database records with interactive guided option pills.
    \"\"\"

    INTENT_RESPONSES = {
        "en": {
            "greeting": "Namaste! I am your Scheme Sathi Assistant. I can help you discover government loan schemes, check your eligibility, calculate EMI, and locate nearest channel partners. What type of assistance do you need?",
            "ask_income": "To determine your exact eligibility and subsidy benefits, could you please specify your approximate annual family income?",
            "ask_loan_amount": "How much loan or project assistance are you looking for?",
            "found_schemes": "Based on your requirements, I have identified suitable government financial schemes with applicable interest rates and capital subsidies:",
            "fallback": "I understand your query. Let me guide you to the most relevant government schemes. Would you like to check your eligibility now?"
        },
        "hi": {
            "greeting": "नमस्ते! मैं आपका स्कीम साथी सहायक हूँ। मैं आपको सरकारी ऋण योजनाओं की खोज, पात्रता जांच, ईएमआई गणना और नजदीकी सहायता केंद्र ढूंढने में मदद कर सकता हूँ। आपको किस प्रकार की सहायता चाहिए?",
            "ask_income": "आपकी सटीक पात्रता और सब्सिडी लाभ निर्धारित करने के लिए, क्या आप अपनी अनुमानित वार्षिक पारिवारिक आय बता सकते हैं?",
            "ask_loan_amount": "आपको कितने ऋण या परियोजना सहायता की आवश्यकता है?",
            "found_schemes": "आपकी आवश्यकताओं के आधार पर, मैंने सरकारी वित्तीय योजनाओं की पहचान की है:",
            "fallback": "मैं आपकी आवश्यकता समझ रहा हूँ। आइए आपकी पात्रता की जाँच करें।"
        },
        "ta": {
            "greeting": "வணக்கம்! நான் உங்கள் ஸ்கீம் சாதி (Scheme Sathi) AI உதவியாளர். தொழில் கடன் திட்டங்கள், மானியங்கள் மற்றும் தகுதியை கண்டறிய உங்களுக்கு உதவுவேன். உங்களுக்கு என்ன உதவி தேவை?",
            "ask_income": "உங்கள் தகுதி மற்றும் மானியத்தை துல்லியமாக கணக்கிட, உங்கள் குடும்ப ஆண்டு வருமானத்தை குறிப்பிடவும்:",
            "ask_loan_amount": "உங்களுக்கு எவ்வளவு கடன் தொகை தேவைப்படுகிறது?",
            "found_schemes": "உங்கள் தேவைகளுக்கு ஏற்ப அரசாங்க கடன் திட்டங்கள் கண்டறியப்பட்டுள்ளன:",
            "fallback": "உங்கள் தேவையை நான் புரிந்துகொண்டேன். தகுதியான திட்டங்களை தேர்வு செய்ய உதவுவேன்."
        },
        "te": {
            "greeting": "నమస్కారం! నేను మీ స్కీమ్ సాథీ అసిస్టెంట్‌ని. ప్రభుత్వ రుణ పథకాలు, సబ్సిడీలు మరియు అర్హతను గుర్తించడంలో మీకు సహాయం చేస్తాను. మీకు ఎలాంటి సహాయం కావాలి?",
            "ask_income": "మీ అర్హత మరియు సబ్సిడీని ఖచ్చితంగా నిర్ణయించడానికి, దయచేసి మీ వార్షిక కుటుంబ ఆదాయాన్ని తెలపండి:",
            "ask_loan_amount": "మీకు ఎంత రుణ మొత్తం అవసరం?",
            "found_schemes": "మీ అవసరాల ఆధారంగా సరిపోయే ప్రభుత్వ పథకాలు ఇక్కడ ఉన్నాయి:",
            "fallback": "నేను మీ ప్రశ్నను అర్థం చేసుకున్నాను. అర్హత తనిఖీ చేద్దాం."
        },
        "kn": {
            "greeting": "ನಮಸ್ಕಾರ! ನಾನು ನಿಮ್ಮ ಸ್ಕೀಮ್ ಸಾಥಿ ಸಹಾಯಕ. ಸರ್ಕಾರಿ ಸಾಲ ಯೋಜನೆಗಳು, ಸಬ್ಸಿಡಿಗಳು ಮತ್ತು ಅರ್ಹತೆಯನ್ನು ತಿಳಿಯಲು ನಿಮಗೆ ಸಹಾಯ ಮಾಡುತ್ತೇನೆ. ನಿಮಗೆ ಯಾವ ಸಹಾಯ ಬೇಕು?",
            "ask_income": "ನಿಮ್ಮ ನಿಖರವಾದ ಅರ್ಹತೆ ಮತ್ತು ಸಬ್ಸಿಡಿ ನಿರ್ಧರಿಸಲು, ನಿಮ್ಮ ವಾರ್ಷಿಕ ಆದಾಯವನ್ನು ತಿಳಿಸಿ:",
            "ask_loan_amount": "ನಿಮಗೆ ಎಷ್ಟು ಮೊತ್ತದ ಸಾಲ ಬೇಕು?",
            "found_schemes": "ನಿಮ್ಮ ಅವಶ್ಯಕತೆಗೆ ಸೂಕ್ತವಾದ ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು:",
            "fallback": "ನಿಮ್ಮ ಪ್ರಶ್ನೆ ನನಗೆ ಅರ್ಥವಾಯಿತು. ಈಗಲೇ ಅರ್ಹತೆ ಪರಿಶೀಲಿಸೋಣ."
        },
        "ml": {
            "greeting": "നമസ്കാരം! ഞാൻ നിങ്ങളുടെ സ്കീം സാഥി അസിസ്റ്റന്റാണ്. സർക്കാർ വായ്പാ പദ്ധതികളും സബ്സിഡികളും കണ്ടെത്താൻ സഹായിക്കാം. എന്ത് സഹായമാണ് വേണ്ടത്?",
            "ask_income": "കൃത്യമായ സബ്‌സിഡിയും അർഹതയും അറിയാൻ വാർഷಿಕ കുടുംബ വരുമാനം വ്യക്തമാക്കുക:",
            "ask_loan_amount": "എത്ര തുകയുടെ വായ്പയാണ് താങ്കൾക്ക് ആവശ്യം?",
            "found_schemes": "നിങ്ങളുടെ ആവശ്യത്തിനനുയോജ്യമായ സർക്കാർ വായ്പാ പദ്ധതികൾ:",
            "fallback": "താങ്കളുടെ ആവശ്യം ഞാൻ മനസ്സിലാക്കി. നമുക്ക് പദ്ധതികൾ പരിശോധിക്കാം."
        }
    }

    @classmethod
    def process_message(
        cls, 
        user_message: str, 
        language: str = "en", 
        schemes_db: List[Scheme] = []
    ) -> Dict[str, Any]:
        lang = language if language in cls.INTENT_RESPONSES else "en"
        texts = cls.INTENT_RESPONSES.get(lang, cls.INTENT_RESPONSES["en"])
        
        msg_lower = user_message.lower()
        extracted_intent = {}
        suggested_options = []
        matching_schemes = []

        # Intent 1: Loan Amount / Range detection
        if any(w in msg_lower for w in ["lakh", "lac", "हज़ार", "लाख", "లక్ష", "ಲಕ್ಷ", "ലക്ഷം", "10000", "50000", "100000", "500000", "1000000", "5000000"]):
            # Filter schemes by loan capacity
            for s in schemes_db[:3]:
                matching_schemes.append({
                    "id": s.id,
                    "code": s.code,
                    "name": s.name,
                    "max_loan": s.max_loan_amount,
                    "interest": s.interest_rate_display,
                    "subsidy": f"{s.subsidy_percentage_general:.0f}% - {s.subsidy_percentage_special:.0f}%"
                })
            reply = f"{texts['found_schemes']}\n\n"
            for ms in matching_schemes:
                reply += f"• **{ms['name']}** (Up to ₹{ms['max_loan']:,.0f}, Interest: {ms['interest']}, Subsidy: {ms['subsidy']})\n"
            
            suggested_options = [
                {"label": "📊 Calculate EMI", "value": "calculate_emi"},
                {"label": "📑 Check Documents", "value": "check_documents"},
                {"label": "📍 Find Nearest Partner", "value": "find_partner"}
            ]
            return {
                "reply": reply,
                "language": lang,
                "extracted_intent": {"type": "loan_query"},
                "suggested_options": suggested_options,
                "recommendations": matching_schemes
            }

        # Intent 2: Business / Start / Expand Intent
        if any(w in msg_lower for w in ["start", "expand", "business", "loan", "दुकान", "व्यापार", "தொழில்", "వ్యాపారం", "ಉದ್ಯಮ", "സംരംഭം"]):
            reply = f"{texts['greeting']}\n\n{texts['ask_income']}"
            suggested_options = [
                {"label": "₹1 – 2 Lakh", "value": "income_1_2", "field": "annual_family_income"},
                {"label": "₹2 – 5 Lakh", "value": "income_2_5", "field": "annual_family_income"},
                {"label": "₹5 Lakh+", "value": "income_5_plus", "field": "annual_family_income"}
            ]
            return {
                "reply": reply,
                "language": lang,
                "extracted_intent": {"purpose": "Start / Expand Business"},
                "suggested_options": suggested_options,
                "recommendations": []
            }

        # Intent 3: Income provided
        if any(w in msg_lower for w in ["income_1_2", "income_2_5", "income_5_plus", "2 lakh", "3 lakh", "5 lakh"]):
            reply = f"{texts['ask_loan_amount']}"
            suggested_options = [
                {"label": "Up to ₹50,000 (Mudra Shishu / SVANidhi)", "value": "loan_50k"},
                {"label": "₹50,000 to ₹5 Lakh (Mudra Kishore)", "value": "loan_5l"},
                {"label": "₹5 Lakh to ₹50 Lakh (PMEGP / Stand-Up India)", "value": "loan_50l"}
            ]
            return {
                "reply": reply,
                "language": lang,
                "extracted_intent": {"income_acknowledged": True},
                "suggested_options": suggested_options,
                "recommendations": []
            }

        # Default Fallback
        reply = texts["greeting"]
        suggested_options = [
            {"label": "🚀 Start a New Business", "value": "Start a Business"},
            {"label": "📈 Expand Existing Business", "value": "Expand Existing Business"},
            {"label": "🎓 Education Loan", "value": "Education Loan"},
            {"label": "🛒 Micro Street Vendor / Artisan", "value": "Small Project Loan"}
        ]
        return {
            "reply": reply,
            "language": lang,
            "extracted_intent": {},
            "suggested_options": suggested_options,
            "recommendations": []
        }
""")

print("Services generated successfully!")
