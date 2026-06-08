import logging
import os
from datetime import datetime


def get_logger():
    """
    Configure and return application logger.
    """
    os.makedirs("logs",exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = f"logs/run_{timestamp}.log"
    logger = logging.getLogger(f"health_checker_{timestamp}")
    
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )
    
    file_handler = logging.FileHandler(
        log_file
    )
    file_handler.setFormatter(formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logger.info(f"Logger initialized > {log_file}")
    
    return logger