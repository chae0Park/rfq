import csv
from pathlib import Path


class TranslationFeeLoader:
    def __init__(self, csv_path: str = "data/translation_fee.csv"):
        self.fees = {}

        with open(Path(csv_path), newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                key = (
                    row["source_language"].lower(),
                    row["target_language"].lower(),
                )

                self.fees[key] = float(row["fee"])

    def get_fee(
        self,
        source_language: str,
        target_language: str,
    ) -> float:

        key = (
            source_language.lower(),
            target_language.lower(),
        )

        return self.fees.get(key, 0.0)