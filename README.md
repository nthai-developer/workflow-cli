# 🛡️ AI Workflow CLI

> **Turn your AI IDE into a disciplined Senior Engineer.**

`workflow-cli` is a **Model Context Protocol (MCP) Server** designed to enforce strict software development workflows within AI-powered IDEs (like Cursor, Windsurf, Claude Desktop, and Antigravity).

It prevents "lazy coding" and hallucinations by enforcing a **State-Machine driven workflow**: Planning → Testing (TDD) → Implementation.

---

## 🌟 Key Features

* **🚫 Strict Mode:** Blocks the AI from generating code until a valid Test Case exists.
* **🚦 State Machine Enforcement:** Manages project states (`PLANNING` → `TESTING` → `CODING`).
* **🔐 Secure Global Config:** Manages API Keys via a global user configuration (`~/.ai_workflow_env`), eliminating the need for risky `.env` files in your repositories.
* **⚡ Instant Distribution:** Deployable immediately via `uv tool`, zero friction setup.
* **💬 Command-Driven:** Replaces free-text chat with structured commands (`/start`, `/plan`, `/test`, `/impl`).

---

## 🚀 Installation

**Prerequisite:** You must have [uv](https://github.com/astral-sh/uv) installed.

### 1. Install the Tool

Run this command to install the tool directly from the repository (you only need to do this once):

```bash
uv tool install --force git+[https://github.com/nthai-developer/workflow-cli.git](https://github.com/nthai-developer/workflow-cli.git)

```

### 2. Configuration (Setup API Keys)

Run the configure command to interactively set up your environment variables (Gemini/OpenAI Keys):

```bash
workflow-cli configure

```

*Configuration is saved securely at `~/.ai_workflow_env` (macOS/Linux) or `%USERPROFILE%\.ai_workflow_env` (Windows).*

---

## 🔌 IDE Integration

Add the following configuration to your IDE's MCP settings file (e.g., `/Users/apple/.gemini/antigravity/mcp_config.json` or Cursor Settings).

```json
{
  "mcpServers": {
    "workflow-guard": {
      "command": "uv",
      "args": ["tool", "run", "workflow-cli"]
    }
  }
}

```

*Note: You do not need to define `env` or `cwd` here. The tool automatically loads the global configuration you set up in step 2.*

---

## 🎮 Usage Guide

Once installed, **you cannot chat freely** (e.g., "Write a login function"). You must follow the strict workflow commands:

### Step 1: Initialize (`/start`)

Start a new feature or task.

> **User:** `/start AUTH-01 User Login Feature`
> **AI:** 🚀 **STARTED**. Context loaded. State transitioned to **PLANNING**.

### Step 2: Planning (`/plan`)

The AI generates technical specifications and architecture docs.

> **User:** `/plan`
> **AI:** 📝 Specs generated at `docs/specs/AUTH-01.md`.
> *Next Step: Generate tests.*

### Step 3: Test Generation (`/test`)

The AI generates Unit Tests based on the Plan. (The tests will fail initially - Red Phase).

> **User:** `/test`
> **AI:** 🧪 Tests generated at `tests/test_auth.py`. State transitioned to **TESTING**.

### Step 4: Implementation (`/impl`)

Only when the state is `TESTING` are you allowed to generate implementation code.

> **User:** `/impl`
> **AI:** 🔨 Implementing logic to pass the tests...

---

## ⛔ Enforcement Protocol (System Prompt)

To ensure the AI respects these rules, paste the following into your IDE's **System Prompt** or **`.agent/rules/execute-rule.md`** file:

```markdown
# STRICT WORKFLOW PROTOCOL
You are a Workflow Execution Unit. You DO NOT accept free-text coding requests.

## RULES:
1. Every user request MUST be mapped to the `workflow_command` tool.
2. If the user says "Create a login page", you MUST Reject it:
   "⛔ Violation. Please start a workflow task first using: `/start [Ticket] [Desc]`"
3. DO NOT hallucinate workflow steps. Follow the tool's output verbatim.
4. If the tool returns "BLOCKED", stop immediately and guide the user to the correct step.

## COMMAND MAPPING:
- User starts with "/start" -> call tool `workflow_command(command="start", args=...)`
- User starts with "/plan"  -> call tool `workflow_command(command="plan", args=...)`
- User starts with "/test"  -> call tool `workflow_command(command="test", args=...)`
- User starts with "/impl"  -> call tool `workflow_command(command="impl", args=...)`

```

---

## 🛠️ Development

If you want to contribute to this tool:

```bash
# Clone the repo
git clone [https://github.com/nthai-developer/workflow-cli.git](https://github.com/nthai-developer/workflow-cli.git)
cd ai-workflow-core

# Install dependencies in editable mode
uv venv
source .venv/bin/activate
uv pip install -e .

# Help command
workflow-cli --help

```
