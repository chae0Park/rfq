from app.db.models.quotation import QuotationDB
from app.models.quotation import QuotationResult


class QuotationMapper:

    @staticmethod
    def to_db(
        rfq_id: int,
        quotation: QuotationResult,
    ) -> QuotationDB:

        breakdown = quotation.breakdown

        return QuotationDB(
            rfq_id=rfq_id,
            base_cost=breakdown.base_cost,
            sample_cost=breakdown.sample_cost,
            programming_fee=breakdown.programming_fee,
            translation_fee=breakdown.translation_fee,
            pm_fee=breakdown.pm_fee,
            margin=breakdown.margin,
            rush_fee=breakdown.rush_fee,
            client_discount=breakdown.client_discount,
            total_cost=quotation.total_cost,
            currency=quotation.currency,
        )