import logging
import os
from datetime import datetime

LOG_DIR = 'logs'
LOG_FILE = os.path.join(LOG_DIR, f'mcp_mailagent_{datetime.now().strftime('%Y%m%d_%H%M%S')}')

os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger('mcp-mailagent')
logger.setLevel(logging.DEBUG)

# Process log files
file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
file_handler.setLevel(logging.INFO)

# Process console logs
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Log format
formatter = logging.Formatter(
    fmt = '[%(asctime)s][%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%D'
)

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)