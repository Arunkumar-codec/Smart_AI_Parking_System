import logging
import sys

from backend.app.core.config import settings


class CorrelationIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, "correlation_id"):
            record.correlation_id = "N/A"
        return True


def setup_logging() -> logging.Logger:
    logger = logging.getLogger("spms")
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
    logger.propagate = False

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s [%(levelname)s] [%(name)s] "
                "[correlation_id=%(correlation_id)s]: %(message)s"
            )
        )
        handler.addFilter(CorrelationIdFilter())
        logger.addHandler(handler)

    return logger


logger = setup_logging()
