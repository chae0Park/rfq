from pydantic import BaseModel


class ApprovalRequest(BaseModel):
    quotation_id: int
    decision: str
    reviewer: str
    comment: str | None = None