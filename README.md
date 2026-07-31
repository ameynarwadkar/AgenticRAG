# 🤖 AgenticRAG

A production-ready FastAPI backend demonstrating **Agentic RAG**. A system that combines Retrieval-Augmented Generation (RAG) with autonomous tool-calling capabilities to create intelligent, action-oriented AI agents.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.0+-00a393.svg)](https://fastapi.tiangolo.com)

---

## 🚀 Overview

While traditional RAG systems simply retrieve context and generate an answer (`Query → Retrieve → Answer`), **AgenticRAG** introduces an autonomous reasoning loop:

**`Query → Retrieve → Reason → Decide → Act → Answer`**

The agent is capable of:
1. **Retrieving** relevant context from a vector knowledge base.
2. **Reasoning** about whether the context is relevant to the user's action.
3. **Deciding** if external tools need to be called.
4. **Acting** by executing tools (e.g., scheduling meetings, sending emails).
5. **Answering** the user with citations and confirmations of actions taken.

### 🌟 Key Features

- **Vector Search Engine**: Powered by Supabase `pgvector`.
- **Intelligent Routing**: Multi-provider support (OpenAI, Azure OpenAI, Anthropic).
- **Autonomous Agents**: Built-in reasoning loop for tool execution.
- **Tool Integrations**: Google Calendar scheduling and Gmail sending out-of-the-box.
- **Conversational Memory**: Multi-turn chat history support.
- **Citation Tracking**: Source attribution for generated answers.

### 🏢 Enterprise-Grade Features Added

- **Multi-Tenant Security**: Row-Level Security (RLS) implemented in Supabase to ensure users only access their own vector embeddings via scoped JWT tokens.
- **Human-in-the-Loop (HITL)**: High-risk tools (like calendar edits and emails) are paused in a `PENDING_APPROVAL` state, requiring explicit frontend confirmation before execution.
- **Action Idempotency**: Tool execution wrappers generate SHA-256 hashes of arguments to prevent accidental duplicate actions (like sending double emails) during LLM network retries.
- **Observability (OTel & Langfuse)**: Fully instrumented with OpenTelemetry for FastAPI/OpenAI distributed tracing, combined with Langfuse for prompt monitoring, token counting, and evaluation.
- **Audit Logging**: Comprehensive system tracking (`audit_logger`) that logs all tool executions, parameters, and their success/failure status to the database.
- **CI/CD Pipeline**: Jenkins pipeline (`Jenkinsfile`) integrated with `pytest` and mock LLM calls to automatically validate the RAG agent's logic on every commit.

---

## 📁 Architecture & Structure

```
AgenticRAG/
├── app/
│   ├── agents/            # Main agent reasoning loop & orchestrator
│   │   └── tools/         # Agent capabilities (Calendar, Email)
│   ├── services/          # Core RAG logic, embeddings, chunking
│   ├── schemas/           # Pydantic validation models
│   ├── config/            # Environment & database configurations
│   └── data/              # Default seeding documents
├── tests/                 # Setup verification and debugging utilities
├── credentials/           # Secure storage for service accounts (gitignored)
├── sql/                   # Database initialization scripts
└── static/                # Web chat interface UI
```

---

## 🛠️ Quick Setup Guide

### 1. Prerequisites
- **Python 3.11+**
- **Supabase Account** for PostgreSQL + pgvector
- **OpenAI / Azure OpenAI / Anthropic** API Keys
- **Google Cloud Console** (Optional: for Calendar & Email tools)

### 2. Installation

```bash
git clone https://github.com/ameynarwadkar/AgenticRAG.git
cd AgenticRAG

# Using uv for lightning-fast package management (or pip)
uv venv
source .venv/bin/activate

uv pip install -r requirements.txt
```

### 3. Database Initialization
1. Create a new project in [Supabase](https://supabase.com/).
2. Navigate to the **SQL Editor**.
3. Copy and run the contents of `sql/init_supabase.sql` to create the `rag_chunks` table, vector indexes, and search functions.

### 4. Configuration
Create your `.env` file from the template:
```bash
cp .env.example .env
```
Fill in your API keys, Supabase credentials, and preferred AI provider (`openai`, `azure`, or `anthropic`).

*(Optional)* For Google Workspace tools:
Place your Google Service Account JSON in `credentials/service_account.json` and configure `GOOGLE_CALENDAR_EMAIL`. Note: Domain-Wide Delegation is required for Google Workspace accounts.

### 5. Verify & Run

Verify your setup using the built-in diagnostic tool:
```bash
uv run python tests/test_setup.py
```

Start the FastAPI server:
```bash
uv run uvicorn main:app --reload --port 8000
```

---

## 📚 API Usage

Once the server is running, visit `http://localhost:8000/docs` for the interactive Swagger UI.

### Seed the Knowledge Base
Populate the vector database with the default documents:
```bash
curl -X POST http://localhost:8000/seed
```

### Pure RAG Query
Answers questions strictly based on the retrieved context.
```bash
curl -X POST http://localhost:8000/answer \
  -H "Content-Type: application/json" \
  -d '{"query": "What is your return policy?", "top_k": 6}'
```

### Agentic Query (Reasoning + Tools)
Can answer questions AND take actions. The agent will use RAG context to influence tool parameters if needed.
```bash
curl -X POST http://localhost:8000/agent \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Schedule a consultation call with john@example.com for tomorrow at 2pm",
    "top_k": 6
  }'
```

---

## 🔧 Adding Custom Tools

The architecture is highly extensible. To add a new agent capability:

1. **Create the Tool (`app/agents/tools/my_tool.py`)**:
   Inherit from `BaseTool` and implement the `execute` method.
2. **Register in Registry (`app/agents/tools/registry.py`)**:
   Add your tool to the `ToolRegistry`.
3. **Add Tool Schema (`app/schemas/tool_schemas.py`)**:
   Provide the JSON schema definition for the LLM to understand when and how to invoke the tool.

---

## 🐳 Docker Deployment

A `Dockerfile` is included for containerized deployment (e.g., Google Cloud Run, AWS AppRunner, Docker Compose).

```bash
docker build -t agentic-rag .
docker run -p 8080:8080 --env-file .env agentic-rag
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License
This project is licensed under the MIT License.