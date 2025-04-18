import os


def get_required_env_var(key: str) -> str:
    """
    Retrieve a required environment variable.

    Args:
        key (str): The name of the environment variable to fetch.

    Returns:
        str: The value of the environment variable.

    Raises:
        ValueError: If the environment variable is not set or is empty.

    Example:
        >>> os.environ["DB_HOST"] = "localhost"
        >>> get_required_env_var("DB_HOST")
        'localhost'

        >>> get_required_env_var("MISSING_VAR")
        ValueError: MISSING_VAR environment variable is required.
    """
    value = os.getenv(key)
    if not value:
        raise ValueError(f"{key} environment variable is required.")
    return value
