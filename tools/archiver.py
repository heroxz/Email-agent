from pydantic import BaseModel
from context_types import ArchiveMetadata

class ArchiveInput(BaseModel):
    text: str

async def archiver(input: ArchiveInput) -> ArchiveMetadata:
    folder = 'business'
    tags = ['project', 'summary', 'process complete']
    return ArchiveMetadata(
        folder = folder,
        tags = tags
    )