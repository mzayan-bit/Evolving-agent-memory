"""Explicit selection + opt-in required; ordinary pytest never collects this folder."""

import os
from pathlib import Path

import pytest

from evomem.experiment.live_validation import embedding, provider, tokenizer

pytestmark = pytest.mark.skipif(
    os.environ.get("EVOMEM_RUN_LIVE_TESTS") != "1",
    reason="Explicit live opt-in required",
)


def test_embedding_live(tmp_path: Path) -> None:
    assert embedding(tmp_path / "embedding")["status"] == "PASS"


def test_qwen_tokenizer_live(tmp_path: Path) -> None:
    assert tokenizer(tmp_path / "tokenizer")["status"] == "PASS"


@pytest.mark.parametrize("family", ["anthropic", "vllm"])
def test_provider_live(family: str, tmp_path: Path) -> None:
    if os.environ.get("EVOMEM_RUN_PAID_TESTS") != "1":
        pytest.skip("Separate paid-call opt-in required")
    result = provider(tmp_path / family, family)
    if result["status"] == "SKIPPED":
        pytest.skip(result["details"]["reason"])
    assert result["status"] == "PASS"
