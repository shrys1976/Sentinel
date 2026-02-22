import logging
import sys
from pathlib import Path

_BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent
LOG_DIR = _BACKEND_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)


def setup_logging() -> None:
    # Idempotent initialization: uvicorn reloads should not duplicate handlers.
    root_logger = logging.getLogger()
    if getattr(root_logger, "_sentinelai_logging_configured", False):
        return

    log_format = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    formatter = logging.Formatter(log_format)

    root_logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(LOG_DIR / "app.log")
    file_handler.setFormatter(formatter)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    setattr(root_logger, "_sentinelai_logging_configured", True)
