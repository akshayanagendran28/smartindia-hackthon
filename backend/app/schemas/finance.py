from pydantic import BaseModel
from typing import Optional, List

class EmiCalculateRequest(BaseModel):
    loan_amount: float
    interest_rate_annual: float
    tenure_months: int
    moratorium_months: Optional[int] = 0

class AmortizationScheduleRow(BaseModel):
    month: int
    opening_balance: float
    emi: float
    principal_paid: float
    interest_paid: float
    closing_balance: float

class EmiCalculateResponse(BaseModel):
    loan_amount: float
    interest_rate_annual: float
    tenure_months: int
    moratorium_months: int
    monthly_emi: float
    total_interest: float
    total_repayment: float
    estimated_disclaimer: str = "All values are indicative estimates based on standard amortization schedules. Final terms depend on sanctioning authority."
    schedule_sample: List[AmortizationScheduleRow] = []
