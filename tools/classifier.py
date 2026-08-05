from pydantic import BaseModel
from context_types import ClassificationResult

class ClassifierInput(BaseModel):
    text: str

async def classifier(input: ClassifierInput) -> ClassificationResult:
    content = input.text.lower()
    if 'meeting' in content or 'report' in content:
        category = 'business'
    elif 'system' in content or 'auth code' in content:
        category = 'system'

    elif 'promotion' in content or 'sold' in content:
        category = 'advertisement'
    else:
        category = 'social'

    return ClassificationResult(
        category = category,
        confidence = 0.9
    )