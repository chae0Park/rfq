from sqlalchemy.orm import Session

from app.models.rfq import RFQExtraction
from app.models.quotation import QuotationResult

from app.services.calculator import RFQCalculator
from app.db.repositories.quotation_repository import QuotationRepository


class QuotationService:

    def __init__(self, db: Session):
        self.calculator = RFQCalculator()
        self.repository = QuotationRepository(db)

    def generate(
        self,
        rfq_id: int,
        rfq: RFQExtraction,
    ):

        quotation = self.calculator.calculate(rfq)

        saved_quotation = self.repository.create(
            rfq_id=rfq_id,
            quotation=quotation,
        )

        return quotation, saved_quotation