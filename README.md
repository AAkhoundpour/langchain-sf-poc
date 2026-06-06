# LangChain Salesforce POC

A small Python proof-of-concept project to learn how to use **LangChain** with a mocked Salesforce MCP-style service.

The goal is to understand:

- How a user prompt is sent to an agent
- How LangChain decides when to call a tool
- How tools connect to backend service functions
- How tool input and output are passed back to the agent
- How to inspect the agent/tool-calling flow using debug logs

This project does **not** connect to real Salesforce yet.  
It uses a mocked `sf_mcp_service.py` file with sample Accounts and Cases.

---

## Project Structure

```text
langchain-sf-poc/
├── README.md
├── requirements.txt
├── pyproject.toml
├── .env
└── src/
    └── langchain_sf_poc/
        ├── __init__.py
        ├── main.py
        ├── agent.py
        ├── agent_logger.py
        ├── config.py
        ├── tools.py
        └── sf_mcp_service.py
```

---

## How It Works

```text
User prompt
   ↓
main.py
   ↓
agent.py
   ↓
LangChain Agent
   ↓
tools.py
   ↓
sf_mcp_service.py
   ↓
Mock Salesforce data
```

Example:

```text
User: Find accounts in the education industry

LangChain agent decides:
I need Salesforce account data.

Agent calls:
search_salesforce_accounts("education")

Tool calls:
search_accounts("education")

Mock service returns:
Matching Salesforce accounts
```

---

## Prerequisites

You need:

- Python 3.10+
- Ollama installed and running
- A local Ollama model already downloaded

Check Ollama is running:

```bash
ollama list
```

If you have `qwen3:latest`, you can use that.

Test it directly:

```bash
ollama run qwen3:latest
```

---

## Setup

From the project root:

```bash
cd langchain-sf-poc
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create your `.env` file:

```bash
touch .env
```

Add this:

```env
OLLAMA_MODEL=qwen3:latest
OLLAMA_BASE_URL=http://localhost:11434
```

If your Ollama model has a different name, use the exact value from:

```bash
ollama list
```

Example:

```env
OLLAMA_MODEL=llama3.2:latest
OLLAMA_BASE_URL=http://localhost:11434
```

---

## Run the Project

Use this command from the project root:

```bash
PYTHONPATH=src python -m langchain_sf_poc.main
```

You should see a console prompt where you can type a question.

---

## Example Prompts

Try these:

```text
Find accounts in the education industry
```

```text
Get account A-1001
```

```text
Show me open cases for account A-1001
```

```text
Create a high priority case for account A-1002 with subject Payment webhook failed again
```

```text
Find education accounts and tell me which one has open cases
```

```text
Create a medium priority case for Inquisitive Education saying Teacher portal login is failing
```

```text
Do we have any financial services accounts?
```

---

## Debug Logging

The project includes `agent_logger.py` to show more detail about what the agent is doing.

When you run the project, you should see logs like:

```text
[CHAIN START]
[LLM START]
[AGENT ACTION]
[TOOL START]
[TOOL END]
[AGENT FINISH]
```

These logs help you understand:

- What prompt was sent to the LLM
- Which tool the agent selected
- What input was passed to the tool
- What output came back from the tool
- What final response was returned to the user

---

## Important Files

### `main.py`

Entry point for the console application.

It gets input from the user and sends it to the agent.

---

### `agent.py`

Builds the LangChain agent.

It configures:

- The LLM
- The available tools
- The system prompt
- The debug callback handler

---

### `tools.py`

Defines LangChain tools.

Each tool wraps a function from `sf_mcp_service.py`.

Example:

```python
@tool
def search_salesforce_accounts(search_term: str) -> str:
    return search_accounts(search_term)
```

This makes the function available to the LangChain agent.

---

### `sf_mcp_service.py`

Mock Salesforce backend service.

It contains sample data and functions such as:

- `search_accounts`
- `get_account_by_id`
- `get_open_cases_for_account`
- `create_case`

This file simulates what a real Salesforce MCP service might do later.

---

### `config.py`

Loads environment variables from `.env`.

Example:

```python
OLLAMA_MODEL=qwen3:latest
OLLAMA_BASE_URL=http://localhost:11434
```

---

### `agent_logger.py`

Custom LangChain callback handler.

It prints the agent execution flow so you can see tool calling details.

---

## Common Errors

### Error: model not found

Example:

```text
Error: model 'llama3.1' not found
```

Fix:

```bash
ollama list
```

Then update `.env` with the exact model name.

Example:

```env
OLLAMA_MODEL=qwen3:latest
```

---

### Error: No module named `langchain_sf_poc`

This means Python cannot find the `src` folder.

Run with:

```bash
PYTHONPATH=src python -m langchain_sf_poc.main
```

Or install the project locally:

```bash
pip install -e .
python -m langchain_sf_poc.main
```

---

### Error: cannot import name `settings`

Make sure `config.py` contains:

```python
settings = Settings()
```

---

### Error: cannot import name `tools`

Make sure `tools.py` has a list at the bottom:

```python
tools = [
    search_salesforce_accounts,
    get_salesforce_account,
    get_salesforce_open_cases,
    create_salesforce_case,
]
```

---

## Next Improvements

Good next steps:

1. Add real Salesforce authentication
2. Replace mocked data with real SOQL queries
3. Add a tool for running safe read-only SOQL
4. Add a tool for creating Salesforce Cases
5. Add guardrails so the agent cannot perform risky actions without confirmation
6. Add LangSmith tracing later if deeper observability is needed
7. Convert this into a proper MCP server/client pattern

---

## Learning Goal

This project is mainly for understanding LangChain.

The most important concept is:

```text
LangChain agent = LLM + tools + decision loop
```

The LLM does not directly access Salesforce.

Instead, it decides when to call a tool, and the tool calls the backend service.

That means the architecture is:

```text
LLM decides
Tool executes
Service owns the business logic
```

This is a good pattern because the model can reason, but your Python code still controls what actions are actually allowed.
