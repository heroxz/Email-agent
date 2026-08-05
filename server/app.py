import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mcp.server.fastmcp import FastMCP

# Import MCP tools
from tools.mail_parser import mail_parser
from tools.classifier import classifier
from tools.summarizer import summarizer
from tools.reply_generator import reply_generator
from tools.archiver import archiver
from tools.debug_sampling import debug_sampling_request

# Create FastMCP instance (server name: mail-agent)
app = FastMCP('mail-agent')

# Register tools using the current decorator API
app.tool()(mail_parser)
app.tool()(classifier)
app.tool()(summarizer)
app.tool()(reply_generator)
app.tool()(archiver)
app.tool()(debug_sampling_request)

if __name__ == '__main__':
    app.run()

