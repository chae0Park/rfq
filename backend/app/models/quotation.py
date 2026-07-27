from pydantic import BaseModel, Field


class CostBreakdown(BaseModel):
    base_cost: float = Field(
        description="Base cost determined by the target country."
    )

    sample_cost: float = Field(
        default=0,
        description="Additional cost based on sample size."
    )

    loi_multiplier: float = Field(
        default=1.0,
        description="Cost multiplier based on interview length."
    )

    ir_multiplier: float = Field(
        default=1.0,
        description="Cost multiplier based on incidence rate."
    )

    programming_fee: float = Field(
        default=0,
        description="Survey programming fee."
    )

    translation_fee: float = Field(
        default=0,
        description="Translation fee."
    )

    pm_fee: float = Field(
        default=0,
        description="Project management fee calculated from direct project costs."
    )

    margin: float = Field(
        default=0,
        description="Company profit margin."
    )

    rush_fee: float = Field(
        default=0,
        description="Additional fee for rush projects."
    )

    client_discount: float = Field(
        default=0,
        description="Discount applied based on client tier."
    )


class QuotationResult(BaseModel):
    # country: str
    countries: list[str]

    currency: str

    total_cost: float

    breakdown: CostBreakdown