"""
MedGuard — Medicines Router
GET /api/medicines/{user_id}  →  List medicines
POST /api/medicines           →  Add medicine
PATCH /api/medicines/{id}     →  Update medicine (status, etc.)
DELETE /api/medicines/{id}    →  Delete medicine
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Medicine
from app.schemas import MedicineResponse, MedicineCreate, MedicineUpdate

router = APIRouter(prefix="/api", tags=["Medicines"])


@router.get("/medicines/{user_id}", response_model=List[MedicineResponse])
def get_medicines(user_id: str, db: Session = Depends(get_db)):
    medicines = db.query(Medicine).filter(Medicine.user_id == user_id).all()
    return medicines


@router.post("/medicines", response_model=MedicineResponse)
def create_medicine(data: MedicineCreate, db: Session = Depends(get_db)):
    medicine = Medicine(
        user_id=data.user_id,
        name=data.name,
        dosage=data.dosage,
        is_antibiotic=data.is_antibiotic,
        status=data.status,
        urgent=data.urgent,
        times=data.times
    )
    db.add(medicine)
    db.commit()
    db.refresh(medicine)
    return medicine


@router.patch("/medicines/{medicine_id}", response_model=MedicineResponse)
def update_medicine(medicine_id: int, data: MedicineUpdate, db: Session = Depends(get_db)):
    medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    
    # Update fields provided
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(medicine, key, value)
    
    db.commit()
    db.refresh(medicine)
    return medicine


@router.delete("/medicines/{medicine_id}")
def delete_medicine(medicine_id: int, db: Session = Depends(get_db)):
    medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    
    db.delete(medicine)
    db.commit()
    return {"message": "Medicine deleted successfully"}
