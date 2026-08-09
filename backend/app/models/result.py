from typing import List
from typing import Optional

from pydantic import BaseModel, Field

from app.models.rfq import RFQExtraction
from app.models.quotation import QuotationResult


class RFQExtractionResult(BaseModel):

    rfq_id: int | None = None

    extracted_data: RFQExtraction = Field(
        description="Structured RFQ information extracted from the email."
    )

    missing_fields: List[str] = Field(
        default_factory=list
    )

    clarification_questions: List[str] = Field(
        default_factory=list
    )

    ready_for_quotation: bool

class PriceReviewResult(BaseModel):
    is_reasonable: bool
    confidence: str
    review: str
    suggestions: list[str]

class ApprovalResult(BaseModel):
    approved: bool
    approver: Optional[str] = None
    comments: Optional[str] = None

class DraftEmailResult(BaseModel):
    subject: str
    body: str

class RFQDashboardResult(BaseModel):
    rfq_id: str
    project_name: str | None = None
    client_name: str | None = None
    status: str
    quotation: QuotationResult
    price_review_status: str