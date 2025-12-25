from src.state import get_context, update_stage, set_ticket, WorkflowStage
from src.config import settings

def handle_start(args: str) -> str:
    """Handle /start [TicketID] [Desc] command"""
    try:
        ticket, desc = args.split(" ", 1)
        set_ticket(ticket, desc)
        update_stage(WorkflowStage.PLANNING)
        return (
            f"🚀 **STARTED**: Ticket `{ticket}`\n"
            f"Context: {desc}\n"
            f"Current Stage: **PLANNING**\n"
            f"👉 Next Step: Use `/plan {ticket}` to generate implementation plan."
        )
    except ValueError:
        return "❌ Error: Format must be `/start [TicketID] [Description]`"

def handle_plan(args: str) -> str:
    ctx = get_context()
    if ctx.current_stage != WorkflowStage.PLANNING:
        return f"⛔ **VIOLATION**: You are in {ctx.current_stage.value}. You must `/start` first."
    
    # Here we can call AI Big Brain to generate plan (simulation)
    return (
        f"📝 **PLAN GENERATED** for `{ctx.active_ticket}`\n"
        f"- Created: docs/specs/{ctx.active_ticket}.md\n"
        f"👉 Next Step: Use `/test` to generate unit tests."
    )

def handle_test(args: str) -> str:
    ctx = get_context()
    # Rule: Must have Plan before Test (optional)
    if ctx.current_stage != WorkflowStage.PLANNING: 
         return f"⛔ **VIOLATION**: Please finish Planning first."

    update_stage(WorkflowStage.TESTING)
    return (
        f"🧪 **TESTS GENERATED**\n"
        f"State transitioned to: **TESTING**\n"
        f"👉 Next Step: Run tests to see them fail, then use `/impl`."
    )

def handle_impl(args: str) -> str:
    ctx = get_context()
    # Rule: Strict TDD - Must be in TESTING state before Coding
    if settings.STRICT_MODE and ctx.current_stage != WorkflowStage.TESTING:
        return f"⛔ **STRICT MODE BLOCK**: You MUST generate tests (`/test`) before implementing code."

    update_stage(WorkflowStage.CODING)
    return (
        f"🔨 **IMPLEMENTING CODE**\n"
        f"State transitioned to: **CODING**\n"
        f"I am now allowed to write implementation logic for `{ctx.active_ticket}`."
    )
