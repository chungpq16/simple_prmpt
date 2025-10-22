"""
Configuration management for the GenAI Prompt Generator application.
"""
import os
from typing import Optional
from dotenv import load_dotenv


class Config:
    """Application configuration class."""
    
    def __init__(self):
        """Initialize configuration by loading environment variables."""
        load_dotenv()
        
        # LLM Farm Configuration
        self.api_key = os.getenv('API_KEY')
        self.llm_farm_url = os.getenv('LLM_FARM_URL')
        self.model_name = os.getenv('MODEL_NAME', 'gpt-4o-mini')
        
        # Application Configuration
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
        self.max_tokens = int(os.getenv('MAX_TOKENS', '4096'))
        self.temperature = float(os.getenv('TEMPERATURE', '0'))
        
        # Performance Configuration
        self.timeout_seconds = int(os.getenv('TIMEOUT_SECONDS', '30'))
        self.max_retries = int(os.getenv('MAX_RETRIES', '3'))
        
    def validate(self) -> tuple[bool, Optional[str]]:
        """
        Validate the configuration.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.api_key:
            return False, "API_KEY is required but not set"
        
        if not self.llm_farm_url:
            return False, "LLM_FARM_URL is required but not set"
        
        if not self.llm_farm_url.startswith(('http://', 'https://')):
            return False, "LLM_FARM_URL must be a valid URL"
        
        return True, None
    
    def get_summary(self) -> dict:
        """Get a summary of the current configuration."""
        return {
            "model_name": self.model_name,
            "log_level": self.log_level,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "timeout_seconds": self.timeout_seconds,
            "max_retries": self.max_retries,
            "api_configured": bool(self.api_key),
            "url_configured": bool(self.llm_farm_url)
        }


# Global configuration instance
config = Config()