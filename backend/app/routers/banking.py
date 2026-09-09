# -*- coding: utf-8 -*-
"""
Banking & Offline Razorpay IFSC API Router
Provides offline IFSC verification, branch discovery, and DBT subsidy bank validation.
"""
from fastapi import APIRouter, HTTPException, Query, Body
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from app.services.banking_service import OfflineBankingService

router = APIRouter(prefix="/banking", tags=["Offline Razorpay IFSC & Banking"])

class BankAccountVerificationRequest(BaseModel):
    account_number: str
    ifsc: str
    holder_name: Optional[str] = None
    scheme_code: Optional[str] = None

@router.get("/ifsc/{ifsc_code}")
def lookup_ifsc(ifsc_code: str):
    """
    Offline IFSC Lookup conforming to the Razorpay IFSC schema.
    """
    result = OfflineBankingService.lookup_ifsc(ifsc_code)
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"IFSC Code '{ifsc_code}' not found in offline dataset."
        )
    return result

@router.get("/branches")
def search_branches(
    query: Optional[str] = Query(None, description="Search by Bank, Branch, IFSC, City, or District"),
    state: Optional[str] = Query(None, description="Filter by State"),
    district: Optional[str] = Query(None, description="Filter by District"),
    bank: Optional[str] = Query(None, description="Filter by Bank Name"),
    scheme_code: Optional[str] = Query(None, description="Filter by Supported Scheme"),
    limit: int = Query(50, description="Max results")
):
    """
    Search offline bank branches and Lead Bank offices.
    """
    return OfflineBankingService.search_branches(
        query=query,
        state=state,
        district=district,
        bank=bank,
        scheme_code=scheme_code,
        limit=limit
    )

@router.post("/verify-account")
def verify_bank_account(req: BankAccountVerificationRequest):
    """
    Offline Bank Account & IFSC Check for Direct Benefit Transfer (DBT) Scheme Disbursement.
    """
    return OfflineBankingService.verify_account_for_dbt(
        account_number=req.account_number,
        ifsc_code=req.ifsc,
        account_holder_name=req.holder_name
    )

@router.get("/banks")
def list_supported_banks():
    """
    Returns unique list of banks available in offline IFSC database.
    """
    conn = OfflineBankingService.get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT bank FROM ifsc_data ORDER BY bank ASC")
    rows = cursor.fetchall()
    return [r["bank"] for r in rows]

@router.get("/states")
def list_states():
    """
    Returns unique list of states available in offline database.
    """
    conn = OfflineBankingService.get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT state FROM ifsc_data ORDER BY state ASC")
    rows = cursor.fetchall()
    return [r["state"] for r in rows]

@router.get("/map-points")
def get_map_points(
    state: Optional[str] = None,
    scheme_code: Optional[str] = None
):
    """
    Returns optimized branch geodata points for offline map rendering.
    """
    branches = OfflineBankingService.search_branches(state=state, scheme_code=scheme_code, limit=100)
    return {
        "status": "SUCCESS",
        "is_offline_ready": True,
        "dataset_source": "Razorpay IFSC Open Dataset + RBI Official Registry",
        "total_points": len(branches),
        "points": branches
    }
