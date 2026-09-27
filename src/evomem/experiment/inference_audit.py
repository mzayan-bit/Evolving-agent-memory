"""Evaluator-only structural comparison. Never imported by inference or repair."""

from evomem.model import Support


def structure(
    supports: tuple[Support, ...], variant: str, targets: set[str]
) -> list[tuple[str, tuple[str, ...]]]:
    """Declared audit: committed pairwise arcs vs sufficient AND/OR sets.

    This is an exact authored-structure comparison, not a language entailment
    oracle. Relation enum details remain in the raw structures in the receipt.
    """
    if variant == "B5a":
        return sorted(
            {
                (s.target, (m,))
                for s in supports
                if s.target in targets
                for m in s.members
            }
        )
    return sorted(
        {
            (s.target, tuple(sorted(s.members)))
            for s in supports
            if s.target in targets and s.sufficient
        }
    )


def compare(
    proposals: tuple[tuple[Support, float], ...],
    gold: tuple[Support, ...],
    variant: str,
    targets: set[str],
    threshold: float = 0.7,
) -> dict[str, object]:
    actual = structure(
        tuple(s for s, c in proposals if c >= threshold), variant, targets
    )
    expected = structure(gold, variant, targets)
    correct = actual == expected
    return {
        "gold_structure": expected,
        "model_structure": actual,
        "semantic_correct": correct,
        "category": "VALID_CORRECT_FORMAT" if correct else "VALID_WRONG_SEMANTICS",
        "semantic_scope": "Exact committed structure on declared engineering targets",
        "audited_targets": sorted(targets),
    }
