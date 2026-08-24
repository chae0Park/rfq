from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx

from app.config.database import get_db
from app.models.approval import ApprovalRequest,ApprovalResponse
from app.models.dashboard import RFQDetailResponse, QuotationSummaryResponse, RFQListItemResponse, LLMCallLogResponse, LLMMonitoringSummaryResponse, RFQUpdateRequest

from app.services.quotation_service import QuotationService
from app.db.repositories.rfq_repository import RFQRepository
from app.db.repositories.quotation_repository import QuotationRepository
from app.db.models.rfq import RFQDB
from app.models.rfq import RFQExtraction

from app.services.approval_service import ApprovalService

from app.models.email_draft import DraftEmailResponse
from app.services.email_draft_service import EmailDraftService
from app.db.repositories.llm_call_log_repository import LLMCallLogRepository

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
        loi=rfq.loi,
        ir=rfq.ir,
        programming_required=rfq.programming_required,
        translation_required=rfq.translation_required,
        rush=rfq.rush,
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


@router.get(
    "/rfqs/{rfq_id}/llm-logs",
    response_model=list[LLMCallLogResponse],
)
def get_llm_logs(
    rfq_id: int,
    db: Session = Depends(get_db),
):
    rfq_repository = RFQRepository(db)

    rfq = rfq_repository.get_by_id(rfq_id)

    if rfq is None:
        raise HTTPException(
            status_code=404,
            detail="RFQ not found.",
        )

    llm_log_repository = LLMCallLogRepository(db)

    logs = llm_log_repository.get_by_rfq_id(rfq_id)

    return [
        LLMCallLogResponse(
            id=log.id,
            rfq_id=log.rfq_id,
            task_type=log.task_type,
            model=log.model,
            status=log.status,
            latency_ms=log.latency_ms,
            input_tokens=log.input_tokens,
            output_tokens=log.output_tokens,
            estimated_cost=log.estimated_cost,
            error_message=log.error_message,
        )
        for log in logs
    ]


@router.get(
    "/llm-logs",
    response_model=list[LLMCallLogResponse],
)
def get_all_llm_logs(
    db: Session = Depends(get_db),
):
    llm_log_repository = LLMCallLogRepository(db)

    logs = llm_log_repository.get_all()

    return [
        LLMCallLogResponse(
            id=log.id,
            rfq_id=log.rfq_id,
            task_type=log.task_type,
            model=log.model,
            status=log.status,
            latency_ms=log.latency_ms,
            input_tokens=log.input_tokens,
            output_tokens=log.output_tokens,
            estimated_cost=log.estimated_cost,
            error_message=log.error_message,
        )
        for log in logs
    ]


@router.get(
    "/llm-logs/summary",
    response_model=LLMMonitoringSummaryResponse,
)
def get_llm_monitoring_summary(
    db: Session = Depends(get_db),
):
    llm_log_repository = LLMCallLogRepository(db)

    logs = llm_log_repository.get_all()

    total_calls = len(logs)

    successful_calls = sum(
        1 for log in logs
        if log.status == "SUCCESS"
    )

    failed_calls = sum(
        1 for log in logs
        if log.status == "FAILED"
    )

    success_rate = (
        (successful_calls / total_calls) * 100
        if total_calls > 0
        else 0.0
    )

    total_input_tokens = sum(
        log.input_tokens or 0
        for log in logs
    )

    total_output_tokens = sum(
        log.output_tokens or 0
        for log in logs
    )

    total_tokens = (
        total_input_tokens
        + total_output_tokens
    )

    latency_values = [
        log.latency_ms
        for log in logs
        if log.latency_ms is not None
    ]

    average_latency_ms = (
        sum(latency_values) / len(latency_values)
        if latency_values
        else 0.0
    )

    total_estimated_cost = sum(
        log.estimated_cost or 0
        for log in logs
    )

    return LLMMonitoringSummaryResponse(
        total_calls=total_calls,
        successful_calls=successful_calls,
        failed_calls=failed_calls,
        success_rate=success_rate,
        total_input_tokens=total_input_tokens,
        total_output_tokens=total_output_tokens,
        total_tokens=total_tokens,
        average_latency_ms=average_latency_ms,
        total_estimated_cost=total_estimated_cost,
    )

@router.patch(
    "/rfqs/{rfq_id}",
    response_model=RFQDetailResponse,
    summary="Update RFQ fields",
)
def update_rfq(
    rfq_id: int,
    request: RFQUpdateRequest,
    db: Session = Depends(get_db),
):
    rfq_repository = RFQRepository(db)

    # 1. RFQ 조회
    rfq = rfq_repository.get_by_id(rfq_id)

    if rfq is None:
        raise HTTPException(
            status_code=404,
            detail="RFQ not found.",
        )

    # 2. 실제 요청에 포함된 필드만 가져오기
    update_data = request.model_dump(
        exclude_unset=True
    )

        # 3. RFQ 업데이트
    updated_rfq = rfq_repository.update(
        rfq=rfq,
        update_data=update_data,
    )

    # 4. 수정된 RFQ 데이터 → RFQExtraction 변환
    rfq_data = RFQExtraction(
        project_name=updated_rfq.project_name,
        country=updated_rfq.country,
        countries=updated_rfq.countries,
        sample_size=updated_rfq.sample_size,
        loi=int(updated_rfq.loi) if updated_rfq.loi is not None else None,
        ir=int(updated_rfq.ir) if updated_rfq.ir is not None else None,
        methodology=updated_rfq.methodology,
        timeline=updated_rfq.timeline,
        languages=updated_rfq.languages,
        programming_required=updated_rfq.programming_required,
        translation_required=updated_rfq.translation_required,
        overlay_required=updated_rfq.overlay_required,
        rush=updated_rfq.rush,
        client_tier=updated_rfq.client_tier,
        currency=updated_rfq.currency,
        client=updated_rfq.client,
    )

    # 5. 수정된 RFQ 기준으로 quotation 재계산
    quotation_service = QuotationService(db)

    try:
        quotation, saved_quotation = quotation_service.recalculate(
            rfq_id=rfq_id,
            rfq=rfq_data,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    # 6. 재계산된 quotation response 생성
    quotation_response = QuotationSummaryResponse(
        base_cost=saved_quotation.base_cost,
        sample_cost=saved_quotation.sample_cost,
        programming_fee=saved_quotation.programming_fee,
        translation_fee=saved_quotation.translation_fee,
        pm_fee=saved_quotation.pm_fee,
        margin=saved_quotation.margin,
        rush_fee=saved_quotation.rush_fee,
        client_discount=saved_quotation.client_discount,
        total_cost=saved_quotation.total_cost,
        currency=saved_quotation.currency,
    )

    # 7. 수정된 RFQ + 재계산된 quotation 반환
    return RFQDetailResponse(
    id=updated_rfq.id,
    project_name=updated_rfq.project_name,
    client_name=updated_rfq.client_name,
    client_email=updated_rfq.client_email,
    client=updated_rfq.client,

    country=updated_rfq.country,
    sample_size=updated_rfq.sample_size,

    loi=updated_rfq.loi,
    ir=updated_rfq.ir,
    programming_required=updated_rfq.programming_required,
    translation_required=updated_rfq.translation_required,
    rush=updated_rfq.rush,

    methodology=updated_rfq.methodology,
    timeline=updated_rfq.timeline,
    status=updated_rfq.status,

    quotation=quotation_response,
)