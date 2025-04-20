import smithery
import mcp
from mcp.client.websocket import websocket_client
import asyncio

# Create Smithery URL with server endpoint
url = smithery.create_smithery_url("https://server.smithery.ai/@seungjinhan/mcp_upbit/ws", {}) + "&api_key=848c9d80-eba1-4bec-b124-78a8f377d100"

async def main():
    # Connect to the server using websocket client
    async with websocket_client(url) as streams:
        async with mcp.ClientSession(*streams) as session:
            # List available tools
            tools_result = await session.list_tools()
            print(f"Available tools: {', '.join([t.name for t in tools_result.tools])}")
            
            # Example: Call a tool
            # result = await session.call_tool("tool_name", {"param1": "value1"})

if __name__ == "__main__":
    asyncio.run(main())