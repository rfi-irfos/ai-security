# License Map — rfi-irfos/ai-security Monorepo

Each component retains its original upstream license. This file maps every directory in `tools/` to its upstream source, original license, and any required attribution notices.

## Apache 2.0 Components

| Tool | Upstream | License | Attribution Required |
|------|----------|---------|---------------------|
| tools/garak | NVIDIA/garak | Apache 2.0 | Yes – retain NOTICE, copyright headers |
| tools/FuzzyAI | CyberArk/FuzzyAI | Apache 2.0 | Yes – retain NOTICES.txt, copyright headers |
| tools/AIGoat | AISecurityConsortium/AIGoat | Apache 2.0 | Yes – retain NOTICE, copyright |
| tools/spikee | ReversecLabs/spikee | MIT (see below) | Yes – retain LICENSE.txt, copyright |
| tools/spike-skill | ReversecLabs/spike-skill | MIT | Yes |
| tools/llama-3-prompt-injection-fine-tuning | ReversecLabs/llama-3-prompt-injection-fine-tuning | MIT | Yes |
| tools/damn-vulnerable-llm-agent | ReversecLabs/damn-vulnerable-llm-agent | Apache 2.0 | Yes |
| tools/llm-vulnerable-recruitment-app | ReversecLabs/llm-vulnerable-recruitment-app | Apache 2.0 | Yes |
| tools/llm-webmail | ReversecLabs/llm-webmail | MIT | Yes |
| tools/design-patterns-for-securing-llm-agents-code-samples | ReversecLabs/design-patterns-for-securing-llm-agents-code-samples | MIT | Yes |
| tools/2025-07-llm-noise-based-attacks-workspace | ReversecLabs/2025-07-llm-noise-based-attacks-workspace | MIT | Yes |
| tools/spikee-test-chatbot | ReversecLabs/spikee-test-chatbot | MIT | Yes |

## MIT Components

| Tool | Upstream | License | Attribution Required |
|------|----------|---------|---------------------|
| tools/llm-guard | ProtectAI/llm-guard | MIT | Yes |
| tools/agentdojo | eth-sri/agentdojo | MIT | Yes |
| tools/cryptex-oss | m4xx101/cryptex-oss | MIT | Yes |
| tools/PIArena | sleeepeer/PIArena | MIT | Yes |
| tools/rebuff | ProtectAI/rebuff | Apache 2.0 | Yes – note discrepancy: repo says Apache 2.0 |
| tools/ps-fuzz | prompt-security/ps-fuzz | MIT (proprietary note in LICENSE) | Check LICENSE – may be source-available only |
| tools/spikee | ReversecLabs/spikee | MIT | Yes |

## GPL Components

| Tool | Upstream | License | Notes |
|------|----------|---------|-------|
| tools/promptmap | utkusen/promptmap | GPLv3 | Copyleft – derivative works must be GPL-compatible. Isolated in own directory; do not link with Apache/MIT code in same process. |

## No License / Unclear

| Tool | Upstream | Notes |
|------|----------|-------|
| tools/EvoSynth | dongdongunique/EvoSynth | No LICENSE file found. Treat as all-rights-reserved until verified. |

## Upstream Sources (canonical URLs)

- spikee: https://github.com/ReversecLabs/spikee
- garak: https://github.com/NVIDIA/garak
- FuzzyAI: https://github.com/cyberark/FuzzyAI
- promptmap: https://github.com/utkusen/promptmap
- ps-fuzz: https://github.com/prompt-security/ps-fuzz
- llm-guard: https://github.com/ProtectAI/llm-guard
- rebuff: https://github.com/protectai/rebuff
- agentdojo: https://github.com/eth-sri/agentdojo
- AIGoat: https://github.com/AISecurityConsortium/AIGoat
- EvoSynth: https://github.com/dongdongunique/EvoSynth
- cryptex-oss: https://github.com/m4xx101/cryptex-oss
- PIArena: https://github.com/sleeepeer/PIArena
- llama-3-prompt-injection-fine-tuning: https://github.com/ReversecLabs/llama-3-prompt-injection-fine-tuning
- damn-vulnerable-llm-agent: https://github.com/ReversecLabs/damn-vulnerable-llm-agent
- llm-vulnerable-recruitment-app: https://github.com/ReversecLabs/llm-vulnerable-recruitment-app
- llm-webmail: https://github.com/ReversecLabs/llm-webmail
- spike-skill: https://github.com/ReversecLabs/spike-skill
- design-patterns-for-securing-llm-agents-code-samples: https://github.com/ReversecLabs/design-patterns-for-securing-llm-agents-code-samples
- 2025-07-llm-noise-based-attacks-workspace: https://github.com/ReversecLabs/2025-07-llm-noise-based-attacks-workspace
- spikee-test-chatbot: https://github.com/ReversecLabs/spikee-test-chatbot

## Monorepo License (this repo)

This monorepo's assembly, structure, curation scripts, and any new code written for this repo are licensed under the MIT License (see `LICENSE` at repo root). The above does not override the original license of any included component.
