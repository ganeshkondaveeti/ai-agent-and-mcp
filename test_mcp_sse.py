import asyncio
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession

async def test_mcp():
    url = "https://mcp-server-4-production-c42d.up.railway.app/sse"
    print(f"Connecting to {url}...")
    
    async with sse_client(url) as streams:
        async with ClientSession(streams[0], streams[1]) as session:
            await session.initialize()
            
            response = await session.list_tools()
            print("Tools available:")
            for tool in response.tools:
                print(f" - {tool.name}: {tool.description}")

if __name__ == "__main__":
    asyncio.run(test_mcp())
