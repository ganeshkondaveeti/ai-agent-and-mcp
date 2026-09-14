import asyncio
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession
from langchain_mcp_adapters.tools import load_mcp_tools

async def test_stdio_mcp():
    print("Starting local MCP server via STDIO...")
    server_params = StdioServerParameters(
        command="node",
        args=["scratch/dist/index.js"],
        env=None
    )
    
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            print("Session initialized. Loading LangChain tools...")
            
            tools = await load_mcp_tools(session)
            print(f"✅ Loaded {len(tools)} tools:")
            for tool in tools:
                print(f"  - {tool.name}: {tool.description}")

if __name__ == "__main__":
    asyncio.run(test_stdio_mcp())
