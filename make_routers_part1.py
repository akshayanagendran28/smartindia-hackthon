import os

base = "C:/Users/aksha/.gemini/antigravity/scratch/scheme-sathi/backend"

def save(rel_path, content):
    full_path = os.path.join(base, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {rel_path}")

# app/routers/auth.py
save("app/routers/auth.py", """from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User, UserProfile
from app.schemas.auth import UserRegister, UserLogin, Token, UserOut
from app.auth.security import verify_password, get_password_hash, create_access_token
from app.auth.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=Token)
def register(user_in: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_in.email.lower()).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists."
        )
    
    user = User(
        email=user_in.email.lower(),
        mobile=user_in.mobile,
        full_name=user_in.full_name,
        hashed_password=get_password_hash(user_in.password),
        role=user_in.role or "entrepreneur",
        state=user_in.state,
        district=user_in.district,
        preferred_language=user_in.preferred_language or "en"
    )
    db.add(user)
    db.flush()

    # Create empty initial profile
    profile = UserProfile(
        user_id=user.id,
        location_state=user_in.state,
        location_district=user_in.district,
        profile_completed=False
    )
    db.add(profile)
    db.commit()
    db.refresh(user)

    token = create_access_token(subject=user.id)
    return {"access_token": token, "token_type": "bearer", "user": user}

@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email.lower()).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password."
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Account is disabled.")

    token = create_access_token(subject=user.id)
    return {"access_token": token, "token_type": "bearer", "user": user}

@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
""")

# app/routers/profile.py
save("app/routers/profile.py", """from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User, UserProfile
from app.schemas.profile import ProfileUpdate, ProfileOut
from app.auth.deps import get_current_user

router = APIRouter(prefix="/profile", tags=["User Profile"])

@router.get("", response_model=ProfileOut)
def get_user_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if not profile:
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile

@router.put("", response_model=ProfileOut)
def update_user_profile(profile_in: ProfileUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if not profile:
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)

    update_data = profile_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)

    # Mark as completed if essential fields are set
    if profile.annual_family_income is not None and profile.age and profile.purpose:
        profile.profile_completed = True

    db.commit()
    db.refresh(profile)
    return profile
""")

# app/routers/schemes.py
save("app/routers/schemes.py", """from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.session import get_db
from app.models.scheme import Scheme, SchemeVersion, SchemeRule, SchemeDocument
from app.schemas.scheme import SchemeOut, SchemeBase

router = APIRouter(prefix="/schemes", tags=["Schemes Catalog"])

@router.get("", response_model=List[SchemeOut])
def list_schemes(
    category: Optional[str] = None,
    department: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Scheme).filter(Scheme.is_active == True)
    if category:
        query = query.filter(Scheme.category == category)
    if department:
        query = query.filter(Scheme.department.ilike(f"%{department}%"))
    if search:
        query = query.filter(
            (Scheme.name.ilike(f"%{search}%")) |
            (Scheme.code.ilike(f"%{search}%")) |
            (Scheme.description.ilike(f"%{search}%"))
        )
    return query.all()

@router.get("/{scheme_id}", response_model=SchemeOut)
def get_scheme_details(scheme_id: int, db: Session = Depends(get_db)):
    scheme = db.query(Scheme).filter(Scheme.id == scheme_id).first()
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found.")
    return scheme
""")

# app/routers/finance.py
save("app/routers/finance.py", """import math
from fastapi import APIRouter
from app.schemas.finance import EmiCalculateRequest, EmiCalculateResponse, AmortizationScheduleRow

router = APIRouter(prefix="/finance", tags=["Financial Guidance & EMI"])

@router.post("/emi", response_model=EmiCalculateResponse)
def calculate_emi(data: EmiCalculateRequest):
    P = float(data.loan_amount)
    r_annual = float(data.interest_rate_annual)
    N = int(data.tenure_months)
    M = int(data.moratorium_months or 0)

    # Convert annual interest rate % to monthly decimal
    r_monthly = (r_annual / 12.0) / 100.0

    # Handle 0% interest (Grants / Zero interest loans like ASIIM)
    if r_monthly == 0.0 or r_annual == 0.0:
        effective_tenure = max(N - M, 1)
        monthly_emi = round(P / effective_tenure, 2)
        total_interest = 0.0
        total_repayment = round(P, 2)
    else:
        # Standard EMI Formula: [P * r * (1 + r)^n] / [(1 + r)^n - 1]
        effective_tenure = max(N - M, 1)
        # Interest accrued during moratorium
        principal_after_moratorium = P * ((1.0 + r_monthly) ** M) if M > 0 else P
        
        factor = (1.0 + r_monthly) ** effective_tenure
        monthly_emi = round((principal_after_moratorium * r_monthly * factor) / (factor - 1.0), 2)
        total_repayment = round(monthly_emi * effective_tenure, 2)
        total_interest = round(total_repayment - P, 2)

    # Generate Amortization Schedule Sample (First 12 months)
    schedule = []
    curr_balance = P
    for month in range(1, min(N + 1, 13)):
        if month <= M:
            interest_paid = round(curr_balance * r_monthly, 2)
            principal_paid = 0.0
            emi_paid = 0.0
            curr_balance = round(curr_balance + interest_paid, 2)
        else:
            interest_paid = round(curr_balance * r_monthly, 2)
            principal_paid = round(min(monthly_emi - interest_paid, curr_balance), 2)
            emi_paid = round(principal_paid + interest_paid, 2)
            curr_balance = round(max(0.0, curr_balance - principal_paid), 2)

        schedule.append(AmortizationScheduleRow(
            month=month,
            opening_balance=round(curr_balance + principal_paid, 2),
            emi=emi_paid,
            principal_paid=principal_paid,
            interest_paid=interest_paid,
            closing_balance=curr_balance
        ))

    return EmiCalculateResponse(
        loan_amount=P,
        interest_rate_annual=r_annual,
        tenure_months=N,
        moratorium_months=M,
        monthly_emi=monthly_emi,
        total_interest=max(0.0, total_interest),
        total_repayment=total_repayment,
        schedule_sample=schedule
    )
""")

# app/routers/matching.py
save("app/routers/matching.py", """import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.session import get_db
from app.models.user import User, UserProfile
from app.models.scheme import Scheme
from app.models.application import Recommendation, EligibilityResult
from app.schemas.matching import QuestionnaireInput, MatchingResponse, SchemeRecommendationOut
from app.services.ranking import ExplainableRankingService
from app.rules.engine import EligibilityRuleEngine
from app.auth.deps import get_current_user

router = APIRouter(prefix="/matching", tags=["AI Scheme Matching & Eligibility"])

@router.post("/analyze", response_model=MatchingResponse)
def analyze_and_rank_schemes(
    user_input: QuestionnaireInput,
    db: Session = Depends(get_db)
):
    schemes = db.query(Scheme).filter(Scheme.is_active == True).all()
    user_dict = user_input.model_dump()

    recommendations: List[SchemeRecommendationOut] = []
    eligible_count = 0

    for scheme in schemes:
        ranked_res = ExplainableRankingService.rank_scheme(scheme, user_dict)
        rec_out = SchemeRecommendationOut(**ranked_res)
        recommendations.append(rec_out)
        if rec_out.is_eligible:
            eligible_count += 1

    # Sort primarily by eligibility status (eligible first) then by match score descending
    recommendations.sort(key=lambda x: (1 if x.is_eligible else 0, x.match_score), reverse=True)

    return MatchingResponse(
        total_evaluated=len(schemes),
        eligible_count=eligible_count,
        recommendations=recommendations
    )

@router.post("/eligibility/check/{scheme_id}")
def check_single_scheme_eligibility(
    scheme_id: int,
    user_input: QuestionnaireInput,
    db: Session = Depends(get_db)
):
    scheme = db.query(Scheme).filter(Scheme.id == scheme_id).first()
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found.")
    
    result = EligibilityRuleEngine.check_scheme_eligibility(scheme, user_input.model_dump())
    ranked = ExplainableRankingService.rank_scheme(scheme, user_input.model_dump())
    
    return {
        "scheme_id": scheme.id,
        "scheme_name": scheme.name,
        "scheme_code": scheme.code,
        "eligible": result["eligible"],
        "eligibility_score": result["score"],
        "matched_rules": result["matched_rules"],
        "failed_rules": result["failed_rules"],
        "missing_documents": result["missing_documents"],
        "compatibility_breakdown": ranked["compatibility_breakdown"],
        "matching_factors": ranked["matching_factors"],
        "missing_requirements": ranked["missing_requirements"]
    }
""")

print("Routers Part 1 generated successfully!")
