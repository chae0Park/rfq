from pydantic import BaseModel


class ApprovalRequest(BaseModel):
    decision: Literal["APPROVE", "REJECT"]
    reviewer: str
    comment: str | None = None

class ApprovalResponse(BaseModel):
    id: int
    rfq_id: int
    quotation_id: int
    decision: str
    reviewer: str
    comment: str | None = None