from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# The definition of general mail structure
class MailMeta(BaseModel):
    sender: str = Field(..., description="Sender email address")
    receiver: str = Field(..., description="Receiver email address")
    subject: str = Field(..., description="Email subject")
    timestamp: datetime = Field(..., description="Email datetime")

class MailBody(BaseModel):
    plain_text: str = Field(..., description="Email content")
    html: Optional[str] = Field(default=None, description="HTML content(if any)")

class MailAttachment(BaseModel):
    filename: str = Field(..., description="Attachment name")
    filetype: str = Field(..., description="File type, e.g. pdf, jpg")
    filesize_kb: str = Field(..., description="File size(KB)")

class MailContext(BaseModel):
    meta: MailMeta
    body: MailBody
    attachments: Optional[List[MailAttachment]] = Field(default_factory=list)

class ClassificationResult(BaseModel):
    category: str = Field(..., description="Email category: e.g. business, system, advertisement")
    confidence: float = Field(..., description="Classified confidence")

# Abstract result
class SummaryResult(BaseModel):
    summary: str = Field(..., description="Generated summary result")

# Suggested reply structure
class ReplyCandidate(BaseModel):
    reply_text: str = Field(..., description="Suggested reply")
    intent: Optional[str] = Field(None, description="Intent types")

# Archive structure
class ArchiveMetadata(BaseModel):
    folder: str = Field(..., description="Archive folder name")
    tags: List[str] = Field(..., description="Archive tags")

