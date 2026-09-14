import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator, List
from langchain_core.tools import BaseTool
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession
from langchain_mcp_adapters.tools import load_mcp_tools

# Default to the user's deployed Railway URL
# Note: The server must implement standard MCP SSE at this endpoint.
DEFAULT_MCP_SERVER_URL = "https://mcp-server-4-production-c42d.up.railway.app/sse"

@asynccontextmanager
async def get_mcp_tools(url: str = None) -> AsyncGenerator[List[BaseTool], None]:
    """
    Connects to a remote MCP Server via SSE, initializes the session,
    loads the tools into LangChain BaseTool format, and yields them.
    
    The connection is kept alive for the duration of the context manager.
    
    Usage:
        async with get_mcp_tools() as tools:
            agent.invoke({"messages": ..., "tools": tools})
    """
    mcp_url = url or os.getenv("MCP_SERVER_URL", DEFAULT_MCP_SERVER_URL)
    
    print(f"🔗 Connecting to MCP Server at {mcp_url}...")
    
    # Use long timeouts because agent processing (LLM calls) can take minutes before using MCP tools
    async with sse_client(mcp_url, timeout=60.0, sse_read_timeout=3600.0) as streams:
        async with ClientSession(streams[0], streams[1]) as session:
            await session.initialize()
            
            # Load tools using langchain-mcp-adapters
            tools = await load_mcp_tools(session)
            
            print(f"✅ Successfully connected and loaded {len(tools)} MCP tools:")
            for tool in tools:
                print(f"  - {tool.name}")
                
            yield tools
