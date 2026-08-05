import asyncio
import inspect
import os
import sys


from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from client.session import create_session
from mcp.types import CreateMessageRequestParams, CreateMessageResult, TextContent
from mcp.shared.context import RequestContext
from mcp import ClientSession
from router import route_message
from debug.logger import logger
from config.settings import settings


async def trigger_sampling_request(session: ClientSession, text: str) -> str:
    """Ask the server to issue a sampling request back to the client."""
    logger.info('Entering trigger_sampling_request with text: %s', text)
    response = await session.call_tool(
        'debug_sampling_request',
        {'input': {'text': text}},
    )
    logger.info('Sampling request response: %s', response)
    if response.content:
        return response.content[0].text
    return ''

async def debug_callback(
        context: RequestContext[ClientSession, None],
        params: CreateMessageRequestParams
) -> CreateMessageResult:
    text = params.messages[0].content.text.strip()
    logger.info(f'params: {params}')
    logger.info(f'{inspect.stack()[0].function}[Input] {text}')

    return CreateMessageResult(
        role='assistant',
        content=TextContent(type='text', text=f'Debug callback received: {text}'),
        model='debug-agent',
        stopReason='endTurn',
    )

async def debug_main():
    #session = await create_session(callback=debug_callback)
    print(settings.DeepSeek_api_key)
    print(settings.DeepSeek_base_url)
    async with create_session(callback=debug_callback) as session:
        try:
            await session.initialize()
            print('[Debug Mode] Input any content to trigger calling summarizer, enter quit to exit')
            while True:
                user_input = input('Email content>').strip()
                if user_input.lower() == 'quit':
                    break
                #await session.inject_text(user_input)
                response_text = await route_message(session, user_input)
                if response_text:
                    logger.info("Assistant:%s", response_text)
                else:
                    logger.info('Assistant: <no content returned>')

                try:
                    sampling_result = await trigger_sampling_request(session, user_input)
                    if sampling_result:
                        logger.info('Sampling callback result: %s', sampling_result)
                except Exception as exc:
                    logger.exception('Sampling request failed: %s', exc)

        finally:
            await session._exit_stack.aclose()

if __name__ == '__main__':
    asyncio.run(debug_main())
