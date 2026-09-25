"""Local component driver, NOT an official CUPMem benchmark reproduction."""

import argparse
import importlib
import json
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkout", type=Path, required=True)
    args = parser.parse_args()
    sys.path.insert(0, str(args.checkout.resolve()))
    store_module = importlib.import_module("cup_mem.store_layer")
    models = importlib.import_module("cup_mem.memory.models")
    store = store_module.ProfileStore()
    bucket, track = "Spatiotemporal_Context", "location(city)"
    delta = models.SessionDelta(
        "d1",
        "session_1",
        1,
        "2025-01-01",
        bucket,
        track,
        "Seattle",
        "explicit",
        ["c1"],
        0.9,
    )
    store.apply_update(
        delta, models.UpdateDecision("ADD", "initial"), timestamp="2025-01-01"
    )
    item = store.get_active_for_track(bucket, track)[0].item_id
    proposal = models.InvalidationProposal(
        "p2", "session_2", bucket, track, ["d2"], ["c2"], "new evidence", 0.8
    )
    store.apply_invalidation(
        proposal,
        models.UpdateDecision("INDIRECT_INVALIDATE", "new evidence", item),
        timestamp="2025-02-01",
    )
    assert len(store.get_active_for_track(bucket, track)) == 0
    assert len(store.get_stale_for_track(bucket, track)) == 1
    assert store.get_unknown_for_track(bucket, track).status == "UNKNOWN_CURRENT"
    print(
        json.dumps(
            {
                "checks": 3,
                "status": "passed",
                "scope": "component mechanics only; no API or inference",
            }
        )
    )


if __name__ == "__main__":
    main()
