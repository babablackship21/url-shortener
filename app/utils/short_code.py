import secrets
import string


def generate_short_code(length: int = 6) -> str:
    """Generate a cryptographically random alphanumeric code of positive length.

    Raises:
        ValueError: Length is not a positive integer.
    """
    if isinstance(length, bool) or not isinstance(length, int) or length < 1:
        raise ValueError("Short code length must be a positive integer.")
    alphabet = string.ascii_letters + string.digits
    return "".join(
        secrets.choice(alphabet) for _ in range(length)
    )