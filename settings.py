from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Optional

class AppSettings(BaseSettings):
    """Application settings loaded from environment variables."""

    # DeepSeek-v4-flash settings
    DeepSeek_api_key: str = Field(..., env='DEEPSEEK_API_KEY')
    DeepSeek_base_url: str = Field('https://api.deepseek.com', env='DEEPSEEK_BASE_URL')
    DeepSeek_model: str = Field('DeepSeek-v4-flash', env='DEEPSEEK_MODEL')

    # Log level
    log_level: str = Field('INFO', env='LOG_LEVEL')

    # Prompt path (if any)
    prompt_path: Optional[str] = Field('prompt_templates/', env='PROMPT_PATH')

    # Max context length for the model
    max_context_length: int = Field(4096, env='MAX_CONTEXT_LENGTH')

    # If use debug mode
    debug_mode: bool = Field(False, env='DEBUG_MODE')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

# Instantiate the settings object   
settings = AppSettings()
