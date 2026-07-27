from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.db.repositories.approval_repository import ApprovalRepository
from app.db.repositories.quotation_repository import QuotationRepository
from app.db.repositories.rfq_repository import RFQRepository
from app.services.draft_email_service import DraftEmailService

router = APIRouter(
    prefix="/draft-email",
    tags=["Draft Email"],
)


@router.post("/{rfq_id}/{quotation_id}/{approval_id}")
def generate_draft_email(
    rfq_id: int,
    quotation_id: int,
    approval_id: int,
    db: Session = Depends(get_db),
):

    rfq = RFQRepository(db).get_by_id(rfq_id)

    quotation = QuotationRepository(db).get_by_id(
        quotation_id
    )

    approval = ApprovalRepository(db).get_by_id(
        approval_id
    )

    service = DraftEmailService(db)

    return service.generate(
        rfq=rfq,
        quotation=quotation,
        approval=approval,
    )