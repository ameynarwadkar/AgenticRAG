import uuid
from typing import Dict, Any, Callable
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

# ==========================================
# 1. Action Store (In-Memory for now, move to Redis/Postgres later)
# ==========================================
PENDING_ACTIONS: Dict[str, dict] = {}

# ==========================================
# 2. Tool Wrapper / Execution Logic
# ==========================================
def request_tool_approval(tool_name: str, kwargs: dict) -> str:
    """
    Called by the agent orchestrator instead of executing a high-risk tool.
    Creates a pending action and tells the LLM to wait.
    """
    action_id = str(uuid.uuid4())
    
    # Store the action payload
    PENDING_ACTIONS[action_id] = {
        "tool_name": tool_name,
        "kwargs": kwargs,
        "status": "PENDING"
    }
    
    # Return this string to the LLM so it knows it must wait.
    return (
        f"ACTION PAUSED: The '{tool_name}' tool requires human approval. "
        f"An approval request (Action ID: {action_id}) has been sent to the user. "
        f"Tell the user you are waiting for their approval to proceed."
    )

def execute_approved_action(action_id: str, tool_registry: dict) -> Any:
    """Executes the tool once the user approves it."""
    if action_id not in PENDING_ACTIONS:
        raise ValueError("Invalid or expired Action ID")
        
    action = PENDING_ACTIONS[action_id]
    if action["status"] != "PENDING":
        raise ValueError("Action has already been processed")
        
    tool_name = action["tool_name"]
    kwargs = action["kwargs"]
    
    # Fetch the actual tool function from your registry
    tool_function = tool_registry.get(tool_name)
    if not tool_function:
        raise ValueError(f"Tool {tool_name} not found")
        
    # Execute it
    result = tool_function(**kwargs)
    
    # Mark as completed
    action["status"] = "COMPLETED"
    action["result"] = result
    
    return result

# ==========================================
# 3. FastAPI Endpoints for the Frontend
# ==========================================
router = APIRouter(prefix="/agent/action", tags=["HITL"])

class ApprovalResponse(BaseModel):
    message: str
    result: Any = None

@router.post("/approve/{action_id}", response_model=ApprovalResponse)
async def approve_action(action_id: str):
    """Frontend calls this when the user clicks 'Approve'."""
    # Note: In reality, you'd pass your tool_registry here or import it
    tool_registry = {} # TODO: Import your actual tool registry mapping
    
    try:
        # We execute the action immediately upon approval
        result = execute_approved_action(action_id, tool_registry)
        return {"message": "Action approved and executed successfully", "result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/reject/{action_id}")
async def reject_action(action_id: str):
    """Frontend calls this when the user clicks 'Reject'."""
    if action_id in PENDING_ACTIONS:
        PENDING_ACTIONS[action_id]["status"] = "REJECTED"
        return {"message": "Action rejected successfully"}
    raise HTTPException(status_code=404, detail="Action not found")
