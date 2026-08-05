from pydantic import BaseModel
from context_types import SummaryResult

class SummarizerInput(BaseModel):
    text: str

async def summarizer(input: SummarizerInput) -> SummaryResult:
    summary = input.text[:60].strip() + '...' if len(input.text) > 60 else input.text
    return SummaryResult(
        summary = summary
    )
