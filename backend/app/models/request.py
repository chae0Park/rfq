from pydantic import BaseModel, Field


class RFQRequest(BaseModel):
    email: str = Field(
        ...,
        description="Raw client RFQ email content."
    )