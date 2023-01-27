from os import getenv
from dotenv import load_dotenv
from prefect.blocks.system import Secret
from prefect.blocks.system import String


def get_secret_value(name: str) -> str:
    """Gets a secret value from the prefect or your local environment.

    Args:
        name (str): The nameo of the secret to get.

    Returns:
        str: The value for the secret. None if it wasn't configured or available.
    """
    load_dotenv()
    
    if getenv('PREFECT_API_URL') is not None:
        return Secret.load(name)
    else:
        return getenv(name.replace('-', '_').upper())


def get_config_value(name: str) -> str:
    """Gets a config value from the prefect or your local environment.

    Args:
        name (str): The name of the configuration variable to get.

    Returns:
        str: The value for the configuration variable. None if it wasn't configured or available.
    """
    if getenv('PREFECT_API_URL') is not None:
        return String.load(name)
    else:
        return getenv(name.replace('-', '_').upper())
