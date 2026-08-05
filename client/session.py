import os
import sys
import asyncio
from contextlib import asynccontextmanager
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters
from mcp.types import CreateMessageRequestParams, CreateMessageResult, TextContent
#from mcp.shared.context import RequestContext
from mcp.server.fastmcp import FastMCP, Context

server_params = StdioServerParameters(
    command=sys.executable,
    args=[os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'server', 'app.py'))],
)

# Callback function to handle the user's input
async def default_callback(
        context: Context[ClientSession, None],
        params: CreateMessageRequestParams
) -> CreateMessageResult:
    text = params.messages[0].content.text
    return CreateMessageResult(
        role = 'assistant',
        content = TextContent(type='text', text=f'Received: {text}'),
        model = 'echo-agent',
        stopReason = 'endTurn'
    )

# Outter caller: Create the session
@asynccontextmanager
async def create_session(callback=default_callback) -> ClientSession:
    async with stdio_client(server_params) as (stdio, write):
        async with ClientSession(stdio, write, sampling_callback=callback) as session:
            yield session

# async def create_session(callback=default_callback) -> ClientSession:
#     stdio, write = await stdio_client(server_params).__aenter__()
#     session = ClientSession(stdio, write, sampling_callback=callback)
#     return session

