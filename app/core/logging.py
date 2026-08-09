import logging
import sys
from pathlib import Path
from app.core.config import settings

def setup_logging(level: str = None) -> logging.Logger:
    """Configures application-wide logging."""
    log_level = level or settings.log_level
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    logger = logging.getLogger("netsec_scanner")
    logger.setLevel(numeric_level)

    # Avoid duplicate handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    # Formatter
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Stream Handler (Console)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(numeric_level)
    logger.addHandler(console_handler)

    # File Handler
    try:
        log_file = Path(settings.log_file_path)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        file_handler.setLevel(numeric_level)
        logger.addHandler(file_handler)
    except Exception as e:
        logger.warning(f"Could not initialize log file handler: {e}")

    return logger

logger = setup_logging()
