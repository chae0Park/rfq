from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.rfq import router as rfq_router
from app.api.dashboard import router as dashboard_router
from app.api.rfq import router as rfq_router
from app.api.quotation import router as quotation_router

from app.config.database import Base
from app.config.database import engine
from app.api import draft_email


app = FastAPI(
    title="RFQ AI",
    description="AI-powered RFQ extraction, quotation engine, GPT price review, and draft email generation.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rfq_router)
app.include_router(dashboard_router)
app.include_router(quotation_router)
app.include_router(draft_email.router)

@app.get("/", tags=["Health"])
def root():
    return {
        "message": "Welcome to RFQ Extraction API"
    }


@app.get("/health", tags=["Health"])
def health():
    return {
        "status": "ok"
    }

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {
        "message": "Welcome to RFQ AI API",
    }