from app.database.session import SessionLocal
from app.models.scheme import Scheme
from app.services.ranking import ExplainableRankingService

db = SessionLocal()
schemes = db.query(Scheme).all()

user1 = {
    "purpose": "Start a Business",
    "annual_family_income": 180000.0,
    "category": "OBC",
    "project_cost": 40000.0,
    "required_loan_amount": 30000.0,
    "age": 29,
    "business_type": "Micro Retail",
    "state": "Maharashtra",
    "available_documents": ["Aadhaar Card", "Bank Account Statement"]
}

print("=== TEST 1: Street Vendor / Micro Retail ===")
for s in schemes:
    ranked = ExplainableRankingService.rank_scheme(s, user1)
    print(f"[{ranked['match_score']}%] {s.name[:45]} -> {ranked['eligibility_status']}")
    for factor in ranked['matching_factors'][:2]:
        print(f"   ✓ {factor}")

db.close()
