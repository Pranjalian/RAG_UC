import os
import logging
import json
from datetime import datetime

def setup_logger(name: str, config: dict = None) -> logging.Logger:
    """
    Sets up a logger that outputs to both the console and a file.
    
    Args:
        name (str): The name of the logger (e.g., 'pipeline', 'scraper').
        config (dict, optional): The application config dict.
        
    Returns:
        logging.Logger: The configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Avoid adding handlers multiple times if logger already exists
    if logger.handlers:
        return logger

    # Console Handler (Standard Format)
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.INFO)
    c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    logger.addHandler(c_handler)

    # File Handler (JSON Format)
    log_dir = "data/logs"
    if config and "scheduler" in config and "log_dir" in config["scheduler"]:
        log_dir = config["scheduler"]["log_dir"]
        
    os.makedirs(log_dir, exist_ok=True)
    
    log_filename = os.path.join(log_dir, f"{name}_{datetime.now().strftime('%Y-%m-%d')}.log")
    f_handler = logging.FileHandler(log_filename, encoding='utf-8')
    f_handler.setLevel(logging.INFO)
    
    # Custom JSON formatter
    class JSONFormatter(logging.Formatter):
        def format(self, record):
            log_record = {
                "timestamp": self.formatTime(record, self.datefmt),
                "name": record.name,
                "level": record.levelname,
                "message": record.getMessage()
            }
            if record.exc_info:
                log_record["exc_info"] = self.formatException(record.exc_info)
            return json.dumps(log_record)

    f_handler.setFormatter(JSONFormatter())
    logger.addHandler(f_handler)

    return logger
