"""
Audit Logger - Append-Only Enterprise Tracking

This module provides an append-only audit ledger service for tracking agent actions.
It securely logs:
- Tool executions (which tools were called)
- Input parameters and output results
- Execution status (SUCCESS/ERROR)
- Trace IDs, Session IDs, and User IDs for compliance

This is crucial for enterprise deployments where every autonomous agent
action must be traceable, auditable, and immutable for compliance purposes.
"""
import logging
from typing import Any, Dict, Optional
import time
from app.config.database import db

logger = logging.getLogger(__name__)

class AuditLogger:
    """Append-only audit ledger for logging tool executions and critical agent steps."""
    
    @staticmethod
    async def log_tool_execution(
        tool_name: str,
        input_params: Dict[str, Any],
        output_results: Optional[Dict[str, Any]],
        status: str,
        model_used: Optional[str] = None,
        execution_duration_ms: Optional[int] = None,
        session_id: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> None:
        """Log a tool execution to the Supabase audit_logs table."""
        try:
            client = db.get_client(admin=True)
            
            log_entry = {
                'tool_name': tool_name,
                'input_params': input_params,
                'output_results': output_results or {},
                'status': status,
                'model_used': model_used,
                'execution_duration_ms': execution_duration_ms,
                'session_id': session_id,
                'user_id': user_id
            }
            
            # Fire and forget / background insertion
            client.table('audit_logs').insert(log_entry).execute()
            logger.info(f"Audit Log Recorded: {tool_name} [{status}]")
            
        except Exception as e:
            # We don't want audit logging failures to crash the main agent flow,
            # but we must log that the audit failed.
            logger.error(f"CRITICAL: Failed to write to audit ledger: {e}")

# Global instance for easy imports
audit_logger = AuditLogger()
