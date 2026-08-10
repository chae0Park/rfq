from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx

from app.config.database import get_db
from app.models.approval import ApprovalRequest,ApprovalResponse
from app.models.dashboard import RFQDetailResponse, QuotationSummaryResponse, RFQListItemResponse

from app.db.repositories.rfq_repository import RFQRepository
from app.db.repositories.quotation_repository import QuotationRepository
from app.db.models.rfq import RFQDB

from app.services.approval_service import ApprovalService


from app.config.database import get_db
from app.models.email_draft import DraftEmailResponse
from app.services.email_draft_service import EmailDraftService


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/rfqs",
    response_model=list[RFQListItemResponse],
)
def get_rfqs(
    db: Session = Depends(get_db),
):
    rfq_repository = RFQRepository(db)
    quotation_repository = QuotationRepository(db)

    rfqs = rfq_repository.get_all()

    result = []

    for rfq in rfqs:

        quotation = quotation_repository.get_by_rfq_id(
            rfq.id
        )

        result.append(
            RFQListItemResponse(
                id=rfq.id,
                client_name=rfq.client_name,
                client_email=rfq.client_email,
                project_name=rfq.project_name,
                country=rfq.country,
                sample_size=rfq.sample_size,
                status=rfq.status.value,
                total_cost=quotation.total_cost if quotation else None,
                currency=quotation.currency if quotation else None,
            )
        )

    return result




@router.get(
    "/rfqs/{rfq_id}",
    response_model=RFQDetailResponse,
)
def get_rfq(
    rfq_id: int,
    db: Session = Depends(get_db),
):
    rfq_repository = RFQRepository(db)
    quotation_repository = QuotationRepository(db)

    rfq = rfq_repository.get_by_id(rfq_id)

    if rfq is None:
        raise HTTPException(
            status_code=404,
            detail="RFQ not found.",
        )

    quotation = quotation_repository.get_by_rfq_id(rfq.id)

    quotation_response = None

    if quotation:
        quotation_response = QuotationSummaryResponse(
            base_cost=quotation.base_cost,
            sample_cost=quotation.sample_cost,
            programming_fee=quotation.programming_fee,
            translation_fee=quotation.translation_fee,
            pm_fee=quotation.pm_fee,
            margin=quotation.margin,
            rush_fee=quotation.rush_fee,
            client_discount=quotation.client_discount,
            total_cost=quotation.total_cost,
            currency=quotation.currency,
        )

    return RFQDetailResponse(
        id=rfq.id,
        project_name=rfq.project_name,
        client_name=rfq.client_name,
        client_email=rfq.client_email,
        client=rfq.client,
        country=rfq.country,
        sample_size=rfq.sample_size,
        methodology=rfq.methodology,
        timeline=rfq.timeline,
        status=rfq.status.value,
        quotation=quotation_response,
    )


def resume_n8n_workflow(
    rfq: RFQDB,
    decision: str,
    approval_id: int,
    quotation_id: int,
):
    if not rfq.n8n_resume_url:
        return

    resume_url = rfq.n8n_resume_url.replace(
        "http://localhost:5678",
        "http://n8n:5678",
    )

    response = httpx.post(
        resume_url,
        json={
            "rfq_id": rfq.id,
            "quotation_id": quotation_id,
            "approval_id": approval_id,
            "decision": decision,
        },
        timeout=10.0,
    )

    response.raise_for_status()

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

    resume_n8n_workflow(
        rfq=rfq,
        decision="APPROVE",
        approval_id=approval.id,
        quotation_id=quotation.id,
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

    resume_n8n_workflow(
        rfq=rfq,
        decision="REJECT",
        approval_id=approval.id,
        quotation_id=quotation.id,
    )

    return ApprovalResponse(
        id=approval.id,
        rfq_id=approval.rfq_id,
        quotation_id=approval.quotation_id,
        decision=approval.decision,
        reviewer=approval.reviewer,
        comment=approval.comment,
    )


@router.post(
    "/rfqs/{rfq_id}/draft-email",
    response_model=DraftEmailResponse,
)
def generate_email_draft(
    rfq_id: int,
    db: Session = Depends(get_db),
):
    service = EmailDraftService(db)

    try:
        return service.generate(rfq_id)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error