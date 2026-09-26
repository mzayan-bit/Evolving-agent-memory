"""Explicit download of pinned small embedding weights and tokenizer-only Qwen files."""

import argparse
import os
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache-root", type=Path, required=True)
    args = parser.parse_args()
    os.environ["HF_HOME"] = str(args.cache_root.absolute())
    os.environ["HF_HUB_DISABLE_IMPLICIT_TOKEN"] = "1"
    from huggingface_hub import snapshot_download

    configurations = [
        (
            "sentence-transformers/all-MiniLM-L6-v2",
            "1110a243fdf4706b3f48f1d95db1a4f5529b4d41",
            [
                "config.json",
                "modules.json",
                "sentence_bert_config.json",
                "config_sentence_transformers.json",
                "tokenizer.json",
                "tokenizer_config.json",
                "special_tokens_map.json",
                "vocab.txt",
                "model.safetensors",
                "1_Pooling/config.json",
            ],
        ),
        (
            "Qwen/Qwen3.5-9B",
            "c202236235762e1c871ad0ccb60c8ee5ba337b9a",
            [
                "config.json",
                "tokenizer.json",
                "tokenizer_config.json",
                "chat_template.jinja",
                "special_tokens_map.json",
                "vocab.json",
                "merges.txt",
            ],
        ),
    ]
    for repo, revision, patterns in configurations:
        print(
            snapshot_download(
                repo, revision=revision, allow_patterns=patterns, token=False
            )
        )


if __name__ == "__main__":
    main()
