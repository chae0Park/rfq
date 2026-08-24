from openai import OpenAI
import csv
import time
from pathlib import Path

from app.config.settings import settings
from app.models.request import RFQRequest
from app.models.rfq import RFQExtraction
from app.prompts.extraction import EXTRACTION_SYSTEM_PROMPT


class RFQExtractor:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.supported_countries = self._load_supported_countries()

    def _load_supported_countries(self) -> list[str]:
        countries = []

        with open(
            Path("data/base_cost.csv"),
            newline="",
            encoding="utf-8",
        ) as file:
            reader = csv.DictReader(file)

            for row in reader:
                countries.append(row["country"])

        return countries

    def extract(self, request: RFQRequest) -> RFQExtraction:
        country_list = "\n".join(
            f"- {country}"
            for country in self.supported_countries
        )

        system_prompt = f"""
{EXTRACTION_SYSTEM_PROMPT}

## Supported Pricing Countries

The following are the canonical country names supported by
the pricing system:

{country_list}

When a country mentioned in the email clearly corresponds to one
of these countries, return exactly the canonical name shown above.

Correct abbreviations, alternative names, and minor spelling mistakes
when the intended country is unambiguous.

If the country does not correspond to any supported country,
preserve the country stated by the client.
"""
        start_time = time.perf_counter()

        response = self.client.responses.parse(
            model=settings.OPENAI_MODEL,
            input=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": request.email_body,
                },
            ],
            text_format=RFQExtraction,
        )
        latency_ms = (time.perf_counter() - start_time) * 1000

        input_tokens = None
        output_tokens = None

        if response.usage:
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens


        return {
            "extraction": response.output_parsed,
            "latency_ms": latency_ms,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
        }