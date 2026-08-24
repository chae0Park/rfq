def calculate_llm_cost(
    input_tokens: int | None,
    output_tokens: int | None,
) -> float | None:

    if input_tokens is None or output_tokens is None:
        return None

    input_price_per_million = 0.40
    output_price_per_million = 1.60

    input_cost = (
        input_tokens / 1_000_000
    ) * input_price_per_million

    output_cost = (
        output_tokens / 1_000_000
    ) * output_price_per_million

    return input_cost + output_cost