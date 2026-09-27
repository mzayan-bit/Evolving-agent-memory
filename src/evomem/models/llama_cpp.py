"""Local llama.cpp dialect of the existing Qwen HTTP adapter.

Weights and server remain external. No runtime dependency or implicit downloads.
"""

import json
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlsplit

from evomem.models.client import ModelRequest, QwenVLLMClient


@dataclass
class QwenLlamaCppClient(QwenVLLMClient):
    timeout: float = 600.0

    def __post_init__(self) -> None:
        url = urlsplit(self.base_url)
        if (
            self.identity.provider != "llama.cpp"
            or self.identity.model != "Qwen/Qwen3.5-9B"
            or not self.identity.version
            or not self.identity.deployment
        ):
            raise ValueError("Pinned Qwen llama.cpp deployment metadata required")
        if (
            url.scheme != "http"
            or url.hostname not in {"localhost", "127.0.0.1", "::1"}
            or url.username
            or url.password
            or url.query
            or url.fragment
            or url.path not in {"", "/"}
        ):
            raise ValueError("llama.cpp requires a local HTTP origin")

    def request_body(self, request: ModelRequest) -> dict[str, Any]:
        body = super().request_body(request)
        schema = body.pop("structured_outputs")["json"]
        # llama.cpp constrains decoding but does not expose the schema to the LLM.
        # Serialize the existing contract, without inventing fixture-specific hints.
        body["messages"][0]["content"] += (
            "\n\nRequired output JSON Schema:\n" + json.dumps(schema, sort_keys=True)
        )
        body.update(
            response_format={
                "type": "json_schema",
                "json_schema": {"name": "evomem", "strict": True, "schema": schema},
            },
            chat_template_kwargs={"enable_thinking": False},
            cache_prompt=False,
            seed=request.seed if request.seed is not None else 0,
            return_tokens=True,
        )
        return body
