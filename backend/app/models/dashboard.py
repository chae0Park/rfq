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

    loi: int | None
    ir: int | None
    programming_required: bool | None
    translation_required: bool | None
    rush: bool | None

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

class LLMCallLogResponse(BaseModel):
    id: int
    rfq_id: int | None
    task_type: str
    model: str
    status: str

    latency_ms: float | None
    input_tokens: int | None
    output_tokens: int | None
    estimated_cost: float | None
    error_message: str | None

class LLMMonitoringSummaryResponse(BaseModel):
    total_calls: int
    successful_calls: int
    failed_calls: int
    success_rate: float

    total_input_tokens: int
    total_output_tokens: int
    total_tokens: int

    average_latency_ms: float
    total_estimated_cost: float

# # All fields are optional to support partial updates via PATCH.
class RFQUpdateRequest(BaseModel):
    country: str | None = None
    sample_size: int | None = None
    loi: int | None = None
    ir: int | None = None

    methodology: str | None = None
    timeline: str | None = None

    programming_required: bool | None = None
    translation_required: bool | None = None
    rush: bool | None = None

    currency: str | None = None