from enum import Enum
from pydantic import BaseModel
from typing import Optional

class WorkflowStage(str, Enum):
    IDLE = "IDLE"           # Not doing anything yet
    PLANNING = "PLANNING"   # Planning phase (/start -> /plan)
    TESTING = "TESTING"     # Writing tests (/test)
    CODING = "CODING"       # Writing code (/impl)
    REVIEW = "REVIEW"       # Reviewing (/review)

class WorkflowContext(BaseModel):
    current_stage: WorkflowStage = WorkflowStage.IDLE
    active_ticket: Optional[str] = None
    feature_description: Optional[str] = None

# In-memory storage (Need Redis if you want to persist when restarting IDE)
_context = WorkflowContext()

def get_context() -> WorkflowContext:
    return _context

def update_stage(stage: WorkflowStage):
    _context.current_stage = stage

def set_ticket(ticket: str, desc: str):
    _context.active_ticket = ticket
    _context.feature_description = desc
