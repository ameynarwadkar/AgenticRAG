# 🤖 Agentic RAG AI Backend

A production-ready FastAPI backend demonstrating **Agentic RAG** - combining Retrieval-Augmented Generation with autonomous tool-calling capabilities.

> **🎬 This is an extension of [yt-rag](https://github.com/ShenSeanChen/yt-rag)** - If you're new here, check out the original RAG tutorial first!

📹 **YouTube Tutorial**: [YouTube Link](https://www.youtube.com/watch?v=w-1lnCmqf_E&list=PLE9hy4A7ZTmpGq7GHf5tgGFWh2277AeDR&index=34)

☕️ **Support**: [Buy me a coffee](https://buy.stripe.com/5kA176bA895ggog4gh)

🤖 **Discord**: [Join our community](https://discord.com/invite/TKKPzZheua)

---

## 🆕 What's New in Agentic RAG?

| Feature | yt-rag (v1) | yt-agentic-rag (v2) |
|---------|-------------|---------------------|
| Vector Search | ✅ | ✅ |
| RAG Q&A | ✅ | ✅ |
| **Tool Calling** | ❌ | ✅ |
| **Agent Reasoning Loop** | ❌ | ✅ |
| **Calendar Scheduling** | ❌ | ✅ |
| **Email Sending** | ❌ | ✅ |
| **Multi-turn Chat History** | ❌ | ✅ |
| **Multi-step Actions** | ❌ | ✅ |

### The Key Difference

**Traditional RAG**: `Query → Retrieve → Answer`

**Agentic RAG**: `Query → Retrieve → Reason → Decide → Act → Answer`

The agent can now:
1. **Retrieve** relevant context from your knowledge base
2. **Reason** about whether the context is relevant to the action
3. **Decide** if tools need to be called
4. **Act** by executing tools (schedule meetings, send emails)
5. **Answer** with citations and confirmation of actions taken

---

## 📁 Project Structure

```
yt-agentic-rag/
│
├── 📂 app/                              # 🚀 PRODUCTION APPLICATION
│   │
│   ├── 📂 agents/                       # 🤖 AI AGENTS (the star of the show!)
│   │   ├── __init__.py                  # Exports agent_service
│   │   ├── orchestrator.py              # Main agent reasoning loop
│   │   └── 📂 tools/                    # Agent capabilities
│   │       ├── __init__.py              # Exports tool_registry
│   │       ├── base.py                  # Abstract base class for tools
│   │       ├── registry.py              # Tool registration & execution
│   │       ├── calendar_tool.py         # Google Calendar integration
│   │       └── email_tool.py            # Gmail integration
│   │
│   ├── 📂 services/                     # 📦 Core business logic
│   │   ├── __init__.py
│   │   ├── rag.py                       # RAG pipeline (retrieve → augment → generate)
│   │   ├── embedding.py                 # Vector embedding service
│   │   ├── chat.py                      # LLM chat completion service
│   │   └── chunker.py                   # Text chunking utilities
│   │
│   ├── 📂 schemas/                      # 📋 API request/response definitions
│   │   ├── __init__.py
│   │   ├── requests.py                  # Input validation (AgentRequest, etc.)
│   │   ├── responses.py                 # Output formats (AgentResponse, etc.)
│   │   ├── entities.py                  # Database entity models
│   │   └── tool_schemas.py              # LLM function-calling definitions
│   │
│   ├── 📂 config/                       # ⚙️ Configuration & infrastructure
│   │   ├── __init__.py
│   │   ├── settings.py                  # Environment variable management
│   │   └── database.py                  # Supabase connection & operations
│   │
│   ├── 📂 data/                         # 📚 Static data
│   │   ├── __init__.py
│   │   └── default_documents.py         # Sample documents for RAG
│   │
│   └── main.py                          # FastAPI app & route definitions
│
├── 📂 devtools/                         # 🛠️ Development & debugging utilities
│   ├── README.md                        # How to use these tools
│   ├── test_setup.py                    # Verify your setup works
│   ├── verify_rag.py                    # Prove RAG is working
│   ├── check_dimensions.py              # Debug embedding dimensions
│   └── chatbot.py                       # Terminal chat client
│
├── 📂 credentials/                      # 🔐 Google service account (gitignored)
│   └── service_account.json             # Your GCP service account key
│
├── 📂 sql/                              # 🗄️ Database setup
│   └── init_supabase.sql                # Supabase schema & pgvector setup
│
├── 📂 static/                           # 🎨 Frontend assets
│   └── chat.html                        # Web chat interface
│
├── main.py                              # Root entry point (re-exports app/main.py)
├── requirements.txt                     # Python dependencies
├── Dockerfile                           # Container configuration
├── .env.example                         # Environment variable template
├── DEPLOYMENT.md                        # Cloud Run deployment guide
└── README.md                            # This file
```

---

## 🚀 Complete Setup Guide (From Scratch)

### Prerequisites

- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Git** - [Download](https://git-scm.com/downloads)
- **Supabase Account** - [Sign up free](https://supabase.com)
- **OpenAI API Key** - [Get key](https://platform.openai.com/api-keys)
- **Google Cloud Account** (for calendar/email tools) - [Console](https://console.cloud.google.com)

---

### Step 1: Clone and Install

```bash
# Clone the repository
git clone https://github.com/ShenSeanChen/yt-agentic-rag.git
cd yt-agentic-rag

# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

---

### Step 2: Set Up Supabase (Vector Database)

#### 2.1 Create a Supabase Project

1. Go to [supabase.com](https://supabase.com) and sign in
2. Click **"New Project"**
3. Choose a name (e.g., `agentic-rag`)
4. Set a secure database password (save this!)
5. Select a region close to you
6. Click **"Create new project"** and wait for setup

#### 2.2 Get Your API Keys

1. In your project, go to **Settings** → **API**
2. Copy these values:
   - **Project URL** (e.g., `https://abc123.supabase.co`)
   - **anon public key** (starts with `eyJ...`)
   - **service_role key** (starts with `eyJ...`) - ⚠️ Keep this secret!

#### 2.3 Initialize the Database Schema

1. In Supabase, go to **SQL Editor**
2. Click **"New Query"**
3. Copy the contents of `sql/init_supabase.sql` and paste it
4. Click **"Run"** to execute

This creates:
- `rag_chunks` table for storing document embeddings
- `match_chunks` function for vector similarity search
- Required indexes for performance

---

### Step 3: Set Up OpenAI

1. Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Click **"Create new secret key"**
3. Copy the key (starts with `sk-...`)

---

### Step 4: Set Up Google Cloud (For Calendar & Email Tools)

> ⚠️ **Skip this step** if you only want RAG without tool calling.

#### 4.1 Create a Google Cloud Project

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Click the project dropdown → **"New Project"**
3. Name it (e.g., `agentic-rag-tools`)
4. Click **"Create"**

#### 4.2 Enable APIs

1. Go to **APIs & Services** → **Library**
2. Search and enable:
   - **Google Calendar API**
   - **Gmail API**

#### 4.3 Create a Service Account

1. Go to **IAM & Admin** → **Service Accounts**
2. Click **"Create Service Account"**
3. Name: `agentic-rag-service`
4. Click **"Create and Continue"**
5. Skip the optional steps, click **"Done"**

#### 4.4 Generate a Key

1. Click on your new service account
2. Go to **Keys** tab
3. Click **"Add Key"** → **"Create new key"**
4. Choose **JSON**
5. Click **"Create"** - a file downloads
6. **Move this file** to `credentials/service_account.json` in your project

#### 4.5 Enable Domain-Wide Delegation (Google Workspace)

> Required if using a Google Workspace account (e.g., `@yourcompany.com`)

1. In the service account details, click **"Show Advanced Settings"**
2. Copy the **Client ID** (a long number)
3. Go to [admin.google.com](https://admin.google.com) (Google Workspace Admin)
4. Navigate to **Security** → **API Controls** → **Domain-wide Delegation**
5. Click **"Add new"**
6. Paste the Client ID
7. Add these OAuth scopes:
   ```
   https://www.googleapis.com/auth/calendar
   https://www.googleapis.com/auth/gmail.send
   ```
8. Click **"Authorize"**

---

### Step 5: Configure Environment Variables

```bash
# Copy the template
cp .env.example .env

# Edit with your values
nano .env  # or use your preferred editor
```

**Fill in your `.env` file:**

```env
# ===========================================
# SUPABASE CONFIGURATION (Required)
# ===========================================
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key

# ===========================================
# OPENAI CONFIGURATION (Required)
# ===========================================
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_EMBED_MODEL=text-embedding-3-small
OPENAI_CHAT_MODEL=gpt-4o

# ===========================================
# AI PROVIDER SETTINGS
# ===========================================
AI_PROVIDER=openai

# ===========================================
# GOOGLE API CONFIGURATION (For Tools - Optional)
# ===========================================
GOOGLE_SERVICE_ACCOUNT_PATH=credentials/service_account.json
GOOGLE_CALENDAR_EMAIL=your-email@yourcompany.com
GOOGLE_CALENDAR_ID=primary

# ===========================================
# APPLICATION SETTINGS
# ===========================================
ENVIRONMENT=development
LOG_LEVEL=INFO
```

---

### Step 6: Verify Setup

```bash
# Run the setup verification script
python tests/test_setup.py
```

You should see:
```
✅ All modules imported successfully
✅ Environment variables configured
✅ Database connection successful
✅ Database schema validated
✅ Successfully seeded X document chunks
✅ RAG query successful!
🎉 ALL TESTS PASSED!
```

---

### Step 7: Start the Server

```bash
uvicorn main:app --reload --port 8000
```

Visit:
- **API Docs**: http://localhost:8000/docs
- **Chat UI**: http://localhost:8000/chat
- **Health Check**: http://localhost:8000/healthz

---

## 📚 API Endpoints

### Health & Info

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/healthz` | GET | Health check with database status |
| `/tools` | GET | List available agent tools |
| `/documents` | GET | List documents in knowledge base |

### RAG (Question Answering)

```bash
# Traditional RAG - Answer questions from knowledge base
curl -X POST http://localhost:8000/answer \
  -H "Content-Type: application/json" \
  -d '{"query": "What is your return policy?", "top_k": 6}'
```

### 🆕 Agent (RAG + Tool Calling)

```bash
# Agentic RAG - Can answer questions AND take actions
curl -X POST http://localhost:8000/agent \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Schedule a consultation call with john@example.com for tomorrow at 2pm",
    "top_k": 6
  }'
```

### 🆕 Multi-turn Conversations (Chat History)

```bash
# Include chat history for context-aware conversations
curl -X POST http://localhost:8000/agent \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Make it 30 minutes",
    "chat_history": [
      {"role": "user", "content": "Schedule a call with john@example.com tomorrow at 2pm"},
      {"role": "assistant", "content": "I can schedule that. How long should the meeting be?"}
    ],
    "top_k": 6
  }'
```

---

## 🔧 Adding New Tools

The architecture makes it easy to add new agent capabilities:

### 1. Create the Tool (`app/agents/tools/my_tool.py`)

```python
# Directory: yt-agentic-rag/app/agents/tools/my_tool.py

from typing import Dict, Any
from .base import BaseTool

class MyTool(BaseTool):
    """Description of what this tool does."""
    
    @property
    def name(self) -> str:
        return "my_tool_name"
    
    @property
    def description(self) -> str:
        return "A clear description for the LLM"
    
    async def execute(self, param1: str, param2: int = 10, **kwargs) -> Dict[str, Any]:
        """Execute the tool with given parameters."""
        # Your implementation here
        result = do_something(param1, param2)
        return self._success_response({"result": result})

# Export singleton instance
my_tool = MyTool()
```

### 2. Register in Registry (`app/agents/tools/registry.py`)

```python
from .my_tool import my_tool

class ToolRegistry:
    def _register_default_tools(self):
        self.register(calendar_tool)
        self.register(email_tool)
        self.register(my_tool)  # Add your tool here
```

### 3. Add Tool Schema (`app/schemas/tool_schemas.py`)

```python
TOOL_DEFINITIONS.append({
    "type": "function",
    "function": {
        "name": "my_tool_name",
        "description": "A clear description for the LLM to understand when to use this tool",
        "parameters": {
            "type": "object",
            "properties": {
                "param1": {
                    "type": "string",
                    "description": "What this parameter is for"
                },
                "param2": {
                    "type": "integer",
                    "description": "Optional parameter with default"
                }
            },
            "required": ["param1"]
        }
    }
})
```

---

## 🎬 Demo Scenarios

### Scenario 1: RAG Influences Tool Parameters

**User**: "Schedule a standard consultation meeting with Emma"

**Agent**:
1. Retrieves RAG context → finds "Standard consultation calls are 30 minutes"
2. Uses this info to set duration = 30 minutes
3. Calls calendar tool with correct duration
4. Responds with citation `[scheduling_consultation_v1]`

### Scenario 2: Multi-turn Conversation

**User**: "I want to schedule a meeting"
**Agent**: "I'd be happy to help! Who should I invite and when?"
**User**: "With john@example.com tomorrow at 3pm"
**Agent**: "What type of meeting? (consultation, demo, support call)"
**User**: "A product demo"
**Agent**: *Creates 45-minute meeting based on RAG context*

### Scenario 3: Pure Tool Call (RAG Irrelevant)

**User**: "Send an email to john@example.com saying hello"

**Agent**:
1. Retrieves context → policies not relevant
2. Ignores irrelevant context
3. Calls email tool directly
4. Confirms action

---

## 🐳 Docker Deployment

```bash
# Build the image
docker build -t yt-agentic-rag .

# Run with environment variables
docker run -p 8080:8080 --env-file .env yt-agentic-rag
```

---

## ☁️ Google Cloud Run Deployment

### 1. Deploy the Container

Deploy your Docker image to Cloud Run via the console or CLI.

### 2. Set Up Service Account Secret

The Google Calendar/Gmail tools require a service account JSON file. Since you can't commit credentials to git, use **Secret Manager**:

```bash
# Create the secret from your local service account file
gcloud secrets create service_account \
  --data-file=credentials/service_account.json \
  --project=YOUR_PROJECT_ID

# Grant Cloud Run access to the secret
gcloud secrets add-iam-policy-binding service_account \
  --member="serviceAccount:YOUR_PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor" \
  --project=YOUR_PROJECT_ID
```

> 💡 Find your project number in Cloud Console → IAM & Admin → Settings

### 3. Mount Secret as Volume in Cloud Run

**Important**: The service account JSON must be mounted as a **file**, not an environment variable.

#### Step A: Create Volume (Volumes Tab)
1. Go to Cloud Run → Your Service → **Edit & Deploy New Revision**
2. Go to **Volumes** tab → **Add Volume**
3. Configure:
   - **Volume type**: Secret
   - **Volume name**: `secret-1`
   - **Secret**: `service_account`
   - **Path 1**: `service_account.json` *(just the filename, not full path!)*
   - **Version**: `latest`
4. Click **Done**

#### Step B: Mount Volume (Containers Tab)
1. Go to **Containers** tab → Click on your container
2. Scroll to **Volume Mounts** → **Add Volume Mount**
3. Configure:
   - **Volume**: `secret-1`
   - **Mount path**: `/app/credentials`
4. Click **Done** → **Deploy**

This makes the secret available at `/app/credentials/service_account.json` which is exactly what the code expects.

### 4. Set Environment Variables

In Cloud Run, add these environment variables:
- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_ROLE_KEY`
- `OPENAI_API_KEY`
- `GOOGLE_CALENDAR_EMAIL` (your workspace email)
- `GOOGLE_SERVICE_ACCOUNT_PATH=credentials/service_account.json`

See [DEPLOYMENT.md](DEPLOYMENT.md) for more deployment options.

---

## 📁 Migration from yt-rag

If you're upgrading from yt-rag:

1. ✅ Your existing Supabase database works as-is
2. ➕ Add new environment variables for Google APIs
3. ✅ The `/answer` endpoint works identically  
4. 🆕 Use `/agent` for new agentic capabilities
5. 🔄 Re-seed with `/seed` to add scheduling policy documents

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-tool`)
3. Add your tool to `app/agents/tools/`
4. Update tool schemas in `app/schemas/tool_schemas.py`
5. Submit a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙋‍♂️ Support

- 📚 **API Docs**: Visit `/docs` when running the server
- 🐛 **Issues**: [GitHub Issues](https://github.com/ShenSeanChen/yt-agentic-rag/issues)
- 💬 **Discord**: [Join our community](https://discord.com/invite/TKKPzZheua)

---

**Built with ❤️ for the developer community**

*From simple RAG to autonomous agents - this project shows the evolution of AI-powered applications.*