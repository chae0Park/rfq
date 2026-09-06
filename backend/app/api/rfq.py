from fastapi import APIRouter, Depends, HTTPException

from app.models.request import RFQRequest
from app.models.result import RFQExtractionResult
# from app.services.extractor import RFQExtractor

from sqlalchemy.orm import Session

from app.config.database import get_db
from fastapi import Depends

from app.services.rfq_service import RFQService


router = APIRouter(
    prefix="/rfq",
    tags=["RFQ"],
)



@router.post(
    "/extract",
    response_model=RFQExtractionResult,
    summary="Extract RFQ information from an email",
)
def extract_rfq(
    request: RFQRequest,
    db: Session = Depends(get_db),
) -> RFQExtractionResult:

    service = RFQService(db)

    return service.process_email(request)

@router.post(
    "/{rfq_id}/waiting-for-client",
    summary="Mark RFQ as waiting for client clarification",
)
def mark_waiting_for_client(
    rfq_id: int,
    db: Session = Depends(get_db),
):
    service = RFQService(db)

    return service.mark_waiting_for_client(rfq_id)


@router.get(
    "/thread/{thread_id}",
    summary="Get RFQ by Gmail thread ID",
)
def get_rfq_by_thread(
    thread_id: str,
    db: Session = Depends(get_db),
):
    service = RFQService(db)

    rfq = service.get_by_thread_id(thread_id)

    if rfq is None:
        raise HTTPException(
            status_code=404,
            detail="RFQ not found for this Gmail thread",
        )

    return rfq