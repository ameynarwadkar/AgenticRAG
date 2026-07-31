"""
Root Entry Point (for uvicorn compatibility).

This file re-exports the FastAPI app from app/main.py.
It allows running: uvicorn main:app --reload

The actual application code is in app/main.py.
"""

from app.main import app

# Re-export the app for uvicorn
__all__ = ["app"]