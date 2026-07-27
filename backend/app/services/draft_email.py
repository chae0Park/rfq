from app.models.result import DraftEmailResult


class DraftEmailService:

    async def generate(
        self,
        rfq,
        quotation,
    ) -> DraftEmailResult:
        ...