import logging
import sys

from config import ENV


def config_logger():
    """Configure stdout logging at DEBUG in development and INFO otherwise."""
    level = logging.DEBUG if ENV in {"debug", "dev"} else logging.INFO
    logging.basicConfig(
        stream=sys.stdout,
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s - %(message)s",
    )
