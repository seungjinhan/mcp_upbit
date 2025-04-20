from typing import Any
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("mcp_upbit")


@mcp.tool() 
async def get_find_stock(stock_name:str):
    return "Hello World! " + stock_name

if __name__ == "__main__":
    mcp.run(transport="stdio")