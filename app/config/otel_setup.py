"""
OpenTelemetry (OTel) Integration - Vendor-Agnostic Tracing

While Langfuse is great for LLM-specific tracing, OpenTelemetry is the 
enterprise standard for end-to-end system observability. It allows you to 
send traces to Datadog, New Relic, Jaeger, Grafana Tempo, or even Langfuse (via OTel export).

This script demonstrates how to auto-instrument your entire FastAPI app
and OpenAI calls without needing custom decorators on every function.
"""

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
# Note: You'll need `pip install opentelemetry-instrumentation-openai`
from opentelemetry.instrumentation.openai import OpenAIInstrumentor 

def setup_opentelemetry(app: FastAPI):
    """
    Call this function in your main.py right after creating the FastAPI app.
    Example:
        app = FastAPI(...)
        setup_opentelemetry(app)
    """
    
    # 1. Setup the Tracer Provider (The engine that generates traces)
    # Define the service name so it shows up beautifully in Jaeger
    resource = Resource(attributes={"service.name": "AgenticRAG"})
    provider = TracerProvider(resource=resource)
    
    # 2. Setup the Exporter (Where do the traces go?)
    # Since we are using Langfuse, Langfuse automatically intercepts the OpenTelemetry 
    # TracerProvider in the background. We don't need to manually configure an Exporter!
    # (If you wanted local terminal logs, you could uncomment the ConsoleSpanExporter below)
    # processor = BatchSpanProcessor(ConsoleSpanExporter())
    # provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    # 3. Auto-Instrument FastAPI 
    # This automatically creates a trace for every incoming HTTP request!
    FastAPIInstrumentor.instrument_app(app)

    # 4. Auto-Instrument OpenAI (Optional)
    # This automatically intercepts all openai.completions.create() calls
    # and attaches prompt/completion tokens and latency to the active FastAPI trace.
    OpenAIInstrumentor().instrument()

    print("✅ OpenTelemetry instrumentation initialized!")

# =====================================================================
# Manual Tracing Example
# =====================================================================
def perform_complex_db_search():
    """Example of how to manually create a span inside an existing trace."""
    tracer = trace.get_tracer(__name__)
    
    with tracer.start_as_current_span("VectorSearch") as span:
        # Add attributes that will show up in Datadog/Jaeger
        span.set_attribute("search.top_k", 6)
        span.set_attribute("search.index", "rag_chunks")
        
        try:
            # db.vector_search(...)
            span.add_event("Vector search completed successfully")
        except Exception as e:
            span.record_exception(e)
            span.set_status(trace.status.Status(trace.status.StatusCode.ERROR))
