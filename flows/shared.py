from os import getenv
from dotenv import load_dotenv
from prefect.blocks.system import Secret
from prefect.blocks.system import String


async def get_secret_value(name: str) -> str:
    """Gets a secret value from the prefect or your local environment.

    Args:
        name (str): The nameo of the secret to get.

    Returns:
        str: The value for the secret. None if it wasn't configured or available.
    """
    if getenv('PREFECT_API_URL') is not None:
        result = await Secret.load(name)
        return result.value.get_secret_value()
    else:
        load_dotenv()
        return getenv(name.replace('-', '_').upper())


async def get_config_value(name: str) -> str:
    """Gets a config value from the prefect or your local environment.

    Args:
        name (str): The name of the configuration variable to get.

    Returns:
        str: The value for the configuration variable. None if it wasn't configured or available.
    """
    if getenv('PREFECT_API_URL') is not None:
        result = await String.load(name)
        return result.value
    else:
        load_dotenv()
        return getenv(name.replace('-', '_').upper())
