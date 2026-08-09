from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.db.models.rfq import RFQDB
from app.models.rfq import RFQExtraction
from app.services.calculator import RFQCalculator


router = APIRouter(
    prefix="/quotation",
    tags=["Quotation"],
)


@router.post("/{rfq_id}")
def create_quotation(
    rfq_id: int,
    db: Session = Depends(get_db),
):
    # 1. DB에서 RFQ 조회
    rfq_db = db.get(RFQDB, rfq_id)

    if rfq_db is None:
        raise HTTPException(
            status_code=404,
            detail="RFQ not found",
        )

    # 2. 견적 계산 가능한 RFQ인지 확인
    if not rfq_db.ready_for_quotation:
        raise HTTPException(
            status_code=400,
            detail="RFQ is not ready for quotation",
        )

    # 3. DB 데이터 → Calculator용 RFQExtraction
    rfq = RFQExtraction(
        project_name=rfq_db.project_name,
        country=rfq_db.country,
        countries=rfq_db.countries,
        sample_size=rfq_db.sample_size,
        loi=int(rfq_db.loi) if rfq_db.loi is not None else None,
        ir=int(rfq_db.ir) if rfq_db.ir is not None else None,
        methodology=rfq_db.methodology,
        timeline=rfq_db.timeline,
        languages=rfq_db.languages,
        programming_required=rfq_db.programming_required,
        translation_required=rfq_db.translation_required,
        overlay_required=rfq_db.overlay_required,
        rush=rfq_db.rush,
        client_tier=rfq_db.client_tier,
        currency=rfq_db.currency,
        client=rfq_db.client,
    )

    # 4. 기존 Calculator 실행
    calculator = RFQCalculator()

    try:
        result = calculator.calculate(rfq)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    # 5. 계산 결과 반환
    return {
        "rfq_id": rfq_id,
        **result.model_dump(),
    }