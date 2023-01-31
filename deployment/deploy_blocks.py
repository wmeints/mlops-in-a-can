from os import getenv
from dotenv import load_dotenv
import asyncio
from prefect_aws.s3 import S3Bucket
from prefect_aws.credentials import MinIOCredentials
from pydantic import SecretStr


async def deploy_bucket(name: str, bucket_name: str, credentials: MinIOCredentials) -> None:
    storage = S3Bucket(
        name=name,
        minio_credentials=credentials,
        bucket_name=bucket_name)

    await storage.save(name, overwrite=True)


async def deploy_datalake_credentials():
    load_dotenv()

    root_password = getenv("MINIO_ROOT_PASSWORD")
    root_username = getenv("MINIO_ROOT_USER")

    credentials = MinIOCredentials(
        name='datalake-credentials',
        minio_root_password=SecretStr(root_password),
        minio_root_user=root_username,
        aws_client_parameters={
            "use_ssl": False,
            "api_version": None,
            "config": None,
            "verify": False,
            "endpoint_url": "http://datalake:9000"
        }
    )

    await credentials.save('datalake-credentials', overwrite=True)

    return credentials


async def main():
    datalake_credentials = await deploy_datalake_credentials()

    await deploy_bucket("raw", "raw", datalake_credentials)
    await deploy_bucket("intermediate", "intermediate",  datalake_credentials)
    await deploy_bucket("cleaned", "cleaned", datalake_credentials)
    await deploy_bucket("flows", "flows", datalake_credentials)


if __name__ == '__main__':
    asyncio.run(main())
