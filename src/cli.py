import os
import sys
from pathlib import Path

# Define global config file path
CONFIG_PATH = Path.home() / ".ai_workflow_env"


def print_help():
    """Print usage instructions to screen"""
    help_text = """
🛡️  AI Workflow CLI - The Disciplined Agent Guard

Usage:
  workflow-cli [COMMAND]

Commands:
  configure    Set up API Key and environment settings (Global Config).
  server       Start MCP Server (Default if no command specified).

Options:
  --help, -h   Display this message.
  --version    Show version.

Examples:
  workflow-cli configure    # Run first time to setup key
  workflow-cli              # IDE will run this command (you don't need to run manually)
"""
    print(help_text)


def configure():
    """Interactive setup for environment variables."""
    print(f"🛠️  AI Workflow CLI Configuration")
    print(f"💾 Config file location: {CONFIG_PATH}")
    print("-" * 40)

    # 1. Input
    gemini_key = input("Enter GEMINI_API_KEY (Leave empty to keep current): ").strip()
    brave_key = input("Enter BRAVE_API_KEY (Optional): ").strip()
    strict_mode = input("Enable STRICT_MODE? (y/n, default: y): ").strip().lower()

    # 2. Read old config (if exists) to avoid overwriting if user enters empty
    current_config = {}
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    current_config[k] = v

    # 3. Update new values
    if gemini_key:
        current_config["GEMINI_API_KEY"] = gemini_key
    if brave_key:
        current_config["BRAVE_API_KEY"] = brave_key
    
    # Handle strict mode
    if strict_mode == 'n':
        current_config["STRICT_MODE"] = "false"
    elif strict_mode == 'y':
        current_config["STRICT_MODE"] = "true"
    # If no input, keep current or default to true if not set
    elif "STRICT_MODE" not in current_config:
        current_config["STRICT_MODE"] = "true"

    # 4. Write file
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            for k, v in current_config.items():
                f.write(f"{k}={v}\n")
        print(f"✅ Configuration saved successfully!")
    except Exception as e:
        print(f"❌ Error saving config: {e}")
        sys.exit(1)

# Entry point for CLI command
def main():
    # Check input parameters
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        
        if cmd == "configure":
            configure()
            return
        elif cmd in ["--help", "-h"]:
            print_help()
            return
        elif cmd in ["--version", "-v"]:
            print("Workflow CLI v0.1.0")
            return
    
    # Default: If no parameter or unknown parameter -> Run Server
    # This is the behavior for IDE to call the tool
    from src.server import main as server_main
    server_main()

if __name__ == "__main__":
    main()
