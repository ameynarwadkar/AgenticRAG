"""
Config Module - Application Configuration & Infrastructure.

This module contains:
- settings.py: Environment variable management
- database.py: Supabase connection and operations
"""

from .settings import get_settings, Settings
from .database import db, Database
from .otel_setup import setup_opentelemetry

__all__ = ['get_settings', 'Settings', 'db', 'Database', 'setup_opentelemetry']
