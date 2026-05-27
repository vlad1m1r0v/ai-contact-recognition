import logging
import re
from typing import Any, Mapping, MutableMapping, Tuple

# Logger format strictly: "[%(levelname)s] - [%(asctime)s] - [%(filename)s:%(lineno)d] - %(message)s"
LOG_FORMAT = "[%(levelname)s] - [%(asctime)s] - [%(filename)s:%(lineno)d] - %(message)s"
DATE_FORMAT = "%H:%M:%S"


class ConventionLogger(logging.LoggerAdapter):
    """
    Custom LoggerAdapter that automatically enforces message suffix conventions:
    1. If logging a process that is executing, the message must end with three dots (...).
    2. If logging a finished process (failure or success), the message must end with a dot (.)
       and must not end with an exclamation mark.
    """

    def __init__(self, logger: logging.Logger, extra: Mapping[str, Any] = None) -> None:
        super().__init__(logger, extra or {})

    def process(
        self, msg: Any, kwargs: MutableMapping[str, Any]
    ) -> Tuple[Any, MutableMapping[str, Any]]:
        # Default behavior: pass-through if not processed specially
        return msg, kwargs

    def executing(
        self, msg: str, *args: Any, level: int = logging.INFO, **kwargs: Any
    ) -> None:
        """
        Log an executing process. Suffixes the message with '...'.
        """
        cleaned = re.sub(r"[\s.!?;]+$", "", msg)
        self.logger.log(level, f"{cleaned}...", *args, **kwargs)

    def finished(
        self, msg: str, *args: Any, level: int = logging.INFO, **kwargs: Any
    ) -> None:
        """
        Log a completed process (success or failure). Suffixes the message with '.'.
        """
        cleaned = re.sub(r"[\s.!?;]+$", "", msg)
        self.logger.log(level, f"{cleaned}.", *args, **kwargs)


def get_logger(name: str) -> ConventionLogger:
    """
    Get a preconfigured ConventionLogger for the given module name.
    """
    logger = logging.getLogger(name)
    return ConventionLogger(logger)


def setup_logging(level: int = logging.INFO) -> None:
    """
    Set up system-wide basic logging configuration with the strict format and datefmt.
    """
    # Reset existing handlers to prevent duplicates
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logging.basicConfig(level=level, format=LOG_FORMAT, datefmt=DATE_FORMAT)
