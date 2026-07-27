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