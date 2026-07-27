import csv
from pathlib import Path


class PanelCPILoader:
    def __init__(self, csv_path: str = "data/panel_cpi.csv"):
        self.panel_cpi = {}

        with open(Path(csv_path), newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                self.panel_cpi[row["country"].lower()] = float(row["panel_cpi"])

    def get_panel_cpi(self, country: str) -> float:
        result = self.panel_cpi.get(country.lower())

        if result is None:
            raise ValueError(f"Panel CPI not found for '{country}'.")

        return result