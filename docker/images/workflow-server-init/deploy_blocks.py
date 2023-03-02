"""
This script automatically configures a number of blocks in the Prefect server
so we don't have to manually configure them using the Prefect UI.
"""

import asyncio
from os import getenv

import dotenv
from prefect.filesystems import Azure


async def deploy_azure_flows_block():
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
    else:
        print(connection_string)

    print("Deploying Azure flows block to Prefect...")

    storage = Azure(
        name="flows",
        bucket_path="flows",
        azure_storage_connection_string=connection_string,
    )

    await storage.save("flows", overwrite=True)


async def main():
    await deploy_azure_flows_block()


if __name__ == "__main__":
    asyncio.run(main())
