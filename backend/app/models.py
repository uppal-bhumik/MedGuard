"""
MedGuard — SQLAlchemy ORM Models
Tables: profiles, medicines, adherence_log
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base


class Profile(Base):
    __tablename__ = "profiles"

    # Changed to String to support UUIDs from frontend auth
    id = Column(String, primary_key=True, index=True)
    full_name = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    is_senior = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # One profile → many medicines
    medicines = relationship("Medicine", back_populates="owner", cascade="all, delete-orphan")


class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("profiles.id"), nullable=False)
    name = Column(String, nullable=False)
    dosage = Column(String, nullable=True)
    is_antibiotic = Column(Boolean, default=False)
    status = Column(String, default="pending")  # pending, taken, skipped
    urgent = Column(Boolean, default=False)
    times = Column(JSON, default=list)  # Store times as a JSON list ["08:00", "20:00"]
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    owner = relationship("Profile", back_populates="medicines")
    # doses relationship removed as AdherenceLog is now a daily summary


class AdherenceLog(Base):
    __tablename__ = "adherence_log"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("profiles.id"), nullable=False)
    date = Column(String, nullable=False)  # YYYY-MM-DD
    all_taken = Column(Boolean, default=False)
    total_meds = Column(Integer, default=0)
    taken_meds = Column(Integer, default=0)
    
    # Optional link to specific medicine dose if needed, but the frontend 
    # seems to aggregate by day. Keeping specific dose tracking is good for history though.
    # For now, let's keep the structure simple and aligned with the "Dashboard" logic 
    # which upserts a daily summary.
    
    # timestampt of record update
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # We might not need a direct relationship to Medicine if this is a daily summary 
    # but the previous model had it. The frontend 'adherence_log' seems to be a daily summary.
    # Let's add a separate table for individual dose logs if we want granular history, 
    # or just stick to the summary for now as requested.
    # actually, the previous model had `medicine_id` and `taken`. 
    # The frontend code in Dashboard.jsx does:
    # sb.from('adherence_log').upsert({ user_id, date, all_taken, ... })
    # So it is a daily summary.
    # But `markTaken` also does:
    # sb.from('medicines').update({ status: 'taken' }).eq('id', id)
    # AND `safeMutation('adherence_log'...)`
    
    # To support the previous granular log if needed, we'd need another table. 
    # But for this migration, let's match the Frontend's `adherence_log` expectation exactly.
    
    # Summary table, no direct link to single medicine
