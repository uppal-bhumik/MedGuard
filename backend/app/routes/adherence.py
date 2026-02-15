"""
MedGuard — Adherence Router
POST /api/adherence  →  Log daily adherence summary
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AdherenceLog
from app.schemas import AdherenceLogCreate, AdherenceLogResponse

router = APIRouter(prefix="/api", tags=["Adherence"])


@router.post("/adherence_log", response_model=AdherenceLogResponse)
def log_adherence(data: AdherenceLogCreate, db: Session = Depends(get_db)):
    # Check if a log exists for this user and date
    log = db.query(AdherenceLog).filter(
        AdherenceLog.user_id == data.user_id,
        AdherenceLog.date == data.date
    ).first()
    
    if log:
        # Update existing
        log.all_taken = data.all_taken
        log.total_meds = data.total_meds
        log.taken_meds = data.taken_meds
    else:
        # Create new
        log = AdherenceLog(
            user_id=data.user_id,
            date=data.date,
            all_taken=data.all_taken,
            total_meds=data.total_meds,
            taken_meds=data.taken_meds
        )
        db.add(log)
    
    db.commit()
    db.refresh(log)
    return log
