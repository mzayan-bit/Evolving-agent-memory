"""Engineering fixtures authored independently of the 30 annotation drafts."""

from dataclasses import replace

from evomem.evaluation import CheckpointGold, Gold, Probe
from evomem.model import Memory, Relation, Revision, Scenario, Status, Support


def fixture(name: str) -> tuple[Scenario, Gold]:
    if name not in FIXTURES:
        raise ValueError("Unknown engineering fixture")
    a = Memory(
        "s1", "production capacity four", "demo", kind="source", origin_ids=("o1",)
    )
    b = Memory("s2", "independent test four", "demo", kind="source", origin_ids=("o2",))
    c = Memory("b1", "production capacity four", "demo", source_ids=("s1",))
    u = Memory("b2", "production capacity four", "other", source_ids=("s2",))
    rules = [Support("j1", "b1", ("s1",)), Support("j2", "b2", ("s2",), scope="other")]
    if name == "alternative":
        rules.append(Support("j3", "b1", ("s2",), Relation.ALTERNATIVE))
    elif name == "conjunction":
        rules[0] = replace(
            rules[0], members=("s1", "s2"), relation=Relation.CONJUNCTIVE
        )
    elif name == "copies":
        b = replace(b, kind="belief", origin_ids=("o1",), source_ids=("s1",))
        rules.append(Support("j3", "s2", ("s1",), Relation.COPIED))
        rules.append(Support("j4", "b1", ("s2",), Relation.ALTERNATIVE))
    initial: tuple[Memory, ...] = (a, b, c, u)
    revisions = [
        Revision(
            1,
            "s1",
            Memory(
                "s3",
                "production capacity eight",
                "demo",
                valid_from=1,
                created_at_checkpoint=1,
                kind="source",
            ),
            fault_cue="s1",
        )
    ]
    affected = frozenset() if name == "alternative" else frozenset({"b1"})
    valid = frozenset({"b1", "b2"}) if name == "alternative" else frozenset({"b2"})
    if name == "copies":
        affected, valid = frozenset({"s2", "b1", "b2"}), frozenset()
    labels = [
        CheckpointGold(
            1,
            affected,
            valid,
            frozenset({"b1"}) if name == "alternative" else frozenset(),
        )
    ]
    probes = [
        Probe("q1", 1, "b1", c.content if name == "alternative" else None),
        Probe("q2", 1, "b2", None if name == "copies" else u.content),
        Probe("q3", 1, "b1", c.content, "historical_then", 0),
        Probe("q4", 1, "b1", c.content, "historical_now", 0),
    ]
    if name == "correction":
        revisions[0] = replace(revisions[0], kind="correction")
        probes[-1] = replace(probes[-1], expected=None)
    if name == "repeated":
        # Fixed propositions: returning to four legitimately reactivates b1.
        d = Memory("b3", "production capacity eight", "demo", status=Status.INACTIVE)
        initial += (d,)
        rules += [
            Support("j3", "b3", ("s3",), valid_from=1),
            Support("j4", "b1", ("s4",), valid_from=2),
        ]
        revisions.append(
            Revision(
                2,
                "s3",
                Memory(
                    "s4",
                    a.content,
                    "demo",
                    valid_from=2,
                    created_at_checkpoint=2,
                    kind="source",
                ),
                fault_cue="s3",
            )
        )
        labels[0] = replace(labels[0], valid=frozenset({"b2", "b3"}))
        labels.append(CheckpointGold(2, frozenset({"b3"}), frozenset({"b1", "b2"})))
        probes += [
            Probe("q5", 1, "b3", d.content),
            Probe("q6", 2, "b1", c.content),
            Probe("q7", 2, "b3", None),
            Probe("q8", 2, "b3", d.content, "historical_then", 1),
            Probe("q9", 2, "b3", d.content, "historical_now", 1),
        ]
    scenario = Scenario(
        name,
        name,
        "engineering-v1",
        initial,
        tuple(revisions),
        tuple(rules),
        tuple(rules),
    )
    return scenario, Gold(tuple(rules), tuple(labels), tuple(probes))


FIXTURES = (
    "necessary",
    "alternative",
    "conjunction",
    "semantic_bystander",
    "repeated",
    "copies",
    "correction",
)
