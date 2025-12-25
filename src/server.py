from mcp.server.fastmcp import FastMCP
from src.config import settings
from src.handlers import handle_start, handle_plan, handle_test, handle_impl

# Initialize MCP Server
mcp = FastMCP("WorkflowGuard")

@mcp.tool()
def workflow_command(command: str, args: str = "") -> str:
    """
    CENTRAL DISPATCHER: Use only this tool for all development requests.
    
    Args:
        command: Command name (start, plan, test, impl). No need for '/' prefix.
        args: Associated parameters.
    """
    cmd = command.lower().replace("/", "").strip()
    
    print(f"DEBUG: Received command '{cmd}' with args '{args}'") # Log into IDE's console

    if cmd == "start":
        return handle_start(args)
    elif cmd == "plan":
        return handle_plan(args)
    elif cmd == "test":
        return handle_test(args)
    elif cmd == "impl":
        return handle_impl(args)
    else:
        return (
            f"⚠️ **Unknown Command**: `/{cmd}`\n"
            f"Available commands:\n"
            f"- `/start [ticket] [desc]`\n"
            f"- `/plan`\n"
            f"- `/test`\n"
            f"- `/impl`"
        )

def main():
    # Load config check
    print(f"Workflow Agent Starting... Strict Mode: {settings.STRICT_MODE}")
    mcp.run()

if __name__ == "__main__":
    main()
