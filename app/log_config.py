import logging
import os
import sys


def configure_logging():
    """Set stdout defaults and level while preserving existing server handlers."""
    level = logging.DEBUG if os.getenv("ENV", "prod") in {"debug", "dev"} else logging.INFO
    logging.basicConfig(
        stream=sys.stdout,
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s - %(message)s",
    )
    logging.getLogger().setLevel(level)
