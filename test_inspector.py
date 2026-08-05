import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock

from mcp import types

from debug.inspector import debug_callback, trigger_sampling_request


class TriggerSamplingRequestTests(unittest.IsolatedAsyncioTestCase):
    async def test_trigger_sampling_request_calls_debug_tool(self):
        session = SimpleNamespace()
        session.call_tool = AsyncMock(return_value=SimpleNamespace(content=[SimpleNamespace(text='ok')]))

        result = await trigger_sampling_request(session, 'hello')

        self.assertEqual(result, 'ok')
        session.call_tool.assert_awaited_once_with('debug_sampling_request', {'input': {'text': 'hello'}})


class DebugCallbackTests(unittest.IsolatedAsyncioTestCase):
    async def test_debug_callback_returns_a_direct_response(self):
        context = SimpleNamespace(
            session=SimpleNamespace(call_tool=AsyncMock(side_effect=AssertionError('nested tool call should not run')))
        )
        params = types.CreateMessageRequestParams(
            messages=[
                types.SamplingMessage(
                    role='user',
                    content=types.TextContent(type='text', text='hello'),
                )
            ],
            maxTokens=80,
        )

        result = await debug_callback(context, params)

        self.assertEqual(result.content.text, 'Debug callback received: hello')
        self.assertEqual(result.role, 'assistant')


if __name__ == '__main__':
    unittest.main()
