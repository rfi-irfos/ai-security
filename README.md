# AI Security Evaluation Toolkit

Consolidated LLM red-teaming, prompt injection, and guardrail evaluation tools for RFI-IRFOS research.

## Quick Start

```bash
cd tools/spikee
python3 -m venv env
source env/bin/activate
pip install -e ".[all]"
spikee init
spikee generate --seed-folder seeds/cybersec-2026-01
spikee test --dataset datasets/cybersec-2026-01-full-prompt-dataset-*.jsonl \
            --target llm_provider \
            --target-options "openai/gpt-4o-mini"
spikee results analyze --result-file results/*.jsonl
```

See `tools/` for individual tool documentation.
See `reconcile_license_map.md` for original upstream licenses and attribution.
