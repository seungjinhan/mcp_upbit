#!/usr/bin/env python3
# Hello World MCP Server in Python
from typing import Any
from datetime import datetime, timedelta
import json
import urllib.parse
import math
import asyncio
from mcp.server.fastmcp import FastMCP
import os

# Initialize FastMCP server
mcp = FastMCP("mcp_upbit")


@mcp.tool() 
async def get_find_stock(stock_name:str):
    return "Hello World! " + stock_name

if __name__ == "__main__":
    mcp.run(transport="stdio")