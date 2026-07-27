from pathlib import Path

import pandas as pd


class BaseCostLoader:
    def __init__(self, csv_path: str = "data/base_cost.csv"):
        self.df = pd.read_csv(Path(csv_path))

    def get_base_cost(self, country: str) -> float:
        result = self.df.loc[
            self.df["country"].str.lower() == country.lower(),
            "base_cost_usd",
        ]

        if result.empty:
            raise ValueError(f"Base cost not found for '{country}'.")

        return float(result.iloc[0])