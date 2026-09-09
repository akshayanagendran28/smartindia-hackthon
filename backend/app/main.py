import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.database.session import engine, Base, SessionLocal
from app.database.seed import seed_database

# Import routers
from app.routers import (
    auth,
    profile,
    schemes,
    matching,
    finance,
    documents,
    partners,
    banking,
    chat,
    notifications,
    admin,
    readiness,
    translate
)

# Initialize database schema
Base.metadata.create_all(bind=engine)

# Auto-seed verified schemes and initial channel partners on startup
db = SessionLocal()
try:
    seed_database(db)
finally:
    db.close()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Intelligent AI-Driven Scheme Discovery & Matching Platform for Smart India Hackathon 2026 (SIH26092)"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static Uploads Directory
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Register Routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(profile.router, prefix=settings.API_V1_STR)
app.include_router(schemes.router, prefix=settings.API_V1_STR)
app.include_router(matching.router, prefix=settings.API_V1_STR)
app.include_router(finance.router, prefix=settings.API_V1_STR)
app.include_router(documents.router, prefix=settings.API_V1_STR)
app.include_router(partners.router, prefix=settings.API_V1_STR)
app.include_router(banking.router, prefix=settings.API_V1_STR)
app.include_router(chat.router, prefix=settings.API_V1_STR)
app.include_router(notifications.router, prefix=settings.API_V1_STR)
app.include_router(admin.router, prefix=settings.API_V1_STR)
app.include_router(readiness.router, prefix=settings.API_V1_STR)
app.include_router(translate.router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "platform": "SCHEME SATHI",
        "tagline": "AI-Driven Scheme Matching for Marginalized Entrepreneurs",
        "problem_statement": "SIH26092",
        "version": settings.VERSION,
        "api_documentation": "/docs"
    }
