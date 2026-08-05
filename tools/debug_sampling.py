from pydantic import BaseModel
from mcp import types
from mcp.server.fastmcp import Context



class DebugSamplingInput(BaseModel):
    text: str


async def debug_sampling_request(input: DebugSamplingInput, ctx: Context) -> str:
    """Ask the client for a sampling response and return the result."""
    #logger.info(f'{inspect.stack()[0].function}[Input] {input.text}')
    result = await ctx.session.create_message(
        messages=[
            types.SamplingMessage(
                role='user',
                content=types.TextContent(type='text', text=input.text),
            )
        ],
        max_tokens=80,
        system_prompt='You are a debug helper.',
    )
    return result.content.text
