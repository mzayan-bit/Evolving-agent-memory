"""Start the pinned local deployment after verifying its weight checksum.

Run from repository root. Paths are relative to that root; no automatic downloads.
"""

import hashlib
import json
import os
import subprocess
from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    os.chdir(root)
    config = json.loads((root / "research/g1/qwen_local/deployment.json").read_text())
    command = config["server_command"]
    version = subprocess.run(
        [command[0], "--version"], capture_output=True, text=True, check=True
    )
    expected = "version: 9222 (" + config["backend_revision"][:9] + ")"
    if expected not in version.stdout + version.stderr:
        raise SystemExit("llama.cpp version mismatch; refusing to start")
    weights = Path(command[command.index("--model") + 1])
    checksum = hashlib.sha256()
    with weights.open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            checksum.update(block)
    if checksum.hexdigest() != config["gguf_sha256"]:
        raise SystemExit("Qwen weight checksum mismatch; refusing to start")
    os.execv(command[0], command)


if __name__ == "__main__":
    main()
