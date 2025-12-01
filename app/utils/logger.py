"""
Centralized logging utility for the distributed system
"""
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

# Create logs directory
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

# Configure logging
def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None):
    """
    Setup centralized logging for the application
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file name (defaults to system_YYYYMMDD.log)
    """
    if log_file is None:
        log_file = logs_dir / f"system_{datetime.now().strftime('%Y%m%d')}.log"
    else:
        log_file = logs_dir / log_file
    
    # Create formatter
    formatter = logging.Formatter(
        fmt='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level.upper()))
    console_handler.setFormatter(formatter)
    
    # File handler
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)  # Log everything to file
    file_handler.setFormatter(formatter)
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    return str(log_file)

def get_logger(name: str):
    """Get a logger instance for a module"""
    return logging.getLogger(name)
