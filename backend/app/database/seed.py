import json
import datetime
from sqlalchemy.orm import Session
from app.models.user import User, UserProfile
from app.models.scheme import Scheme, SchemeRule, SchemeDocument, SchemeVersion
from app.models.partner import ChannelPartner, PartnerScheme
from app.models.application import Notification
from app.auth.security import get_password_hash
from app.database.myscheme_dataset import MYSCHEME_DATASET

def seed_database(db: Session):
    print("Seeding canonical myScheme.gov.in official dataset...")

    # 1. Seed Demo Users
    def ensure_user(email, name, pwd, role, category, gender, income, state, district):
        u = db.query(User).filter(User.email == email).first()
        if not u:
            u = User(
                email=email,
                full_name=name,
                hashed_password=get_password_hash(pwd),
                role=role,
                state=state,
                district=district,
                preferred_language="en"
            )
            db.add(u)
            db.flush()
            prof = UserProfile(
                user_id=u.id,
                full_name=name,
                age=29,
                gender=gender,
                category=category,
                social_category=category,
                annual_family_income=income,
                annual_income=income,
                purpose="Start a Business",
                required_loan_amount=1200000.0,
                required_loan=1200000.0,
                project_cost=1500000.0,
                state=state,
                district=district,
                location_state=state,
                location_district=district,
                area_type="rural",
                business_type="manufacturing",
                has_training=True,
                has_skill_training=True,
                profile_completed=True
            )
            db.add(prof)
            db.commit()
            print(f"Created demo user: {email}")
        else:
            u.hashed_password = get_password_hash(pwd)
            db.commit()

    ensure_user("admin@schemesathi.gov.in", "National Portal Admin", "admin123", "admin", "General", "female", 600000.0, "Delhi", "New Delhi")
    ensure_user("supervisor@schemesathi.gov.in", "State Nodal Supervisor", "super123", "supervisor", "General", "male", 450000.0, "Maharashtra", "Mumbai")
    ensure_user("priya@example.com", "Priya Sharma (Woman SC Founder)", "password123", "entrepreneur", "SC", "female", 180000.0, "Maharashtra", "Mumbai")
    ensure_user("rahul@example.com", "Rahul Gupta (Street Vendor)", "password123", "entrepreneur", "OBC", "male", 95000.0, "Delhi", "New Delhi")
    ensure_user("ananya@example.com", "Ananya Roy (Student Founder)", "password123", "entrepreneur", "General", "female", 220000.0, "Karnataka", "Bengaluru")
    ensure_user("karthik@example.com", "Karthik Raja (Artisan / Handicraft)", "password123", "entrepreneur", "Minority", "male", 140000.0, "Tamil Nadu", "Chennai")

    # 2. Seed All Verified Schemes from myScheme.gov.in
    for item in MYSCHEME_DATASET:
        existing = db.query(Scheme).filter(Scheme.code == item["code"]).first()
        if not existing:
            subsidy_str = json.dumps(item.get("subsidy_details", {})) if isinstance(item.get("subsidy_details"), dict) else str(item.get("subsidy_details", ""))
            
            scheme = Scheme(
                code=item["code"],
                name=item["name"],
                department=item["department"],
                category=item.get("category", "Business & Entrepreneurship"),
                description=item["description"],
                loan_type=item.get("loan_type", "Term Loan"),
                min_loan_amount=item.get("min_loan_amount", 10000.0),
                max_loan_amount=item.get("max_loan_amount", 1000000.0),
                min_project_cost=item.get("min_project_cost", 10000.0),
                max_project_cost=item.get("max_project_cost", 5000000.0),
                min_age=item.get("min_age", 18),
                max_age=item.get("max_age", 65),
                max_income_limit=item.get("max_income_limit"),
                interest_rate_min=item.get("interest_rate_min", 7.0),
                interest_rate_max=item.get("interest_rate_max", 12.0),
                interest_rate_display=item.get("interest_rate_display", "Concessional"),
                repayment_period_months=item.get("repayment_period_months", 60),
                moratorium_months=item.get("moratorium_months", 6),
                subsidy_percentage_general=item.get("subsidy_percentage_general", 0.0),
                subsidy_percentage_special=item.get("subsidy_percentage_special", 0.0),
                subsidy_details=subsidy_str,
                eligible_purposes=json.dumps(item.get("eligible_purposes", ["Start a Business"])),
                eligible_business_types=json.dumps(item.get("eligible_business_types", ["manufacturing", "service"])),
                eligible_categories=json.dumps(item.get("eligible_categories", ["General", "SC", "ST", "OBC", "Minority", "Woman"])),
                eligible_states=json.dumps(item.get("eligible_states", ["All India"])),
                eligible_education=json.dumps(item.get("eligible_education", [])),
                official_portal_url=item.get("official_portal_url", "https://www.myscheme.gov.in"),
                application_process=item.get("application_process", ""),
                version=1,
                is_active=True
            )
            db.add(scheme)
            db.flush()

            # Add Version 1.0 baseline
            version_entry = SchemeVersion(
                scheme_id=scheme.id,
                version_number=1,
                change_summary="Official myScheme.gov.in gazetted scheme baseline.",
                updated_by="National Admin"
            )
            db.add(version_entry)

            # Add Default Rules
            rules_to_add = [
                {
                    "rule_name": f"{scheme.code} Minimum Age Rule",
                    "rule_code": f"{scheme.code}_MIN_AGE",
                    "field_name": "age",
                    "operator": ">=",
                    "threshold_value": str(item.get("min_age", 18)),
                    "failure_reason_template": f"Applicant must be at least {item.get('min_age', 18)} years of age."
                },
                {
                    "rule_name": f"{scheme.code} Project Cost Limit",
                    "rule_code": f"{scheme.code}_MAX_PROJ",
                    "field_name": "project_cost",
                    "operator": "<=",
                    "threshold_value": str(int(item.get("max_project_cost", 5000000))),
                    "failure_reason_template": f"Project cost exceeds eligible limit of ₹{int(item.get('max_project_cost', 5000000)):,}."
                }
            ]

            if item.get("max_income_limit"):
                rules_to_add.append({
                    "rule_name": f"{scheme.code} Income Ceiling",
                    "rule_code": f"{scheme.code}_INCOME_CAP",
                    "field_name": "annual_family_income",
                    "operator": "<=",
                    "threshold_value": str(int(item["max_income_limit"])),
                    "failure_reason_template": f"Annual family income exceeds maximum ceiling of ₹{int(item['max_income_limit']):,}."
                })

            for r in rules_to_add:
                db.add(SchemeRule(scheme_id=scheme.id, **r))

            # Add Documents
            for doc in item.get("required_documents", []):
                db.add(SchemeDocument(
                    scheme_id=scheme.id,
                    document_name=doc["name"],
                    document_type=doc.get("type", "identity_proof"),
                    is_mandatory=doc.get("mandatory", True)
                ))

    db.commit()

    # 3. Seed Channel Partners
    if db.query(ChannelPartner).count() == 0:
        partners_data = [
            {"name": "Bank of India - Mumbai Lead District Office", "partner_type": "bank", "address": "Fort, Mumbai", "city": "Mumbai", "district": "Mumbai", "state": "Maharashtra", "pincode": "400001", "latitude": 18.9322, "longitude": 72.8347, "phone": "022-22661000", "nodal_officer": "R. K. Verma", "rating": 4.8},
            {"name": "State Bank of India - MSME Branch Bandra", "partner_type": "bank", "address": "Bandra Kurla Complex", "city": "Mumbai", "district": "Mumbai", "state": "Maharashtra", "pincode": "400051", "latitude": 19.0657, "longitude": 72.8687, "phone": "022-26565000", "nodal_officer": "Sunita Patil", "rating": 4.9},
            {"name": "Canara Bank - PMEGP Nodal Desk", "partner_type": "bank", "address": "MG Road, Bengaluru", "city": "Bengaluru", "district": "Bengaluru Urban", "state": "Karnataka", "pincode": "560001", "latitude": 12.9716, "longitude": 77.5946, "phone": "080-25584000", "nodal_officer": "M. Suresh", "rating": 4.7},
            {"name": "Punjab National Bank - Delhi Central Desk", "partner_type": "bank", "address": "Connaught Place", "city": "Delhi", "district": "New Delhi", "state": "Delhi", "pincode": "110001", "latitude": 28.6315, "longitude": 77.2167, "phone": "011-23321000", "nodal_officer": "Amit Saxena", "rating": 4.6},
            {"name": "Indian Overseas Bank - MSME Hub Chennai", "partner_type": "bank", "address": "Mount Road, Anna Salai", "city": "Chennai", "district": "Chennai", "state": "Tamil Nadu", "pincode": "600002", "latitude": 13.0827, "longitude": 80.2707, "phone": "044-28525000", "nodal_officer": "K. Raman", "rating": 4.8},
            {"name": "Union Bank of India - Pune Camp Branch", "partner_type": "bank", "address": "Camp, Pune", "city": "Pune", "district": "Pune", "state": "Maharashtra", "pincode": "411001", "latitude": 18.5204, "longitude": 73.8567, "phone": "020-26123000", "nodal_officer": "V. Deshmukh", "rating": 4.7},
            {"name": "Bank of Baroda - Lucknow Hazratganj", "partner_type": "bank", "address": "Hazratganj", "city": "Lucknow", "district": "Lucknow", "state": "Uttar Pradesh", "pincode": "226001", "latitude": 26.8467, "longitude": 80.9462, "phone": "0522-2234000", "nodal_officer": "Pradeep Yadav", "rating": 4.5},
            {"name": "Kolkata MSME Facilitation Desk", "partner_type": "bank", "address": "BBD Bagh", "city": "Kolkata", "district": "Kolkata", "state": "West Bengal", "pincode": "700001", "latitude": 22.5726, "longitude": 88.3639, "phone": "033-22485000", "nodal_officer": "Subrata Mukherjee", "rating": 4.6},
            {"name": "Digital India CSC e-Governance Point #104", "partner_type": "csc_center", "address": "Dharavi Main Road", "city": "Mumbai", "district": "Mumbai", "state": "Maharashtra", "pincode": "400017", "latitude": 19.0410, "longitude": 72.8530, "phone": "022-24018899", "nodal_officer": "Anil Kamble", "rating": 4.9},
            {"name": "CSC e-Gram Seva Kendra #218", "partner_type": "csc_center", "address": "Kengeri Satellite Town", "city": "Bengaluru", "district": "Bengaluru Urban", "state": "Karnataka", "pincode": "560060", "latitude": 12.9177, "longitude": 77.4838, "phone": "080-28485566", "nodal_officer": "Girish Rao", "rating": 4.8},
            {"name": "District Industries Centre (DIC) Mumbai", "partner_type": "dic_office", "address": "Old Custom House, Fort", "city": "Mumbai", "district": "Mumbai", "state": "Maharashtra", "pincode": "400001", "latitude": 18.9300, "longitude": 72.8350, "phone": "022-22662000", "nodal_officer": "General Manager DIC", "rating": 4.7},
            {"name": "District Industries Centre (DIC) Chennai", "partner_type": "dic_office", "address": "Guindy Industrial Estate", "city": "Chennai", "district": "Chennai", "state": "Tamil Nadu", "pincode": "600032", "latitude": 13.0067, "longitude": 80.2033, "phone": "044-22501000", "nodal_officer": "General Manager DIC", "rating": 4.8}
        ]

        for p in partners_data:
            partner = ChannelPartner(
                name=p["name"],
                partner_type=p["partner_type"],
                address=p["address"],
                city=p["city"],
                district=p["district"],
                state=p["state"],
                pincode=p["pincode"],
                latitude=p["latitude"],
                longitude=p["longitude"],
                contact_person=p["nodal_officer"],
                contact_phone=p["phone"],
                contact_email="helpdesk@" + p["name"].lower().replace(" ", "")[:10] + ".gov.in",
                average_rating=p["rating"],
                supported_schemes=json.dumps(["PMEGP", "STANDUP-IND", "MUDRA-SHISHU", "MUDRA-KISHORE", "SVANIDHI", "VISHWAKARMA", "TN-NEEDS", "MH-CMEGP", "KA-UDYOGINI", "KL-ESS", "UP-MMYSY", "WB-KARMA-SATHI"]),
                is_active=True
            )
            db.add(partner)

        db.commit()

    print("myScheme.gov.in dataset seeding successfully completed!")
