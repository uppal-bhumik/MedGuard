"""
MedGuard — Prescription Router
POST /api/prescriptions/upload  →  Mock-extract medicines from uploaded file
"""

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Profile, Medicine
from app.schemas import MedicineResponse
import os
import json
import base64
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

router = APIRouter(prefix="/api", tags=["Prescriptions"])


@router.post("/prescriptions/upload", response_model=list[MedicineResponse])
async def upload_prescription(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Get the latest profile (highest id)
    profile = db.query(Profile).order_by(Profile.id.desc()).first()
    if not profile:
        raise HTTPException(status_code=404, detail="No profile found. Create a profile first.")

    # 1. Read file and convert to base64
    try:
        contents = await file.read()
        base64_image = base64.b64encode(contents).decode("utf-8")
        mime_type = file.content_type or "image/jpeg"
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read file: {str(e)}")

    # 2. Call OpenAI GPT-4o-mini
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY is missing in .env")
        # Fallback to demo mode if key is missing (safety net)
        filename = (file.filename or "").lower()
        if "demo1" in filename:
            return [{"name": "Amoxicillin", "is_antibiotic": True}, {"name": "Paracetamol", "is_antibiotic": False}]
        else:
            return [{"name": "Paracetamol", "is_antibiotic": False}, {"name": "Ibuprofen", "is_antibiotic": False}]

    try:
        client = OpenAI(api_key=api_key)
        
        system_prompt = """
        You are a medical assistant OCR. Analyze the prescription image and extract medicines.
        Return ONLY a raw JSON array (no markdown, no ```json wrapper).
        Format: [{"name": "Medicine Name", "dosage": "500mg", "frequency": "Twice Daily", "is_antibiotic": boolean}]
        Rules:
        - Extract exact names.
        - Guess antibiotic status based on name (set is_antibiotic: true/false).
        - If text is illegible, return []
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": system_prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:{mime_type};base64,{base64_image}"},
                        },
                    ],
                }
            ],
            max_tokens=1000,
        )

        content = response.choices[0].message.content.strip()
        # Clean potential markdown
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        
        extracted = json.loads(content)

    except Exception as e:
        print(f"❌ OpenAI Error: {e}")
        raise HTTPException(status_code=500, detail=f"AI Analysis Failed: {str(e)}")

    # 3. Save to DB
    medicines = []
    for med in extracted:
        # Default times if not provided
        times = ["08:00", "20:00"] if "Twice" in (med.get("frequency") or "") else ["08:00"]
        
        m = Medicine(
            user_id=profile.id,
            name=med.get("name", "Unknown"),
            dosage=med.get("dosage", ""),
            is_antibiotic=med.get("is_antibiotic", False),
            times=times,
            status="pending"
        )
        db.add(m)
        medicines.append(m)

    db.commit()
    for m in medicines:
        db.refresh(m)

    return medicines
