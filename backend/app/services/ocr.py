import re
import json
import os
from typing import Dict, Any, List, Tuple

class DocumentOcrService:
    """
    OCR text extraction, field NER parser, and Profile cross-verification engine.
    Extracts key fields from Income Certificates, Caste Certificates, GSTIN, Bank Statements, Project Reports.
    """

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
        gstin_match = re.search(r"\d{2}[A-Z]{5}\d{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}", raw_text)
        if gstin_match:
            extracted["extracted_gstin"] = gstin_match.group(0)

        # 4. Extract Aadhaar Masked or Full Number
        aadhaar_match = re.search(r"\d{4}\s*\d{4}\s*\d{4}", raw_text)
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
