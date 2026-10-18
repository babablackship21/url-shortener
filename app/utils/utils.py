import os
from pathlib import Path


def read_secret_or_env(var_name: str, default: str = "") -> str:
    """Read an environment value or UTF-8 secret file, falling back if empty.

    Raises:
        ValueError: A secret file exists but cannot be read or decoded.
    """
    value = os.environ.get(var_name, "").strip()
    if not value:
        return default
    try:
        path = Path(value)
        if path.is_file():
            return path.read_text(encoding="utf-8").strip() or default
    except (OSError, UnicodeError) as exc:
        raise ValueError(f"Could not read configuration secret for {var_name}.") from exc
    return value
