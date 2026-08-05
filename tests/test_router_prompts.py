import asyncio
import unittest
from types import SimpleNamespace

import router


class DummySession:
    async def call_tool(self, intent, arguments):
        return SimpleNamespace(content=[SimpleNamespace(text="tool fallback")])


class RouterPromptTests(unittest.TestCase):
    def test_reply_prompt_is_used_for_reply_requests(self):
        captured = {}

        async def fake_generate(prompt, intent):
            captured["prompt"] = prompt
            captured["intent"] = intent
            return "Model reply"

        original = router.generate_with_model
        router.generate_with_model = fake_generate
        try:
            result = asyncio.run(router.route_message(DummySession(), "Please reply to this email."))
        finally:
            router.generate_with_model = original

        self.assertEqual(result, "Model reply")
        self.assertEqual(captured["intent"], "reply_generator")
        self.assertIn("Generated reply:", captured["prompt"])
        self.assertIn("Please reply to this email.", captured["prompt"])


if __name__ == "__main__":
    unittest.main()
