"""
Logging configuration for the GenAI Prompt Generator application.
"""
import logging
import os
from typing import Optional


def get_logger(name: Optional[str] = None, level: Optional[str] = None) -> logging.Logger:
    """
    Get a configured logger instance.
    
    Args:
        name: Logger name (defaults to __name__)
        level: Log level (defaults to INFO or env LOG_LEVEL)
        
    Returns:
        Configured logger instance
    """
    logger_name = name or __name__
    log_level = level or os.getenv('LOG_LEVEL', 'INFO')
    
    logger = logging.getLogger(logger_name)
    
    if not logger.handlers:
        # Create console handler
        handler = logging.StreamHandler()
        handler.setLevel(log_level)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(handler)
        logger.setLevel(log_level)
    
    return logger