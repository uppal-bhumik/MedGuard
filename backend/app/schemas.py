"""
MedGuard — Pydantic Schemas (request / response)
"""

from datetime import datetime
from typing import List, Optional, Any
from pydantic import BaseModel


# ── Profile ──────────────────────────────────────────────

class ProfileCreate(BaseModel):
    id: str  # User ID from Auth provider (UUID)
    full_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    email: Optional[str] = None  # Frontend might send email, handy to have


class ProfileResponse(BaseModel):
    id: str
    full_name: Optional[str]
    age: Optional[int]
    gender: Optional[str]
    is_senior: bool
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Medicine ─────────────────────────────────────────────

class MedicineCreate(BaseModel):
    user_id: str
    name: str
    dosage: Optional[str] = None
    is_antibiotic: bool = False
    status: str = "pending"
    urgent: bool = False
    times: List[str] = []  # ["08:00", "20:00"]


class MedicineUpdate(BaseModel):
    name: Optional[str] = None
    dosage: Optional[str] = None
    status: Optional[str] = None
    urgent: Optional[bool] = None
    times: Optional[List[str]] = None


class MedicineResponse(BaseModel):
    id: int
    user_id: str
    name: str
    dosage: Optional[str]
    is_antibiotic: bool
    status: str
    urgent: bool
    times: Any  # JSON/List
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Dose / Adherence ────────────────────────────────────

class AdherenceLogCreate(BaseModel):
    user_id: str
    date: str
    all_taken: bool
    total_meds: int
    taken_meds: int


class AdherenceLogResponse(BaseModel):
    id: int
    user_id: str
    date: str
    all_taken: bool
    total_meds: int
    taken_meds: int
    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}


# ── Risk ─────────────────────────────────────────────────

class RiskResponse(BaseModel):
    user_id: str
    total_doses: int
    missed_doses: int
    risk_level: str  # "Low" | "Medium" | "High"
