from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.rfq import router as rfq_router
from app.api.dashboard import router as dashboard_router
from app.api.quotation import router as quotation_router
from app.api.price_review import router as price_review_router
from app.api.workflow import router as workflow_router
from app.api import draft_email

from app.config.database import Base, engine



app = FastAPI(
    title="RFQ AI",
    description="AI-powered RFQ extraction, quotation engine, GPT price review, and draft email generation.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://rfq-lemon.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rfq_router)
app.include_router(dashboard_router)
app.include_router(quotation_router)
app.include_router(price_review_router)
app.include_router(draft_email.router)
app.include_router(workflow_router)

Base.metadata.create_all(bind=engine)

@app.get("/", tags=["Health"])
def root():
    return {
        "message": "Welcome to RFQ AI API"
    }


@app.get("/health", tags=["Health"])
def health():
    return {
        "status": "ok"
    }

