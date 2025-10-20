from mcp import stdio_client, StdioServerParameters
from strands.tools.mcp import MCPClient
import os
from pathlib import Path


def get_sec_edgar_mcp_client():
    """Get MCPClient connected to SEC EDGAR MCP server."""
    sec_edgar_path = Path("/home/amorelli/development/sec-edgar-mcp")

    if not sec_edgar_path.exists():
        raise FileNotFoundError(
            f"SEC EDGAR MCP server not found at {sec_edgar_path}. "
            "Clone from https://github.com/stefanoamorelli/sec-edgar-mcp"
        )

    server_script = sec_edgar_path / "sec_edgar_mcp" / "server.py"

    if not server_script.exists():
        raise FileNotFoundError(
            f"SEC EDGAR server script not found at {server_script}"
        )

    user_agent = os.getenv("SEC_EDGAR_USER_AGENT")
    if not user_agent:
        raise ValueError("SEC_EDGAR_USER_AGENT environment variable is required")

    return MCPClient(lambda: stdio_client(
        StdioServerParameters(
            command="python",
            args=[str(server_script)],
            env={"SEC_EDGAR_USER_AGENT": user_agent}
        )
    ))


def get_fred_mcp_client():
    """Get MCPClient connected to FRED MCP server."""
    fred_path = Path("/home/amorelli/development/fred-mcp-server")

    if not fred_path.exists():
        raise FileNotFoundError(
            f"FRED MCP server not found at {fred_path}. "
            "Clone from https://github.com/stefanoamorelli/fred-mcp-server"
        )

    server_script = fred_path / "build" / "index.js"

    if not server_script.exists():
        raise FileNotFoundError(
            f"FRED server script not found at {server_script}. "
            "Run 'pnpm install && pnpm build' in the fred-mcp-server directory"
        )

    fred_api_key = os.getenv("FRED_API_KEY")
    if not fred_api_key:
        raise ValueError("FRED_API_KEY environment variable is required")

    return MCPClient(lambda: stdio_client(
        StdioServerParameters(
            command="node",
            args=[str(server_script)],
            env={"FRED_API_KEY": fred_api_key}
        )
    ))


def get_combined_mcp_tools():
    """
    Get tools from both SEC EDGAR and FRED MCP servers.

    Returns a tuple of (sec_client, fred_client, combined_tools).
    Use within a context manager:

    Example:
        sec_client, fred_client, tools = get_combined_mcp_tools()
        with sec_client, fred_client:
            agent = Agent(tools=tools)
            response = agent("Your query")
    """
    sec_client = get_sec_edgar_mcp_client()
    fred_client = get_fred_mcp_client()

    with sec_client, fred_client:
        sec_tools = sec_client.list_tools_sync()
        fred_tools = fred_client.list_tools_sync()
        combined_tools = sec_tools + fred_tools

    return sec_client, fred_client, combined_tools
