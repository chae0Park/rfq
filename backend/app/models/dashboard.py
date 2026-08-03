from pydantic import BaseModel


class QuotationSummaryResponse(BaseModel):
    base_cost: float
    sample_cost: float
    programming_fee: float
    translation_fee: float
    pm_fee: float
    margin: float
    rush_fee: float
    client_discount: float
    total_cost: float
    currency: str


class RFQDetailResponse(BaseModel):
    id: int
    project_name: str | None
    client_name: str | None
    client_email: str | None
    client: str | None
    country: str | None
    sample_size: int | None
    methodology: str | None
    timeline: str | None
    status: str

    quotation: QuotationSummaryResponse | None



class RFQListItemResponse(BaseModel):
    id: int
    client_name: str | None
    client_email: str | None
    project_name: str | None
    country: str | None
    sample_size: int | None
    status: str

    total_cost: float | None = None
    currency: str | None = None