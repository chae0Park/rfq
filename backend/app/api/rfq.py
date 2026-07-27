from fastapi import APIRouter

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