> [!WARNING]
> **THIS PROJECT HAS BEEN ARCHIVED.**
> 
> This project and its associated models on [Hugging Face](https://huggingface.co/[REDACTED]) are no longer under active development or maintained.

# LLM Guard - The Security Toolkit for LLM Interactions

LLM Guard by [Protect AI](https://[REDACTED].com/llm-guard) is a comprehensive tool designed to fortify the security of Large Language Models (LLMs).

[**Documentation**](https://[REDACTED].github.io/llm-guard/) | [**Playground**](https://huggingface.co/spaces/[REDACTED]/llm-guard-playground) | [**Changelog**](https://[REDACTED].github.io/llm-guard/changelog/)

[![GitHub
stars](https://img.shields.io/github/stars/[REDACTED]/llm-guard.svg?style=social&label=Star&maxAge=2592000)](https://GitHub.com/[REDACTED]/llm-guard/stargazers/)
[![MIT license](https://img.shields.io/badge/license-MIT-brightgreen.svg)](http://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)]([URL_REDACTED]
[![PyPI - Python Version](https://img.shields.io/pypi/v/llm-guard)](https://pypi.org/project/llm-guard)
[![Downloads](https://static.pepy.tech/badge/llm-guard)](https://pepy.tech/project/llm-guard)
[![Downloads](https://static.pepy.tech/badge/llm-guard/month)](https://pepy.tech/project/llm-guard)

<ahref="[LINK_REDACTED]"><img src="[URL_REDACTED]" width="200" alt="Join Our Slack Community"></a>

## What is LLM Guard?

![LLM-Guard]([URL_REDACTED]

By offering sanitization, detection of harmful language, prevention of data leakage, and resistance against prompt
injection attacks, LLM-Guard ensures that your interactions with LLMs remain safe and secure.

## Installation

Begin your journey with LLM Guard by downloading the package:

```sh
pip install llm-guard
```

## Getting Started

**Important Notes**:

- LLM Guard is designed for easy integration and deployment in production environments. While it's ready to use
  out-of-the-box, please be informed that we're constantly improving and updating the repository.
- Base functionality requires a limited number of libraries. As you explore more advanced features, necessary libraries
  will be automatically installed.
- Ensure you're using Python version 3.9 or higher. Confirm with: `python --version`.
- Library installation issues? Consider upgrading pip: `python -m pip install --upgrade pip`.

**Examples**:

- Get started with [ChatGPT and LLM Guard](./examples/openai_api.py).
- Deploy LLM Guard as [API](https://[REDACTED].github.io/llm-guard/api/overview/)

## Supported scanners

### Prompt scanners

- [Anonymize](https://[REDACTED].github.io/llm-guard/input_scanners/anonymize/)
- [BanCode](./docs/input_scanners/ban_code.md)
- [BanCompetitors](https://[REDACTED].github.io/llm-guard/input_scanners/ban_competitors/)
- [BanSubstrings](https://[REDACTED].github.io/llm-guard/input_scanners/ban_substrings/)
- [BanTopics](https://[REDACTED].github.io/llm-guard/input_scanners/ban_topics/)
- [Code](https://[REDACTED].github.io/llm-guard/input_scanners/code/)
- [Gibberish](https://[REDACTED].github.io/llm-guard/input_scanners/gibberish/)
- [InvisibleText](https://[REDACTED].github.io/llm-guard/input_scanners/invisible_text/)
- [Language](https://[REDACTED].github.io/llm-guard/input_scanners/language/)
- [PromptInjection](https://[REDACTED].github.io/llm-guard/input_scanners/prompt_injection/)
- [Regex](https://[REDACTED].github.io/llm-guard/input_scanners/regex/)
- [Secrets](https://[REDACTED].github.io/llm-guard/input_scanners/secrets/)
- [Sentiment](https://[REDACTED].github.io/llm-guard/input_scanners/sentiment/)
- [TokenLimit](https://[REDACTED].github.io/llm-guard/input_scanners/token_limit/)
- [Toxicity](https://[REDACTED].github.io/llm-guard/input_scanners/toxicity/)

### Output scanners

- [BanCode](./docs/output_scanners/ban_code.md)
- [BanCompetitors](https://[REDACTED].github.io/llm-guard/output_scanners/ban_competitors/)
- [BanSubstrings](https://[REDACTED].github.io/llm-guard/output_scanners/ban_substrings/)
- [BanTopics](https://[REDACTED].github.io/llm-guard/output_scanners/ban_topics/)
- [Bias](https://[REDACTED].github.io/llm-guard/output_scanners/bias/)
- [Code](https://[REDACTED].github.io/llm-guard/output_scanners/code/)
- [Deanonymize](https://[REDACTED].github.io/llm-guard/output_scanners/deanonymize/)
- [JSON](https://[REDACTED].github.io/llm-guard/output_scanners/json/)
- [Language](https://[REDACTED].github.io/llm-guard/output_scanners/language/)
- [LanguageSame](https://[REDACTED].github.io/llm-guard/output_scanners/language_same/)
- [MaliciousURLs](https://[REDACTED].github.io/llm-guard/output_scanners/malicious_urls/)
- [NoRefusal](https://[REDACTED].github.io/llm-guard/output_scanners/no_refusal/)
- [ReadingTime](https://[REDACTED].github.io/llm-guard/output_scanners/reading_time/)
- [FactualConsistency](https://[REDACTED].github.io/llm-guard/output_scanners/factual_consistency/)
- [Gibberish](https://[REDACTED].github.io/llm-guard/output_scanners/gibberish/)
- [Regex](https://[REDACTED].github.io/llm-guard/output_scanners/regex/)
- [Relevance](https://[REDACTED].github.io/llm-guard/output_scanners/relevance/)
- [Sensitive](https://[REDACTED].github.io/llm-guard/output_scanners/sensitive/)
- [Sentiment](https://[REDACTED].github.io/llm-guard/output_scanners/sentiment/)
- [Toxicity](https://[REDACTED].github.io/llm-guard/output_scanners/toxicity/)
- [URLReachability](https://[REDACTED].github.io/llm-guard/output_scanners/url_reachability/)

## Community, Contributing, Docs & Support

LLM Guard is an open source solution.
We are committed to a transparent development process and highly appreciate any contributions.
Whether you are helping us fix bugs, propose new features, improve our documentation or spread the word,
we would love to have you as part of our community.

- Give us a ⭐️ github star ⭐️ on the top of this page to support what we're doing,
  it means a lot for open source projects!
- Read our
  [docs](https://[REDACTED].github.io/llm-guard/)
  for more info about how to use and customize LLM Guard, and for step-by-step tutorials.
- Post a [Github
  Issue]([URL_REDACTED] to submit a bug report, feature request, or suggest an improvement.
- To contribute to the package, check out our [contribution guidelines](CONTRIBUTING.md), and open a PR.

Join our Slack to give us feedback, connect with the maintainers and fellow users, ask questions,
get help for package usage or contributions, or engage in discussions about LLM security!

<ahref="[LINK_REDACTED]"><img src="[URL_REDACTED]" width="200" alt="Join Our Slack Community"></a>

### Production Support

We're eager to provide personalized assistance when deploying your LLM Guard to a production environment.

- [Send Email ✉️](mailto:community@[REDACTED].com)
