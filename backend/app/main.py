"""
MedGuard — FastAPI Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routes.profile import router as profile_router
from app.routes.prescription import router as prescription_router
from app.routes.medicines import router as medicines_router
from app.routes.adherence import router as adherence_router
from app.routes.risk import router as risk_router

# Create all tables on startup (safe for demo — idempotent)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MedGuard API",
    description="Medication adherence monitoring backend for elderly users",
    version="0.1.0",
)

# CORS — allow everything for demo / local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





# ── Routers ──────────────────────────────────────────────
app.include_router(profile_router)
app.include_router(prescription_router)
app.include_router(medicines_router)
app.include_router(adherence_router)
app.include_router(risk_router)

# ── Static Files (Frontend) ──────────────────────────────
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Check if frontend build exists (for local production/deployment)
frontend_dist = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "frontend", "dist")

if os.path.exists(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

    @app.get("/")
    async def serve_spa_root():
        return FileResponse(os.path.join(frontend_dist, "index.html"))



    # Catch-all for React Router (SPA)
    @app.get("/{full_path:path}")
    async def serve_react_app(full_path: str):
        # API requests strictly separate
        if full_path.startswith("api/"):
            return {"error": "API route not found"}
        
        # Serve index.html for any other path
        return FileResponse(os.path.join(frontend_dist, "index.html"))

