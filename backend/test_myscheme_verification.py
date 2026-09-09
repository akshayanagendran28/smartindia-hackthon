import sys
import os
import json

sys.path.insert(0, os.path.abspath("."))
from app.database.seed import seed_database
from app.database.session import SessionLocal
from app.models.scheme import Scheme
from app.models.partner import ChannelPartner
from app.services.ranking import ExplainableRankingService
from app.services.geo import GeospatialPartnerService

print("=== 1. SEEDING & SCHEME VERIFICATION ===")
db = SessionLocal()
seed_database(db)
schemes = db.query(Scheme).all()
print(f"Total Schemes in Database: {len(schemes)}")
for s in schemes:
    states = s.eligible_states
    print(f" - [{s.code}] {s.name[:45]} | Category: {s.category} | States: {states}")

print("\n=== 2. RULE ENGINE & MATCHING SIMULATION ===")
# Test Case 1: Rural SC Woman entrepreneur seeking Rs. 25 Lakh manufacturing loan in Tamil Nadu
user1 = {
    "age": 29,
    "gender": "Female",
    "social_category": "SC",
    "state": "Tamil Nadu",
    "area_type": "Rural",
    "required_loan": 2500000,
    "project_cost": 2500000,
    "business_type": "Manufacturing",
    "purpose": "Start a Business",
    "education": "Graduate",
    "annual_income": 240000,
    "has_training": True
}

ranked1 = [ExplainableRankingService.rank_scheme(s, user1) for s in schemes]
eligible1 = [r for r in ranked1 if r["is_eligible"]]
eligible1.sort(key=lambda x: x["match_score"], reverse=True)

print(f"\nUser 1 (SC Rural Woman in Tamil Nadu, Rs 25 Lakh): {len(eligible1)} schemes eligible")
for top in eligible1[:5]:
    print(f"  -> Score: {top['match_score']}% | Scheme: {top['scheme_name']} ({top['scheme_code']})")
    print(f"     Top factors: {top['matching_factors'][:2]}")

# Test Case 2: Urban Street Vendor seeking Rs. 20,000 loan in Karnataka
user2 = {
    "age": 35,
    "gender": "Male",
    "social_category": "OBC",
    "state": "Karnataka",
    "area_type": "Urban",
    "required_loan": 20000,
    "project_cost": 25000,
    "business_type": "Micro Retail / Street Vendor",
    "purpose": "Working Capital",
    "education": "10th Pass",
    "annual_income": 90000
}

ranked2 = [ExplainableRankingService.rank_scheme(s, user2) for s in schemes]
eligible2 = [r for r in ranked2 if r["is_eligible"]]
eligible2.sort(key=lambda x: x["match_score"], reverse=True)

print(f"\nUser 2 (Urban Street Vendor in Karnataka, Rs 20k): {len(eligible2)} schemes eligible")
for top in eligible2[:3]:
    print(f"  -> Score: {top['match_score']}% | Scheme: {top['scheme_name']} ({top['scheme_code']})")

# Test Case 3: Partner bank locator (Chennai GPS)
partners = db.query(ChannelPartner).all()
eval_partners = [GeospatialPartnerService.evaluate_partner(p, 13.0827, 80.2707, "PMEGP") for p in partners]
eval_partners.sort(key=lambda x: x["partner_suitability_score"], reverse=True)

print(f"\n=== 3. PARTNER BANK LOCATOR (Chennai GPS 13.0827, 80.2707) ===")
print(f"Nearby evaluated banks/CSCs for PMEGP: {len(eval_partners)}")
for p in eval_partners[:4]:
    print(f"  -> {p['name']} ({p['partner_type']}) | Dist: {p['distance_km']} km | Suitability: {p['partner_suitability_score']}%")

db.close()
print("\n>>> ALL VERIFICATION TESTS COMPLETED SUCCESSFULLY! <<<")
