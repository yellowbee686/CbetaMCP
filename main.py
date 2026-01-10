import os
import pathlib
import importlib
from fastapi import FastAPI
from fastmcp import FastMCP

# Initialize FastAPI & MCP Server
app = FastAPI(title="MCP Tool Aggregation Service", version="0.2.0")

# Create MCP server instance
mcp = FastMCP(name="CBETA MCP Tools")

# Export for tool registration in other modules
__mcp_server__ = mcp

# Common response structures
def success_response(result: dict) -> dict:
    return {"status": "success", "result": result}

def error_response(message: str) -> dict:
    return {"status": "error", "message": message}

# Track registered tool names to detect duplicates
registered_tool_names: set[str] = set()

def recursive_import_tools(base_dir: str = "tools") -> None:
    """Recursively import all tool modules from the specified directory."""
    base_path = pathlib.Path(base_dir)
    for path in base_path.rglob("*.py"):
        if path.name.startswith("_"):  # Skip __init__.py and _xxx.py
            continue
        module_parts = path.with_suffix("").parts
        module_path = ".".join(module_parts)
        try:
            mod = importlib.import_module(module_path)
            for attr_name in dir(mod):
                attr = getattr(mod, attr_name)
                if callable(attr) and getattr(attr, "_is_mcp_tool", False):
                    if attr.__name__ in registered_tool_names:
                        print(f"⚠️ Duplicate MCP tool registration: `{attr.__name__}` from module: {module_path}")
                    else:
                        registered_tool_names.add(attr.__name__)
        except Exception as e:
            print(f"❌ Module import failed: {module_path}, error: {e}")

# Import all tool modules
recursive_import_tools()

# Mount MCP server to FastAPI app at /mcp path
# The http_app() returns an ASGI app that supports SSE transport
mcp_app = mcp.http_app(path="/sse")
app.mount("/mcp", mcp_app)

# Start server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("APP_PORT", "8000")))
