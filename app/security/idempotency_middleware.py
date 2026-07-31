import hashlib
import json
from functools import wraps
from typing import Any, Callable

# Simple in-memory store for demonstration. Move to Redis for production.
PROCESSED_KEYS = {}

def with_idempotency(func: Callable) -> Callable:
    """
    Decorator to prevent a tool from executing the exact same action twice.
    It generates a hash based on the tool arguments.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        # 1. Generate a unique key based on the function name and its arguments
        # We use a hash so that if the LLM retries the exact same arguments, we catch it.
        payload = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True, default=str)
        key_hash = hashlib.sha256(f"{func.__name__}:{payload}".encode()).hexdigest()
        
        # 2. Check if we've already processed this exact action recently
        if key_hash in PROCESSED_KEYS:
            print(f"[IDEMPOTENCY] Blocked duplicate execution of {func.__name__}")
            # Return the cached successful result to trick the LLM into thinking it succeeded
            return PROCESSED_KEYS[key_hash]
            
        # 3. Execute the function
        result = await func(*args, **kwargs)
        
        # 4. Save the result so we don't do it again
        PROCESSED_KEYS[key_hash] = result
        return result
        
    return wrapper

# Usage Example:
# @with_idempotency
# async def send_email(to: str, body: str):
#     # actual logic
