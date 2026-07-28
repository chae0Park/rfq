from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.database import get_db
# from app.enums.rfq_status import RFQStatus
from app.models.approval import ApprovalRequest,ApprovalResponse

from app.db.repositories.rfq_repository import RFQRepository
from app.db.repositories.quotation_repository import QuotationRepository

from app.services.approval_service import ApprovalService

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("/rfqs")
def get_rfqs(
    db: Session = Depends(get_db),
):
    repository = RFQRepository(db)
    return repository.get_all()


@router.get("/rfqs/{rfq_id}")
def get_rfq(
    rfq_id: int,
    db: Session = Depends(get_db),
):
    repository = RFQRepository(db)

    rfq = repository.get_by_id(rfq_id)

    if rfq is None:
        raise HTTPException(
            status_code=404,
            detail="RFQ not found.",
        )

    return rfq


@router.post("/rfqs/{rfq_id}/approve", response_model=ApprovalResponse,)
def approve_rfq(
    rfq_id: int,
    request: ApprovalRequest,
    db: Session = Depends(get_db),
):

    rfq_repository = RFQRepository(db)
    quotation_repository = QuotationRepository(db)
    approval_service = ApprovalService(db)

    rfq = rfq_repository.get_by_id(rfq_id)

    if rfq is None:
        raise HTTPException(
            status_code=404,
            detail="RFQ not found.",
        )

    quotation = quotation_repository.get_by_rfq_id(rfq.id)

    if quotation is None:
        raise HTTPException(
            status_code=404,
            detail="Quotation not found.",
        )

    approval = approval_service.approve(
        rfq=rfq,
        quotation_id=quotation.id,
        request=request,
    )

    return ApprovalResponse(
        id=approval.id,
        rfq_id=approval.rfq_id,
        quotation_id=approval.quotation_id,
        decision=approval.decision,
        reviewer=approval.reviewer,
        comment=approval.comment,
    )


@router.post("/rfqs/{rfq_id}/reject", response_model=ApprovalResponse)
def reject_rfq(
    rfq_id: int,
    request: ApprovalRequest,
    db: Session = Depends(get_db),
):

    rfq_repository = RFQRepository(db)
    quotation_repository = QuotationRepository(db)
    approval_service = ApprovalService(db)

    rfq = rfq_repository.get_by_id(rfq_id)

    if rfq is None:
        raise HTTPException(
            status_code=404,
            detail="RFQ not found.",
        )

    quotation = quotation_repository.get_by_rfq_id(rfq.id)

    if quotation is None:
        raise HTTPException(
            status_code=404,
            detail="Quotation not found.",
        )

    approval = approval_service.approve(
        rfq=rfq,
        quotation_id=quotation.id,
        request=request,
    )

    return ApprovalResponse(
        id=approval.id,
        rfq_id=approval.rfq_id,
        quotation_id=approval.quotation_id,
        decision=approval.decision,
        reviewer=approval.reviewer,
        comment=approval.comment,
    )