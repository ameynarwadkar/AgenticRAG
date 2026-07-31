"""
Observability & Tracing - Agent Step Tracking

This module implements comprehensive tracing for the RAG pipeline using Langfuse.
It allows developers to observe:
- Latency and duration of vector DB retrievals
- Prompt and completion token usage for LLM calls
- Tool execution times and costs per query
- Complex agent workflows via nested traces and spans

By applying these decorators to the RAG backend, you gain complete visibility
into the agent's reasoning loop, making it possible to debug hallucinations
and optimize system performance.
"""
import os
from langfuse import Langfuse
from langfuse import observe, get_client

# Ensure these are in your .env:
# LANGFUSE_SECRET_KEY=sk-lf-...
# LANGFUSE_PUBLIC_KEY=pk-lf-...
# LANGFUSE_HOST=https://cloud.langfuse.com (or your self-hosted URL)

# Initialize Langfuse client
langfuse = Langfuse()

# You can use the @observe() decorator on your RAG functions!
# Example on how to wrap your existing RAG retrieval:

@observe(as_type="retriever")
async def traced_vector_search(query_embedding, top_k):
    """
    To integrate this, you'll add @observe() to db.vector_search 
    or inside rag.py's _retrieve_context function.
    """
    # Langfuse will automatically track the latency!
    # You can also manually add context to the trace:
    langfuse_context.update_current_observation(
        input={"top_k": top_k},
        # model="text-embedding-3-small" (if generating embeddings)
    )
    
    # ... your existing DB logic here ...
    pass

@observe(as_type="generation")
async def traced_llm_call(messages, model):
    """
    Add @observe() to your LLM call methods in chat.py or orchestrator.py
    """
    langfuse_context.update_current_trace(
        name="Agent-RAG-Loop",
        session_id="session-123", # Can group by user interaction
        user_id="user-xyz"
    )
    
    # ... your existing LLM execution here ...
    
    # You can log token usage directly if you parse it from the response:
    # langfuse_context.update_current_observation(
    #     usage={"input": 150, "output": 45, "unit": "TOKENS"}
    # )
    pass


# =====================================================================
# Tool Execution Tracing Example
# =====================================================================
@observe(as_type="span")
async def traced_tool_execution(tool_name: str, **kwargs):
    """
    To track tool execution, you can wrap the tool registry call or the individual
    tool methods. Langfuse will record how long the external API call took and
    what parameters were passed.
    """
    # 1. Log the inputs sent to the tool
    langfuse_context.update_current_observation(
        name=f"Tool Execution: {tool_name}",
        input=kwargs
    )
    
    try:
        # ... your existing tool execution logic (e.g., await tool.execute(**kwargs)) ...
        result = {"status": "SUCCESS", "data": "Tool output"}
        
        # 2. Log the successful output
        langfuse_context.update_current_observation(output=result)
        return result
        
    except Exception as e:
        # 3. Log errors if the tool fails
        langfuse_context.update_current_observation(
            level="ERROR",
            status_message=str(e)
        )
        raise
