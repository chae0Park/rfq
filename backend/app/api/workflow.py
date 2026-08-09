from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.db.repositories.rfq_repository import RFQRepository


router = APIRouter(
    prefix="/workflow",
    tags=["Workflow"],
)


class ResumeUrlRequest(BaseModel):
    resume_url: str


@router.post("/rfqs/{rfq_id}/resume-url")
def save_resume_url(
    rfq_id: int,
    request: ResumeUrlRequest,
    db: Session = Depends(get_db),
):
    repository = RFQRepository(db)

    rfq = repository.get_by_id(rfq_id)

    if rfq is None:
        raise HTTPException(
            status_code=404,
            detail="RFQ not found",
        )

    rfq.n8n_resume_url = request.resume_url

    db.commit()
    db.refresh(rfq)

    return {
        "rfq_id": rfq.id,
        "resume_url_saved": True,
    }