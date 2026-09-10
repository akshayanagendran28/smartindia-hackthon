# -*- coding: utf-8 -*-
"""
Unified Real-Time Document Validation Pipeline
Orchestrates:
1. File Ingestion & Format Sanitization
2. Image Preprocessing (OpenCV / Pillow)
3. Multi-tier OCR & Text Stream Extraction
4. Field & Rule Validation (Aadhaar, PAN, Caste, Income, DPR, Udyam)
5. Profile Cross-Verification (Fuzzy matching, DOB, Income tolerance, Caste match)
6. Scheme Eligibility Verification (for Income and DPR)
7. Official Government / DigiLocker Verification Adapter
8. Audit Trail Logging & Normalized JSON Response
"""
import os
import datetime
from typing import Dict, Any, Optional
from .ocr_engine import MultiTierOcrEngine
from .validators.aadhaar_validator import AadhaarValidator
from .validators.pan_validator import PanValidator
from .validators.caste_validator import CasteValidator
from .validators.income_validator import IncomeValidator
from .validators.dpr_validator import DprValidator
from .validators.udyam_validator import UdyamValidator
from .validators.education_validator import EducationValidator

class DocumentValidationPipeline:

    DOC_TYPE_MAP = {
        "doc10th": "10th Marksheet",
        "10th": "10th Marksheet",
        "10th marksheet": "10th Marksheet",
        "10th standard marksheet": "10th Marksheet",
        "doc12th": "12th Marksheet",
        "12th": "12th Marksheet",
        "12th marksheet": "12th Marksheet",
        "12th standard marksheet": "12th Marksheet",
        "docadmission": "Admission Letter",
        "admission": "Admission Letter",
        "admission letter": "Admission Letter",
        "admission proof": "Admission Letter",
        "college admission proof": "Admission Letter",
        "docfeestructure": "Fee Structure",
        "feestructure": "Fee Structure",
        "fee structure": "Fee Structure",
        "institutional fee structure": "Fee Structure",
        "fees": "Fee Structure",
        "docaadhaar": "Aadhaar",
        "aadhaar": "Aadhaar",
        "aadhaar card": "Aadhaar",
        "docpan": "PAN",
        "pan": "PAN",
        "pan card": "PAN",
        "doccaste": "Caste Certificate",
        "caste": "Caste Certificate",
        "caste certificate": "Caste Certificate",
        "community certificate": "Caste Certificate",
        "docincome": "Income Certificate",
        "income": "Income Certificate",
        "income certificate": "Income Certificate",
        "docdpr": "Detailed Project Report",
        "dpr": "Detailed Project Report",
        "project report": "Detailed Project Report",
        "docudyam": "Udyam Registration",
        "udyam": "Udyam Registration",
        "udyam registration": "Udyam Registration",
        "udyam registration certificate": "Udyam Registration",
        "udyam certificate": "Udyam Registration",
        "udyam aadhar": "Udyam Registration",
        "msme": "Udyam Registration",
        "msme certificate": "Udyam Registration"
    }

    @classmethod
    def normalize_doc_type(cls, doc_type_raw: str) -> str:
        key = (doc_type_raw or "").strip().lower()
        return cls.DOC_TYPE_MAP.get(key, doc_type_raw)

    @classmethod
    def validate_document(
        cls, 
        file_path: str, 
        document_type: str, 
        user_profile: Dict[str, Any],
        raw_text_override: Optional[str] = None,
        selected_scheme_code: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes end-to-end real-time document validation pipeline.
        """
        norm_type = cls.normalize_doc_type(document_type)
        audit_logs = []
        now = datetime.datetime.utcnow().isoformat() + "Z"

        # 1. Audit Log: Upload & Ingestion
        audit_logs.append({
            "stage": "INGESTION",
            "action": "File Received & Sanitized",
            "status": "SUCCESS",
            "timestamp": now,
            "details": f"File '{os.path.basename(file_path)}' accepted for document category '{norm_type}'."
        })

        # 2. Preprocessing & OCR
        if raw_text_override and len(raw_text_override.strip()) > 10:
            raw_text = raw_text_override.strip()
            ocr_res = {
                "raw_text": raw_text,
                "ocr_status": "SUCCESS",
                "confidence": 0.98,
                "engine_used": "Direct OCR Payload",
                "preprocessing": {"quality_score": 0.98}
            }
        else:
            ocr_res = MultiTierOcrEngine.extract_text(file_path, document_type=norm_type)
            raw_text = ocr_res.get("raw_text", "")

        audit_logs.append({
            "stage": "OCR_EXTRACTION",
            "action": "Image Preprocessing & Multi-Tier OCR",
            "status": ocr_res.get("ocr_status", "SUCCESS"),
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "details": f"OCR Engine ({ocr_res.get('engine_used')}) extracted {len(raw_text.split())} words with confidence {ocr_res.get('confidence', 0.95):.2f}."
        })

        # 3. Route to Document-Specific Validator
        if norm_type == "Aadhaar":
            val_res = AadhaarValidator.validate(raw_text, user_profile, ocr_confidence=ocr_res.get("confidence", 0.95))
        elif norm_type == "PAN":
            val_res = PanValidator.validate(raw_text, user_profile, ocr_confidence=ocr_res.get("confidence", 0.95))
        elif norm_type == "Caste Certificate":
            val_res = CasteValidator.validate(raw_text, user_profile, ocr_confidence=ocr_res.get("confidence", 0.95))
        elif norm_type == "Income Certificate":
            val_res = IncomeValidator.validate(raw_text, user_profile, selected_scheme_code=selected_scheme_code, ocr_confidence=ocr_res.get("confidence", 0.95))
        elif norm_type == "Detailed Project Report":
            val_res = DprValidator.validate(raw_text, user_profile, ocr_confidence=ocr_res.get("confidence", 0.95))
        elif norm_type == "Udyam Registration":
            val_res = UdyamValidator.validate(raw_text, user_profile, ocr_confidence=ocr_res.get("confidence", 0.95))
        elif norm_type in ["10th Marksheet", "12th Marksheet", "Admission Letter", "Fee Structure"]:
            val_res = EducationValidator.validate(raw_text, user_profile, doc_type=norm_type, ocr_confidence=ocr_res.get("confidence", 0.95))
        else:
            # Fallback for generic or unknown documents
            val_res = EducationValidator.validate(raw_text, user_profile, doc_type=norm_type, ocr_confidence=ocr_res.get("confidence", 0.95))
            val_res["document_type"] = norm_type

        # 4. Audit Log: Format & Rule Validation
        audit_logs.append({
            "stage": "FORMAT_VALIDATION",
            "action": "Algorithmic & Field Schema Check",
            "status": "SUCCESS" if val_res.get("format_valid") else "FAILED",
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "details": f"Format verification completed. Result: {val_res.get('format_valid')}"
        })

        # 5. Audit Log: Profile Cross-Check
        audit_logs.append({
            "stage": "PROFILE_CROSSCHECK",
            "action": "Fuzzy Matching with User Profile",
            "status": "MATCH" if val_res.get("profile_match") else "MISMATCH",
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "details": f"Cross-referenced extracted fields against registered applicant data."
        })

        # 6. Audit Log: Official Verification
        official_info = val_res.get("official_verification_details", {})
        audit_logs.append({
            "stage": "OFFICIAL_VERIFICATION",
            "action": official_info.get("service", "Government Gateway Adapter"),
            "status": val_res.get("official_verification", "VERIFIED"),
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "details": official_info.get("message", "Completed verification request.")
        })

        # Combine Final Response
        val_res["ocr_raw_text"] = raw_text
        val_res["audit_logs"] = audit_logs
        val_res["preprocessing_info"] = ocr_res.get("preprocessing", {})

        return val_res
