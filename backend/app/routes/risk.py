"""
MedGuard — Risk Router
GET /api/risk/{user_id}  →  Calculate risk level from missed doses
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Profile, Medicine, AdherenceLog

router = APIRouter(prefix="/api", tags=["Risk"])


@router.get("/risk/{user_id}")
def get_risk(user_id: int, db: Session = Depends(get_db)):
    # Verify user exists
    profile = db.query(Profile).filter(Profile.id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    # Get all medicine IDs for this user
    medicine_ids = [
        m.id for m in db.query(Medicine).filter(Medicine.user_id == user_id).all()
    ]

    # Count missed doses (taken = false)
    missed = (
        db.query(AdherenceLog)
        .filter(AdherenceLog.medicine_id.in_(medicine_ids), AdherenceLog.taken == False)
        .count()
    ) if medicine_ids else 0

    # Risk rules
    if missed == 0:
        risk_level = "Low"
    elif missed <= 2:
        risk_level = "Medium"
    else:
        risk_level = "High"

    return {
        "user_id": user_id,
        "missed_doses": missed,
        "risk_level": risk_level,
    }
