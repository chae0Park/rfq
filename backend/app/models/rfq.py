from typing import Optional

from pydantic import BaseModel, Field


class RFQExtraction(BaseModel):
    project_name: Optional[str] = Field(
        default=None,
        description="Project name mentioned in the email."
    )

    country: Optional[str] = Field(
        default=None,
        description="Target country."
    )

    countries: list[str] | None = Field(
        default=None,
        description="List of countries included in a multi-country RFQ."
    )

    region: Optional[str] = Field(
        default=None,
        description="Target region or state."
    )

    city: Optional[str] = Field(
        default=None,
        description="Target city."
    )

    sample_size: Optional[int] = Field(
        default=None,
        description="Requested sample size."
    )

    target_audience: Optional[str] = Field(
        default=None,
        description="Target respondents."
    )

    gender: Optional[str] = Field(
        default=None,
        description="Target gender."
    )

    age: Optional[str] = Field(
        default=None,
        description="Target age range."
    )

    quota: Optional[str] = Field(
        default=None,
        description="Quota requirement."
    )

    timeline: Optional[str] = Field(
        default=None,
        description="Project timeline."
    )

    methodology: Optional[str] = Field(
        default=None,
        description="Research methodology."
    )

    translation_required: Optional[bool] = Field(
        default=None,
        description="Whether translation is required."
    )

    programming_required: Optional[bool] = Field(
        default=None,
        description="Whether survey programming is required."
    )

    overlay_required: Optional[bool] = Field(
        default=None,
        description="Whether data overlay is required."
    )

    project_scope: Optional[str] = Field(
        default=None,
        description="Full Service or Fieldwork Only."
    )

    loi: Optional[int] = Field(
        default=None,
        description="Expected Length of Interview (LOI) in minutes."
    )

    ir: Optional[int] = Field(
        default=None,
        description="Expected Incidence Rate (IR) percentage."
    )

    languages: Optional[list[str]] = Field(
        default=None,
        description="Survey languages required for the project."
    )

    client: Optional[str] = Field(
        default=None,
        description="Client requesting the quotation."
    )

    end_client: Optional[str] = Field(
        default=None,
        description="End client if explicitly mentioned."
    )

    additional_notes: Optional[str] = Field(
        default=None,
        description="Additional requirements or notes."
    )

    rush: bool | None = Field(
        default=False,
        description="Whether the project requires expedited delivery."
    )

    client_tier: str | None = Field(
        default="Standard",
        description="Client pricing tier."
    )

    currency: str | None = Field(
        default="USD",
        description="Requested quotation currency."
    )

