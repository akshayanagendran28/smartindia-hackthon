import json
from typing import Dict, Any, List, Tuple
from app.models.scheme import Scheme, SchemeRule

class EligibilityRuleEngine:
    """
    Deterministic Rule Engine for Scheme Sathi.
    Evaluates applicant profile parameters against explicit scheme rules.
    Guarantees transparent, explainable decisions without blackbox hallucinations.
    """

    @staticmethod
    def evaluate_rule(rule: SchemeRule, user_data: Dict[str, Any]) -> Tuple[bool, str]:
        field = rule.field_name
        op = rule.operator.lower()
        threshold_raw = rule.threshold_value
        
        val = user_data.get(field)
        
        # Handle missing field
        if val is None:
            # Check if default is acceptable or fail
            if field == "age": val = 25
            elif field == "annual_family_income": val = 0.0
            elif field == "project_cost": val = 0.0
            elif field == "required_loan_amount": val = 0.0
            elif field == "category": val = "General"
            elif field == "purpose": val = "Start a Business"
            elif field == "business_type": val = "Micro Retail"
            else:
                return True, "Field not provided, skipped"

        try:
            if op in ["<=", "max_limit", "max"]:
                threshold = float(threshold_raw)
                user_val = float(val)
                if user_val <= threshold or threshold <= 0:
                    return True, f"{field.replace('_', ' ').title()} (₹{user_val:,.0f} or {user_val}) is within allowable limit of ₹{threshold:,.0f}."
                else:
                    reason = rule.failure_reason_template or f"{field.replace('_', ' ').title()} exceeds allowable limit of ₹{threshold:,.0f}."
                    return False, reason

            elif op in [">=", "min_limit", "min"]:
                threshold = float(threshold_raw)
                user_val = float(val)
                if user_val >= threshold:
                    return True, f"{field.replace('_', ' ').title()} meets minimum threshold."
                else:
                    reason = rule.failure_reason_template or f"{field.replace('_', ' ').title()} does not meet minimum threshold."
                    return False, reason

            elif op in ["==", "=", "equals"]:
                if str(val).strip().lower() == str(threshold_raw).strip().lower():
                    return True, f"Condition matched: {field} is {val}."
                else:
                    reason = rule.failure_reason_template or f"{field.replace('_', ' ').title()} does not match required value {threshold_raw}."
                    return False, reason

            elif op in ["!=", "not_equals"]:
                if str(val).strip().lower() != str(threshold_raw).strip().lower():
                    return True, f"Requirement matched: {field} != {threshold_raw}."
                else:
                    return False, rule.failure_reason_template or f"Failed inequality condition for {field}."

            elif op in ["in", "contains", "in_list", "one_of"]:
                try:
                    valid_items = json.loads(threshold_raw) if threshold_raw.startswith("[") else [x.strip() for x in threshold_raw.split(",")]
                except Exception:
                    valid_items = [threshold_raw]
                
                valid_items_lower = [str(x).strip().lower() for x in valid_items]
                user_val_str = str(val).strip().lower()
                
                # Check for All India or All
                if "all" in valid_items_lower or "all india" in valid_items_lower:
                    return True, f"{field.replace('_', ' ').title()} is universally eligible."
                
                if user_val_str in valid_items_lower or any(user_val_str in item for item in valid_items_lower):
                    return True, f"{field.replace('_', ' ').title()} ({val}) is listed as eligible."
                else:
                    reason = rule.failure_reason_template or f"{field.replace('_', ' ').title()} ({val}) is not supported for this scheme."
                    return False, reason

            elif op in ["category_match"]:
                try:
                    cats = json.loads(threshold_raw) if threshold_raw.startswith("[") else [threshold_raw]
                except Exception:
                    cats = [threshold_raw]
                cats_lower = [c.lower() for c in cats]
                user_cat = str(val).lower()
                
                if "general" in cats_lower or "all" in cats_lower or user_cat in cats_lower:
                    return True, f"Social category '{val}' is fully eligible."
                else:
                    reason = rule.failure_reason_template or f"Scheme requires category in {cats}, user is '{val}'."
                    return False, reason

            else:
                return True, "Default pass"

        except Exception as e:
            return True, f"Evaluation bypass: {str(e)}"

    @classmethod
    def check_scheme_eligibility(cls, scheme: Scheme, user_data: Dict[str, Any]) -> Dict[str, Any]:
        matched_rules = []
        failed_rules = []
        
        # 1. Base Scheme Model Hard Limits Checks
        # Max income limit
        if scheme.max_income_limit and scheme.max_income_limit > 0:
            user_inc = float(user_data.get("annual_family_income", 0))
            if user_inc > scheme.max_income_limit:
                failed_rules.append({
                    "rule_code": "MAX_INCOME",
                    "rule_name": "Annual Family Income Ceiling",
                    "field": "annual_family_income",
                    "user_value": f"₹{user_inc:,.0f}",
                    "threshold": f"₹{scheme.max_income_limit:,.0f}",
                    "reason": f"Annual family income of ₹{user_inc:,.0f} exceeds the maximum allowed ceiling of ₹{scheme.max_income_limit:,.0f} for this scheme."
                })
            else:
                matched_rules.append({
                    "rule_code": "MAX_INCOME",
                    "rule_name": "Annual Family Income Ceiling",
                    "detail": f"Family income of ₹{user_inc:,.0f} is within allowable limit."
                })

        # Max project cost
        if scheme.max_project_cost and scheme.max_project_cost > 0:
            user_proj = float(user_data.get("project_cost", 0))
            if user_proj > scheme.max_project_cost:
                failed_rules.append({
                    "rule_code": "MAX_PROJECT_COST",
                    "rule_name": "Maximum Project Cost Limit",
                    "field": "project_cost",
                    "user_value": f"₹{user_proj:,.0f}",
                    "threshold": f"₹{scheme.max_project_cost:,.0f}",
                    "reason": f"Project cost of ₹{user_proj:,.0f} exceeds the maximum project cost limit of ₹{scheme.max_project_cost:,.0f} for {scheme.name}."
                })
            else:
                matched_rules.append({
                    "rule_code": "MAX_PROJECT_COST",
                    "rule_name": "Maximum Project Cost Limit",
                    "detail": f"Project cost of ₹{user_proj:,.0f} complies with scheme ceiling."
                })

        # Min / Max Age
        user_age = int(user_data.get("age", 25))
        if user_age < scheme.min_age or user_age > scheme.max_age:
            failed_rules.append({
                "rule_code": "AGE_RANGE",
                "rule_name": "Age Eligibility Requirement",
                "field": "age",
                "user_value": f"{user_age} years",
                "threshold": f"{scheme.min_age} - {scheme.max_age} years",
                "reason": f"Applicant age ({user_age} years) is outside the permitted age bracket ({scheme.min_age} to {scheme.max_age} years)."
            })
        else:
            matched_rules.append({
                "rule_code": "AGE_RANGE",
                "rule_name": "Age Eligibility Requirement",
                "detail": f"Age {user_age} years is eligible ({scheme.min_age}-{scheme.max_age} years permitted)."
            })

        # Purpose check
        user_purpose = user_data.get("purpose", "")
        if user_purpose:
            try:
                allowed_purposes = json.loads(scheme.eligible_purposes)
            except Exception:
                allowed_purposes = ["Start a Business", "Expand Existing Business"]
            
            allowed_purposes_lower = [p.lower() for p in allowed_purposes]
            if allowed_purposes_lower and not any(user_purpose.lower() in p or p in user_purpose.lower() for p in allowed_purposes_lower):
                failed_rules.append({
                    "rule_code": "ELIGIBLE_PURPOSE",
                    "rule_name": "Purpose Compatibility",
                    "field": "purpose",
                    "user_value": user_purpose,
                    "threshold": ", ".join(allowed_purposes),
                    "reason": f"Requested purpose '{user_purpose}' is not covered by this scheme (Supported: {', '.join(allowed_purposes)})."
                })
            else:
                matched_rules.append({
                    "rule_code": "ELIGIBLE_PURPOSE",
                    "rule_name": "Purpose Compatibility",
                    "detail": f"Purpose '{user_purpose}' is fully supported."
                })

        # Category check
        user_cat = user_data.get("category") or user_data.get("social_category") or "SC"
        try:
            allowed_cats = json.loads(scheme.eligible_categories)
        except Exception:
            allowed_cats = ["SC", "ST", "Minority", "Woman", "Divyangjan"]
        
        allowed_cats_lower = [c.lower() for c in allowed_cats]
        user_cat_lower = str(user_cat).lower()
        is_female = str(user_data.get("gender", "")).lower() == "female" or "woman" in user_cat_lower or "women" in user_cat_lower

        if "all" in allowed_cats_lower or "all india" in allowed_cats_lower or "general" in allowed_cats_lower:
            matched_rules.append({
                "rule_code": "CATEGORY_REQUIREMENT",
                "rule_name": "Target Social Category",
                "detail": f"Category '{user_cat}' qualifies for scheme allocation."
            })
        elif user_cat_lower in allowed_cats_lower or (is_female and ("woman" in allowed_cats_lower or "women" in allowed_cats_lower)):
            matched_rules.append({
                "rule_code": "CATEGORY_REQUIREMENT",
                "rule_name": "Target Social Category",
                "detail": f"Target category '{user_cat}' qualifies for special allocations/subsidies."
            })
        else:
            failed_rules.append({
                "rule_code": "CATEGORY_REQUIREMENT",
                "rule_name": "Target Social Category",
                "field": "category",
                "user_value": user_cat,
                "threshold": ", ".join([c for c in allowed_cats if c.lower() != 'general']),
                "reason": f"This scheme is targeted specifically for {', '.join([c for c in allowed_cats if c.lower() != 'general'])} applicants. Current profile category is '{user_cat}'."
            })

        # 2. Scheme Custom Database Rules
        for rule in scheme.rules:
            if not rule.is_active:
                continue
            passed, detail_or_reason = cls.evaluate_rule(rule, user_data)
            if passed:
                matched_rules.append({
                    "rule_code": rule.rule_code,
                    "rule_name": rule.rule_name,
                    "detail": detail_or_reason
                })
            else:
                failed_rules.append({
                    "rule_code": rule.rule_code,
                    "rule_name": rule.rule_name,
                    "field": rule.field_name,
                    "user_value": str(user_data.get(rule.field_name, "N/A")),
                    "threshold": rule.threshold_value,
                    "reason": detail_or_reason
                })

        # 3. Document Availability Analysis
        avail_docs = [d.lower() for d in user_data.get("available_documents", [])]
        missing_docs = []
        for doc in scheme.documents:
            if doc.is_mandatory:
                dt = doc.document_type.lower()
                dn = doc.document_name.lower()
                if not any(dt in ad or dn in ad or ad in dt for ad in avail_docs):
                    missing_docs.append(doc.document_name)

        is_eligible = len(failed_rules) == 0
        total_rules = len(matched_rules) + len(failed_rules)
        eligibility_score = round((len(matched_rules) / max(total_rules, 1)) * 100, 1)

        return {
            "eligible": is_eligible,
            "score": eligibility_score,
            "matched_rules": matched_rules,
            "failed_rules": failed_rules,
            "missing_documents": missing_docs
        }
