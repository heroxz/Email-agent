from datetime import datetime
from pydantic import BaseModel
from context_types import MailContext, MailMeta, MailBody

class MainParserInput(BaseModel):
    raw_text: str

async def mail_parser(input: MainParserInput) -> MailContext:
    # Fake parser. 
    return MailContext(
        meta = MailMeta(
            sender = "user@example.com",
            receiver = "bot@example.com",
            subject = "Test mail",
            timestamp=datetime.utcnow()
        ),
        body = MailBody(
            plain_text = input.raw_text
        )
    )

