"""Exact token-ID shape normalization; never a character-length token estimate."""

from collections.abc import Mapping


def token_ids(value: object) -> tuple[int, ...]:
    # Transformers releases may return BatchEncoding instead of the old flat list.
    if isinstance(value, Mapping):
        value = value.get("input_ids")
    if not isinstance(value, (list, tuple)) or any(
        type(v) is not int or v < 0 for v in value
    ):
        raise ValueError("Expected one unbatched sequence of exact token IDs")
    return tuple(value)
