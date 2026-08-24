from sqlalchemy.orm import Session

from app.db.mappers.quotation_mapper import QuotationMapper
from app.db.models.quotation import QuotationDB
from app.models.quotation import QuotationResult


class QuotationRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        rfq_id: int,
        quotation: QuotationResult,
    ) -> QuotationDB:

        quotation_db = QuotationMapper.to_db(
            rfq_id=rfq_id,
            quotation=quotation,
        )

        self.db.add(quotation_db)
        self.db.commit()
        self.db.refresh(quotation_db)

        return quotation_db
    

    def get_by_id(
        self,
        quotation_id: int,
    ) -> QuotationDB:

        return (
            self.db.query(QuotationDB)
            .filter(QuotationDB.id == quotation_id)
            .first()
        )

    # dashboard에서 승인 된 quotation을 가져오기 위해 추가
    def get_by_rfq_id(
        self,
        rfq_id: int,
    ) -> QuotationDB:

        return (
            self.db.query(QuotationDB)
            .filter(QuotationDB.rfq_id == rfq_id)
            .first()
        )

    def update(
        self,
        quotation_db: QuotationDB,
        quotation: QuotationResult,
    ) -> QuotationDB:

        updated_data = QuotationMapper.to_db(
            rfq_id=quotation_db.rfq_id,
            quotation=quotation,
        )

        quotation_db.base_cost = updated_data.base_cost
        quotation_db.sample_cost = updated_data.sample_cost
        quotation_db.programming_fee = updated_data.programming_fee
        quotation_db.translation_fee = updated_data.translation_fee
        quotation_db.pm_fee = updated_data.pm_fee
        quotation_db.margin = updated_data.margin
        quotation_db.rush_fee = updated_data.rush_fee
        quotation_db.client_discount = updated_data.client_discount
        quotation_db.total_cost = updated_data.total_cost
        quotation_db.currency = updated_data.currency

        self.db.commit()
        self.db.refresh(quotation_db)

        return quotation_db