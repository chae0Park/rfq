import csv
from pathlib import Path


class ExchangeRateLoader:

    def __init__(self):
        self.rates = self._load_rates()

    def _load_rates(self):
        file_path = (
            Path(__file__).resolve().parents[2]
            / "data"
            / "exchange_rates.csv"
        )

        rates = {}

        with open(file_path, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                rates[row["currency"].upper()] = float(row["rate"])

        return rates

    def get_rate(self, currency: str) -> float:
        rate = self.rates.get(currency.upper())

        if rate is None:
            raise ValueError(f"Unsupported currency: {currency}")

        return rate