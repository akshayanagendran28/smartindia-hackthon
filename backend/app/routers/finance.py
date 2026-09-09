import math
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
