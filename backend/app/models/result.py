from typing import List

from pydantic import BaseModel, Field

from app.models.rfq import RFQExtraction



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

