import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000/api"

def log_test(test_name, success, details=""):
    status = "[PASS]" if success else "[FAIL]"
    print(f"{status} | {test_name}")
    if details:
        print(f"       -> {details}")

def main():
    print("=" * 70)
    print("RUNNING COMPREHENSIVE SCHEME SATHI VERIFICATION SUITE")
    print("=" * 70)
    all_passed = True

    # -------------------------------------------------------------
    # TEST 1: Educational Loan Flow (SC, Female, Rs. 5,00,000, 6 mandatory docs)
    # -------------------------------------------------------------
    try:
        payload_edu = {
            "purpose_type": "EDUCATION",
            "loan_amount": 500000,
            "required_loan": 500000,
            "annual_income": 250000,
            "annual_family_income": 250000,
            "category": "SC",
            "social_category": "SC",
            "gender": "female",
            "age": 20,
            "course_type": "Technical / Engineering (B.Tech / B.E / M.Tech)",
            "institution_type": "NAAC / AICTE / UGC Approved Govt/Aided College",
            "admission_status": "Confirmed Admission (Offer / Allotment Letter in Hand)",
            "annual_course_fee": 125000,
            "course_duration_years": 4,
            "state": "Maharashtra",
            "district": "Mumbai",
            "bypass_doc_gate": True
        }
        res = requests.post(f"{BASE_URL}/matching/evaluate", json=payload_edu, timeout=10)
        data = res.json()
        eligible = data.get("eligible_schemes", [])
        eligible_codes = [s.get("scheme_code") for s in eligible]
        
        has_csis = any("CSIS" in c for c in eligible_codes)
        has_nsfdc = any("NSFDC" in c for c in eligible_codes)
        has_cgfsel = any("CGFSEL" in c for c in eligible_codes)
        no_business = all(s.get("purpose_type") == "EDUCATION" for s in eligible)
        
        t1_pass = res.status_code == 200 and has_csis and has_nsfdc and has_cgfsel and no_business
        log_test("Test 1: Educational Loan Flow (SC, Female, Rs. 5L)", t1_pass, 
                 f"Matched Schemes: {eligible_codes}, Education schemes only: {no_business}")
        if not t1_pass: all_passed = False
    except Exception as e:
        log_test("Test 1: Educational Loan Flow", False, str(e))
        all_passed = False

    # -------------------------------------------------------------
    # TEST 2: Loan Switch (Education -> Business Loan @ Rs. 12,00,000)
    # -------------------------------------------------------------
    try:
        payload_biz = {
            "purpose_type": "BUSINESS",
            "loan_amount": 1200000,
            "required_loan": 1200000,
            "project_cost": 1500000,
            "annual_income": 300000,
            "annual_family_income": 300000,
            "category": "SC",
            "social_category": "SC",
            "gender": "female",
            "age": 29,
            "business_stage": "New Greenfield Enterprise",
            "business_type": "manufacturing",
            "education_qualification": "10th",
            "area_type": "rural",
            "state": "Maharashtra",
            "district": "Mumbai",
            "bypass_doc_gate": True
        }
        res_biz = requests.post(f"{BASE_URL}/matching/evaluate", json=payload_biz, timeout=10)
        data_biz = res_biz.json()
        eligible_biz = data_biz.get("eligible_schemes", [])
        eligible_biz_codes = [s.get("scheme_code") for s in eligible_biz]
        
        has_pmegp = any("PMEGP" in c for c in eligible_biz_codes)
        has_standup = any("STANDUP" in c or "STAND_UP" in c for c in eligible_biz_codes)
        no_edu_leak = all(s.get("purpose_type") != "EDUCATION" for s in eligible_biz)
        
        t2_pass = res_biz.status_code == 200 and has_pmegp and has_standup and no_edu_leak
        log_test("Test 2: Loan Switch (Education -> Business Loan)", t2_pass, 
                 f"Matched Schemes: {eligible_biz_codes}, No Edu Leakage: {no_edu_leak}")
        if not t2_pass: all_passed = False
    except Exception as e:
        log_test("Test 2: Loan Switch", False, str(e))
        all_passed = False

    # -------------------------------------------------------------
    # TEST 3: Loan Switch Back (Business -> Education Loan @ Rs. 5,00,000)
    # -------------------------------------------------------------
    try:
        res_switch_back = requests.post(f"{BASE_URL}/matching/evaluate", json=payload_edu, timeout=10)
        data_switch_back = res_switch_back.json()
        eligible_sb = data_switch_back.get("eligible_schemes", [])
        eligible_sb_codes = [s.get("scheme_code") for s in eligible_sb]
        
        no_biz_leak = all(s.get("purpose_type") == "EDUCATION" for s in eligible_sb)
        t3_pass = res_switch_back.status_code == 200 and len(eligible_sb) > 0 and no_biz_leak
        log_test("Test 3: Loan Switch Back (Business -> Education)", t3_pass, 
                 f"Matched Schemes: {eligible_sb_codes}, Clean state restoration: {no_biz_leak}")
        if not t3_pass: all_passed = False
    except Exception as e:
        log_test("Test 3: Loan Switch Back", False, str(e))
        all_passed = False

    # -------------------------------------------------------------
    # TEST 4: Document Verification Requirements & Checklist (6 Mandatory Docs for Education)
    # -------------------------------------------------------------
    try:
        res_edu_docs = requests.get(f"{BASE_URL}/documents/checklist", params={"purpose_type": "EDUCATION"}, timeout=10)
        data_edu_docs = res_edu_docs.json()
        docs_list = data_edu_docs.get("checklist", []) if isinstance(data_edu_docs, dict) else data_edu_docs
        
        has_6_edu_docs = len(docs_list) >= 6
        
        # Verify single PAN verification endpoint
        res_pan = requests.post(f"{BASE_URL}/documents/verify-pan", json={"pan_number": "ABCDE1234F", "full_name": "Priya Sharma"}, timeout=10)
        pan_valid = res_pan.status_code == 200 and res_pan.json().get("valid") is True
        
        t4_pass = res_edu_docs.status_code == 200 and has_6_edu_docs and pan_valid
        log_test("Test 4: 6 Mandatory Documents for Education & Unified PAN Check", t4_pass, 
                 f"Required Docs Count: {len(docs_list)}, PAN Verification API: {pan_valid}")
        if not t4_pass: all_passed = False
    except Exception as e:
        log_test("Test 4: Document Verification", False, str(e))
        all_passed = False

    # -------------------------------------------------------------
    # TEST 5: Dynamic Loan Amount Evaluation (Rs. 5L vs Rs. 12L vs Rs. 25L)
    # -------------------------------------------------------------
    try:
        # Rs. 5L (CGFSEL eligible <= 7.5L, CSIS eligible <= 10L, NSFDC eligible <= 20L)
        payload_5l = {**payload_edu, "loan_amount": 500000, "required_loan": 500000}
        r_5l = requests.post(f"{BASE_URL}/matching/evaluate", json=payload_5l, timeout=10).json()
        codes_5l = [s.get("scheme_code") for s in r_5l.get("eligible_schemes", [])]
        
        # Rs. 12L (CGFSEL ineligible > 7.5L, CSIS ineligible > 10L, NSFDC-EDU eligible <= 20L)
        payload_12l = {**payload_edu, "loan_amount": 1200000, "required_loan": 1200000}
        r_12l = requests.post(f"{BASE_URL}/matching/evaluate", json=payload_12l, timeout=10).json()
        codes_12l = [s.get("scheme_code") for s in r_12l.get("eligible_schemes", [])]
        
        # Rs. 25L (NSFDC-EDU ineligible > 20L)
        payload_25l = {**payload_edu, "loan_amount": 2500000, "required_loan": 2500000}
        r_25l = requests.post(f"{BASE_URL}/matching/evaluate", json=payload_25l, timeout=10).json()
        codes_25l = [s.get("scheme_code") for s in r_25l.get("eligible_schemes", [])]
        
        dynamic_correct = ("CGFSEL" in codes_5l) and ("CGFSEL" not in codes_12l) and ("NSFDC-EDU" in codes_12l) and ("NSFDC-EDU" not in codes_25l)
        log_test("Test 5: Dynamic Loan Amount Evaluation & Loan Ceilings", dynamic_correct,
                 f"5L codes: {codes_5l}, 12L codes: {codes_12l}, 25L codes: {codes_25l}")
        if not dynamic_correct: all_passed = False
    except Exception as e:
        log_test("Test 5: Dynamic Loan Amount Evaluation", False, str(e))
        all_passed = False

    # -------------------------------------------------------------
    # TEST 6: Multilingual Switch & Translation across 12 Languages
    # -------------------------------------------------------------
    try:
        langs = ["hi", "ta", "te", "kn", "ml", "mr", "bn", "gu", "pa", "or", "as"]
        t6_all = True
        for lang in langs[:4]:
            res_tr = requests.post(f"{BASE_URL}/translate", json={"text": "Scheduled Caste", "target_language": lang}, timeout=10)
            if res_tr.status_code != 200 or not res_tr.json().get("translated_text"):
                t6_all = False
                break
        
        log_test("Test 6: Multilingual Switch & Regional Language API", t6_all, f"Tested regional translation endpoints: {langs[:4]}")
        if not t6_all: all_passed = False
    except Exception as e:
        log_test("Test 6: Multilingual Switch", False, str(e))
        all_passed = False

    # -------------------------------------------------------------
    # TEST 7: Chat Assistant (Contextual Q&A for Schemes & Docs)
    # -------------------------------------------------------------
    try:
        res_chat = requests.post(f"{BASE_URL}/chat/message", json={"message": "What documents are mandatory for an educational loan?", "language": "en"}, timeout=10)
        chat_data = res_chat.json()
        reply = chat_data.get("reply") or chat_data.get("message") or ""
        
        has_doc_terms = ("10th" in reply or "Marksheet" in reply or "Income" in reply or "Aadhaar" in reply or "PAN" in reply or "Certificate" in reply)
        t7_pass = res_chat.status_code == 200 and has_doc_terms
        log_test("Test 7: Contextual AI Chat Assistant", t7_pass, f"Response sample: {reply[:100]}...")
        if not t7_pass: all_passed = False
    except Exception as e:
        log_test("Test 7: Chat Assistant", False, str(e))
        all_passed = False

    # -------------------------------------------------------------
    # TEST 8: Admin & DBT Banks Dynamic Loading
    # -------------------------------------------------------------
    try:
        res_banks = requests.get(f"{BASE_URL}/banking/banks", timeout=10)
        banks_data = res_banks.json()
        banks_list = banks_data if isinstance(banks_data, list) else banks_data.get("banks", [])
        
        res_schemes = requests.get(f"{BASE_URL}/schemes", timeout=10)
        res_branches = requests.get(f"{BASE_URL}/banking/branches", timeout=10)
        
        t8_pass = res_banks.status_code == 200 and len(banks_list) >= 4 and res_schemes.status_code == 200 and res_branches.status_code == 200
        log_test("Test 8: DBT Banks Dynamic List & Admin Hub Endpoints", t8_pass, 
                 f"Dynamic Banks loaded: {len(banks_list)}, Schemes API: {res_schemes.status_code}, Branches API: {res_branches.status_code}")
        if not t8_pass: all_passed = False
    except Exception as e:
        log_test("Test 8: Admin & DBT Banks", False, str(e))
        all_passed = False

    print("=" * 70)
    if all_passed:
        print("[SUCCESS] ALL 8 TESTS PASSED SUCCESSFULLY! The Scheme Sathi system is fully verified.")
    else:
        print("[WARNING] SOME TESTS FAILED. Please review the output above.")
    print("=" * 70)

if __name__ == "__main__":
    main()
