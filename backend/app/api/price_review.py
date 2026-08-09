from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.db.repositories.rfq_repository import RFQRepository
from app.db.repositories.quotation_repository import QuotationRepository
from app.db.repositories.price_review_repository import PriceReviewRepository
from app.services.price_review_service import PriceReviewService

from app.models.rfq import RFQExtraction
from app.models.quotation import QuotationResult
from app.models.price_review import PriceReviewResult


router = APIRouter(
    prefix="/price-review",
    tags=["Price Review"],
)


@router.post(
    "/{rfq_id}",
    response_model=PriceReviewResult,
    summary="Review quotation price",
)
def review_price(
    rfq_id: int,
    db: Session = Depends(get_db),
) -> PriceReviewResult:

    # 1. RFQ 조회
    rfq_repository = RFQRepository(db)
    rfq_db = rfq_repository.get_by_id(rfq_id)

    if rfq_db is None:
        raise HTTPException(
            status_code=404,
            detail="RFQ not found",
        )

    # 2. Quotation 조회
    quotation_repository = QuotationRepository(db)
    quotation_db = quotation_repository.get_by_rfq_id(rfq_id)

    if quotation_db is None:
        raise HTTPException(
            status_code=404,
            detail="Quotation not found",
        )

    # 3. DB RFQ → PriceReviewService 입력 모델
    rfq = RFQExtraction(
        project_name=rfq_db.project_name,
        country=rfq_db.country,
        countries=rfq_db.countries,
        sample_size=rfq_db.sample_size,
        loi=rfq_db.loi,
        ir=rfq_db.ir,
        methodology=rfq_db.methodology,
        timeline=rfq_db.timeline,
        languages=rfq_db.languages,
        programming_required=rfq_db.programming_required,
        translation_required=rfq_db.translation_required,
        overlay_required=rfq_db.overlay_required,
        rush=rfq_db.rush,
        client_tier=rfq_db.client_tier,
        currency=rfq_db.currency,
    )

    # 4. DB Quotation → PriceReviewService 입력 모델
    quotation = QuotationResult(
        countries=rfq_db.countries or [rfq_db.country],
        currency=quotation_db.currency,
        total_cost=quotation_db.total_cost,
        breakdown={
            "base_cost": quotation_db.base_cost,
            "sample_cost": quotation_db.sample_cost,
            "loi_multiplier": 1.0,
            "ir_multiplier": 1.0,
            "programming_fee": quotation_db.programming_fee,
            "translation_fee": quotation_db.translation_fee,
            "pm_fee": quotation_db.pm_fee,
            "rush_fee": quotation_db.rush_fee,
            "margin": quotation_db.margin,
            "client_discount": quotation_db.client_discount,
        },
    )

    # 5. GPT Price Review
    service = PriceReviewService()

    result = service.review(
        rfq=rfq,
        quotation=quotation,
    )

    # 6. 결과 DB 저장
    review_repository = PriceReviewRepository(db)

    review_repository.create(
        rfq_id=rfq_id,
        quotation_id=quotation_db.id,
        result=result,
    )

    return result