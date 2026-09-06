import csv
from pathlib import Path


class MarketBenchmarkLoader:

    def __init__(self):
        self.benchmarks = self._load_benchmarks()

    def _load_benchmarks(self):
        file_path = (
            Path(__file__).resolve().parents[2]
            / "data"
            / "market_benchmarks.csv"
        )

        benchmarks = []

        with open(
            file_path,
            newline="",
            encoding="utf-8",
        ) as file:
            reader = csv.DictReader(file)

            for row in reader:
                benchmarks.append({
                    "country": row["country"],
                    "sample_size_min": int(
                        row["sample_size_min"]
                    ),
                    "sample_size_max": int(
                        row["sample_size_max"]
                    ),
                    "loi_min": int(row["loi_min"]),
                    "loi_max": int(row["loi_max"]),
                    "ir_min": int(row["ir_min"]),
                    "ir_max": int(row["ir_max"]),
                    "programming_required":
                        row["programming_required"].lower()
                        == "true",
                    "translation_required":
                        row["translation_required"].lower()
                        == "true",
                    "rush":
                        row["rush"].lower()
                        == "true",
                    "benchmark_low_usd": float(
                        row["benchmark_low_usd"]
                    ),
                    "benchmark_high_usd": float(
                        row["benchmark_high_usd"]
                    ),
                    "source_type": row["source_type"],
                })

        return benchmarks

    def find_benchmark(
        self,
        country: str,
        sample_size: int,
        loi: int | None,
        ir: int | None,
        programming_required: bool,
        translation_required: bool,
        rush: bool,
    ):
        # LOI 또는 IR이 없으면
        # 정확한 market benchmark를 선택할 수 없음
        if loi is None or ir is None:
            return None

        for benchmark in self.benchmarks:
            if (
                benchmark["country"] == country
                and benchmark["sample_size_min"]
                <= sample_size
                <= benchmark["sample_size_max"]
                and benchmark["loi_min"]
                <= loi
                <= benchmark["loi_max"]
                and benchmark["ir_min"]
                <= ir
                <= benchmark["ir_max"]
                and benchmark["programming_required"]
                == programming_required
                and benchmark["translation_required"]
                == translation_required
                and benchmark["rush"] == rush
            ):
                return benchmark

        return None