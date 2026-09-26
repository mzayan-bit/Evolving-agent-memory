"""Public fictional engineering evidence. No hidden formal gold used in prompts."""

from evomem.model import InformationAccess, Memory, PolicyView, Revision, Status


def support_view() -> PolicyView:
    rows = [
        Memory(
            "a",
            "Only the Zorvia registry certifies permit K17. It certified K17.",
            "lab",
            kind="source",
            status=Status.SUPERSEDED,
            valid_until=1,
            origin_ids=("registry",),
        ),
        Memory(
            "a2",
            "The Zorvia registry withdrew permit K17 and certifies K29 now.",
            "lab",
            kind="source",
            valid_from=1,
            origin_ids=("registry",),
        ),
        Memory("n", "Zorvia holds permit K17.", "lab"),
        Memory(
            "b",
            "Independent Tovren lab directly certifies permit K17 for Zorvia.",
            "lab",
            kind="source",
            origin_ids=("lab",),
        ),
        Memory("alt", "Zorvia has at least one certification of K17.", "lab"),
        Memory(
            "c",
            "Velkin gate opens exactly when both blue and round. It is blue.",
            "lab",
            kind="source",
        ),
        Memory("d", "Velkin gate is round.", "lab", kind="source"),
        Memory("conj", "Velkin gate opens.", "lab"),
        Memory("e", "Zorvia paints its office violet.", "lab", kind="source"),
        Memory("assoc", "Zorvia is authorized to use protocol M83.", "lab"),
        Memory(
            "copy",
            "A copied bulletin repeats only registry a: Zorvia holds K17.",
            "lab",
            source_ids=("a",),
            origin_ids=("registry",),
        ),
    ]
    return PolicyView(
        1,
        tuple(rows),
        Revision(1, "a", rows[1], fault_cue="a"),
        (),
        (),
        (),
        InformationAccess(),
    )


def nonce_view(value: str = "K17") -> PolicyView:
    source = Memory("s", f"Project Zorvia uses protocol {value}.", "lab", kind="source")
    target = Memory("t", "Project Zorvia uses protocol K17.", "lab")
    unrelated = Memory("u", "Project Tovren uses protocol M83.", "lab", kind="source")
    other = Memory("v", "Project Tovren uses protocol M83.", "lab")
    return PolicyView(
        1,
        (source, target, unrelated, other),
        Revision(1, "s", source, fault_cue="s"),
        (),
        (),
        (),
        InformationAccess(),
    )
