from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.db.repositories.rfq_repository import RFQRepository
from app.models.approval import ApprovalRequest
from app.services.approval_service import ApprovalService

router = APIRouter(prefix="/approval", tags=["Approval"])


@router.post("/{rfq_id}")
def approve(
    rfq_id: int,
    request: ApprovalRequest,
    db: Session = Depends(get_db),
):
    rfq_repository = RFQRepository(db)
    rfq = rfq_repository.get_by_id(rfq_id)

    service = ApprovalService(db)

    return service.approve(
        rfq=rfq,
        quotation_id=request.quotation_id,
        request=request,
    )