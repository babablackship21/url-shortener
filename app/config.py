from dotenv import load_dotenv
from sqlalchemy.engine import URL
from utils.utils import read_secret_or_env

load_dotenv(override=False)



def get_database_url() -> str:
    """
    Build the SQLAlchemy database URL from environment variables.
    DATABASE_URL takes precedence over individual settings.
    """
    database_url = read_secret_or_env("DATABASE_URL")

    if database_url:
        return database_url

    db_user = read_secret_or_env("POSTGRES_USER")
    db_password = read_secret_or_env("POSTGRES_PASSWORD")
    db_name = read_secret_or_env("POSTGRES_DB")
    db_host = read_secret_or_env("POSTGRES_HOST", "localhost")
    db_port = read_secret_or_env("POSTGRES_PORT", "5432")

    missing = [
        name
        for name, value in {
            "POSTGRES_USER": db_user,
            "POSTGRES_PASSWORD": db_password,
            "POSTGRES_DB": db_name,
        }.items()
        if not value
    ]

    if missing:
        raise ValueError(
            f"Missing required database settings: {', '.join(missing)}"
        )

    try:
        port = int(db_port)
        if not 1 <= port <= 65535:
            raise ValueError
    except ValueError:
        raise ValueError("POSTGRES_PORT must be a valid port number.") from None

    database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    return database_url


def get_safe_browsing_api_key() -> tuple[str, str]:
    """
    Retrieve the Google Safe Browsing API key from environment variables.

    Returns:
        tuple[str, str]: The API endpoint and key.
    Raises:
        ValueError: If the API endpoint or key is not set.
    """
    endpoint = read_secret_or_env("GOOGLE_SAFE_BROWSING_API_URL")
    api_key = read_secret_or_env("GOOGLE_SAFE_BROWSING_API_KEY") 

    if not api_key or not endpoint:
        raise ValueError("GOOGLE_SAFE_BROWSING_API_KEY or GOOGLE_SAFE_BROWSING_API_URL not set.")

    return endpoint, api_key

def get_env() -> str:
    """
    Retrieve the application environment from environment variables.

    Returns:
        str: The application environment (e.g., 'dev', 'prod').
    """
    return read_secret_or_env("ENV", "prod")



def get_api_base_url() -> str:
    """
    Constructs the base URL for the API based on the incoming request.

    Args:
        request: The incoming HTTP request object.
    returns:
        str: The base URL for the API.
    """
    
    return read_secret_or_env("API_BASE_URL", "http://localhost/api")



DATABASE_URL = get_database_url()
GOOGLE_SAFE_BROWSING_API_URL, GOOGLE_SAFE_BROWSING_API_KEY = get_safe_browsing_api_key()
ENV = get_env()
BASE_URL =get_api_base_url()
