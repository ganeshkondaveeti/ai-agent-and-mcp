import asyncio
from mcp.client.streamable_http import streamable_http_client
from mcp.client.session import ClientSession

import httpx

async def test_mcp():
    url = "https://mcp-server-4-production-c42d.up.railway.app/mcp"
    print(f"Connecting to {url}...")
    
    try:
        async with streamable_http_client(url) as streams:
            async with ClientSession(streams[0], streams[1]) as session:
                await session.initialize()
                
                response = await session.list_tools()
                print("Tools available:")
                for tool in response.tools:
                    print(f" - {tool.name}: {tool.description}")
    except httpx.HTTPStatusError as e:
        print(f"HTTPStatusError: {e}")
        print(f"Response: {e.response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_mcp())
