from pydantic import BaseModel
from context_types import ReplyCandidate

class ReplyInput(BaseModel):
    text: str

async def reply_generator(input: ReplyInput) -> ReplyCandidate:
    reply = 'Hello, email received, will process as soon as possible. Thanks!'
    return ReplyCandidate(
        reply_text = reply, intent = 'Confirm'
    )