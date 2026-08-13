from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.config.database import get_db
from app.models.email_draft import DraftEmailResponse
from app.services.draft_email_service import DraftEmailService

router = APIRouter(
    prefix="/draft-email",
    tags=["Draft Email"],
)


@router.post(
        "/{rfq_id}/{quotation_id}/{approval_id}",
        response_model=DraftEmailResponse,
        )
def generate_draft_email(
    rfq_id: int,
    quotation_id: int,
    approval_id: int,
    db: Session = Depends(get_db),
):

    service = DraftEmailService(db)

    try:
        return service.generate(rfq_id=rfq_id)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error