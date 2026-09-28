from fastapi import APIRouter, Depends, HTTPException, Query
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

@router.get("/{scheme_id_or_code}", response_model=SchemeOut)
def get_scheme_details(scheme_id_or_code: str, db: Session = Depends(get_db)):
    scheme = None
    if scheme_id_or_code.isdigit():
        scheme = db.query(Scheme).filter(Scheme.id == int(scheme_id_or_code)).first()
    if not scheme:
        scheme = db.query(Scheme).filter(
            (Scheme.code.ilike(scheme_id_or_code)) | 
            (Scheme.name.ilike(scheme_id_or_code))
        ).first()
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found in database.")
    return scheme
