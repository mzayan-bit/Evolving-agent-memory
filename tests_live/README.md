# Opt-in engineering validation

Default `uv run pytest` collects only `tests/`. Even explicit `pytest tests_live`
skips every test unless `EVOMEM_RUN_LIVE_TESTS=1`. Provider tests additionally
require `EVOMEM_RUN_PAID_TESTS=1` and configured credentials/server. No test reads
human annotation packets. The provider runner permits at most 8 calls: one basic
call and up to seven further calls across five support cases in one batch,
two B10 queries, two B8 generations and one readout, including at most one B5
schema retry. A rejected reservation and a cache hit do not dispatch.

Use an isolated Python 3.11 environment. The exact local embedding runtime is
archived in `research/resources/runtime/embedding-macos-arm64-python311.txt`.
Prepare only small public assets explicitly:

```sh
uv venv --python 3.11 ../g1-live-env
uv pip install --python ../g1-live-env/bin/python -r research/resources/runtime/embedding-macos-arm64-python311.txt
../g1-live-env/bin/python scripts/prepare_live_assets.py --cache-root ../g1-model-cache
```

Run local validation with an absolute HF_HOME pointing at that cache, and a fresh
output directory. Loading itself is offline; no implicit model download occurs:

```sh
EVOMEM_RUN_LIVE_TESTS=1 HF_HUB_OFFLINE=1 HF_HOME=/absolute/path/g1-model-cache PYTHONPATH=src ../g1-live-env/bin/python -m evomem.experiment.live_validation --component embedding --output results/unique-embedding
EVOMEM_RUN_LIVE_TESTS=1 HF_HUB_OFFLINE=1 HF_HOME=/absolute/path/g1-model-cache PYTHONPATH=src ../g1-live-env/bin/python -m evomem.experiment.live_validation --component tokenizer --output results/unique-tokenizer
```

For a configured authorized provider, select `anthropic` or `vllm`, add
`EVOMEM_RUN_PAID_TESTS=1`, and use the project environment. The tests_live pytest
suite calls the same functions and saves manifests in its temporary directories;
use the runner for retained artifacts. Do not run the suite repeatedly to collect
quality scores. A tokenizer PASS is not Qwen generation PASS; model-weight loading
is never attempted by the tokenizer check. The scripts do not automatically
provision servers, convert quantization or replace models.
