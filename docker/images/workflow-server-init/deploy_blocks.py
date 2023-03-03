"""
This script automatically configures a number of blocks in the Prefect server
so we don't have to manually configure them using the Prefect UI.
"""

import asyncio
from os import getenv

import dotenv
from prefect.filesystems import Azure


async def deploy_azure_block(name: str, path: str) -> None:
    """
    Deploys an Azure block to the Prefect environment that points to the `flows`
    container in the Azure Storage Account Emulator.

    The flows container is used to store prefect flow deployments.
    """

    dotenv.load_dotenv()

    connection_string = getenv("AZURE_CONNECTION_STRING", "")

    if connection_string == "":
        print("AZURE_CONNECTION_STRING environment variable not set.")
        exit(1)

    print(f"Deploying Azure block '{name}' to Prefect...")

    storage = Azure(
        name=name,
        bucket_path=path,
        azure_storage_connection_string=connection_string,
    )

    await storage.save(name, overwrite=True)


async def main():
    await deploy_azure_block("flows", "flows")
    await deploy_azure_block("raw", "raw")

if __name__ == "__main__":
    asyncio.run(main())
