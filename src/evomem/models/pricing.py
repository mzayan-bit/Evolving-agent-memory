"""Optional post-run repricing, deliberately absent from repair and budget logic."""

from typing import Any

from evomem.models.client import ModelResponse


def estimate_usd(response: ModelResponse, prices: dict[str, Any]) -> float | None:
    if (
        response.identity.provider != prices["provider"]
        or response.identity.model != prices["model"]
    ):
        raise ValueError("Price/model mismatch")
    if response.identity.provider != "anthropic":
        return None  # Local hardware cost is unknown, not zero.
    usage = response.raw_usage
    base = usage.get("input_tokens")
    output = usage.get("output_tokens")
    read = usage.get("cache_read_input_tokens", 0)
    write = usage.get("cache_creation_input_tokens", 0)
    if any(type(v) is not int or v < 0 for v in (base, output, read, write)):
        return None
    detail = usage.get("cache_creation") or {}
    short = detail.get("ephemeral_5m_input_tokens", 0)
    long = detail.get("ephemeral_1h_input_tokens", 0)
    if write and short + long != write:
        return None  # Cannot guess cache write TTL.
    return float(
        (
            base * prices["input_rate"]
            + output * prices["output_rate"]
            + read * prices["cached_input_rate"]
            + short * prices["cache_write_5m_rate"]
            + long * prices["cache_write_1h_rate"]
        )
        / prices["per_tokens"]
    )
