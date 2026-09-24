# Spikee Test Chatbot

A minimal chatbot application designed for testing multi-turn targets in **[Spikee](https://spikee.ai)**.

This tool provides a simple interface to interact with various LLM providers (OpenAI, Anthropic, Gemini, Bedrock, TogetherAI) to facilitate prompt injection and security testing workflows.

## Features
- **Multi-LLM Support**: Configurable via `config.yaml`.
- **Chat History**: Persisted in a local SQLite database with sidebar management.
- **No Authentication**: Simplified for local testing usage.

## Setup

1. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment:**
   Copy the example environment file and add your API keys:
   ```bash
   cp .env.example .env
   # Edit .env with your keys (OPENAI_API_KEY, ANTHROPIC_API_KEY, etc.)
   ```

4. **Configure Models:**
   Edit `config.yaml` to add or remove specific models as needed.

## Running

Start the server using `uvicorn`:

```bash
uvicorn main:app --reload
```

Access the UI at: `http://localhost:8000`

## API Reference

### Chat
- **Send Message**: `POST /api/chat`
  ```json
  {
    "message": "Hello",
    "model": "gpt-4o",
    "session_id": "optional-uuid",
    "system_prompt": "Optional system prompt that sets the conversation context (only used if this is the first message in a conversation).",
    "guardrail": "off",
    "llm_judge_config": {
        "model": "current",
        "scope": "general-purpose"
    }
  }
  ```

#### Guardrail Configuration (`guardrail`)
The `guardrail` parameter can optionally be sent to dynamically apply moderation or custom policy evaluations on the user's input before resolving the LLM call. Supported values:
- `"off"`: No guardrails applied (Default).
- `"azure-prompt-shields"`: Scans the prompt via Azure Content Safety to block detected jailbreaks. Requires `AZURE_AI_CONTENT_SAFETY_KEY` in environment.
- `"aws-bedrock-pi"`: Evaluates the prompt through AWS Bedrock Guardrails. Requires `AWS_GUARDRAIL_ID` in environment. 
- `"llm-judge"`: Uses an LLM dynamically as a judge to block Prompt Injections and dangerous content according to a structured Trust & Safety Policy.

#### LLM Judge Configuration (`llm_judge_config`)
When the guardrail is set to `"llm-judge"`, the following inner configurations manipulate how the judge operates:
- **`model`**:
  - `"current"`: Uses the selected inference `model` defined in the root payload to run the judge policy.
  - `"gpt-oss-20b-safeguard"`: Independently routes the judge check through `openrouter/openai/gpt-oss-safeguard-20b`, an LLM specifically engineered for reasoning through trust and safety taxonomy (Requires `OPENROUTER_API_KEY`).
- **`scope`**:
  - `"general-purpose"`: The judge evaluates against a wide safety policy blocking jailbreaks, CBRN, illegal content, and dangerous suggestions.
  - `"my-llm-bank"`: The judge evaluates against a strict, narrow taxonomy permitting only retail-banking discussions (e.g., overdrafts, account balances, transfers) and refusing all other standard LLM inquiries.

### Models
- **List Models**: `GET /api/models`

### Sessions
- **List History**: `GET /api/sessions`
- **Get Session**: `GET /api/sessions/{session_id}`
- **Delete Session**: `DELETE /api/sessions/{session_id}`
- **Clear All**: `DELETE /api/sessions`

