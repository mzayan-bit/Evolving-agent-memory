"""Protocol categories; semantic correctness is assigned only by an evaluator."""

from enum import StrEnum

from evomem.models.client import ModelCallError


class InferenceCategory(StrEnum):
    VALID_CORRECT_FORMAT = "VALID_CORRECT_FORMAT"
    VALID_WRONG_SEMANTICS = "VALID_WRONG_SEMANTICS"
    MALFORMED_OUTPUT = "MALFORMED_OUTPUT"
    UNKNOWN_TARGET_ID = "UNKNOWN_TARGET_ID"
    UNKNOWN_MEMBER_ID = "UNKNOWN_MEMBER_ID"
    MISSING_REQUIRED_FIELD = "MISSING_REQUIRED_FIELD"
    MISSING_TARGET = "MISSING_TARGET"
    DUPLICATE_RELATION = "DUPLICATE_RELATION"
    CONTRADICTORY_STRUCTURE = "CONTRADICTORY_STRUCTURE"
    MODEL_REFUSAL = "MODEL_REFUSAL"
    MODEL_TIMEOUT = "MODEL_TIMEOUT"
    MODEL_TRANSPORT_ERROR = "MODEL_TRANSPORT_ERROR"
    TRUNCATED_OUTPUT = "TRUNCATED_OUTPUT"
    BUDGET_EXHAUSTED = "BUDGET_EXHAUSTED"


class ProtocolError(ValueError):
    def __init__(self, category: InferenceCategory, message: str) -> None:
        super().__init__(message)
        self.category = category


class InferenceError(ModelCallError):
    def __init__(self, category: InferenceCategory, message: str) -> None:
        super().__init__(message)
        self.category = category
