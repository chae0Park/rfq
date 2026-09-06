from app.services.market_benchmark_loader import MarketBenchmarkLoader
from app.services.exchange_rate_loader import ExchangeRateLoader


class MarketPriceReviewService:

    def __init__(self):
        self.benchmark_loader = MarketBenchmarkLoader()
        self.exchange_rate_loader = ExchangeRateLoader()

    def review(
        self,
        price: float,
        currency: str,
        country: str,
        sample_size: int,
        loi: int,
        ir: int,
        programming_required: bool,
        translation_required: bool,
        rush: bool,
    ):
        benchmark = self.benchmark_loader.find_benchmark(
            country=country,
            sample_size=sample_size,
            loi=loi,
            ir=ir,
            programming_required=programming_required,
            translation_required=translation_required,
            rush=rush,
        )

        if benchmark is None:
            return {
                "status": "NO_BENCHMARK",
                "price": price,
            }

        low = benchmark["benchmark_low_usd"]
        high = benchmark["benchmark_high_usd"]

        rate = self.exchange_rate_loader.get_rate(currency)
        price_usd = price / rate

        if price_usd < low:
            status = "BELOW_BENCHMARK"
        elif price_usd > high:
            status = "ABOVE_BENCHMARK"
        else:
            status = "WITHIN_BENCHMARK"

        return {
            "status": status,
            "price": price,
            "benchmark_low": low,
            "benchmark_high": high,
            "source_type": benchmark["source_type"],
        }