"""Optional MCP filesystem toolset over the local docs folder."""

from __future__ import annotations

from campus_assistant.config import DOCS_DIR


def build_docs_mcp_toolset():
    """Connect the agent to the local docs folder through an MCP filesystem server.

    Requires Node.js (`npx`) at runtime. The custom read_campus_doc tool still
    works if MCP is not installed.
    """
    from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
    from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
    from mcp import StdioServerParameters

    return McpToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command="npx",
                args=["-y", "@modelcontextprotocol/server-filesystem", str(DOCS_DIR)],
            ),
            timeout=15,
        ),
        tool_filter=["read_file", "list_directory", "search_files", "get_file_info"],
    )
