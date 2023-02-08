from os import path
import asyncio

import ray
from prefect import flow, get_run_logger, task
from prefect_aws.credentials import MinIOCredentials
from prefect_aws.s3 import S3Bucket


@task
async def download_dataset(input_path: str) -> None:
    logger = get_run_logger()
    temp_path = f"/tmp/{path.basename(input_path)}"
    storage = await S3Bucket.load("raw")
    credentials = await MinIOCredentials.load("datalake-credentials")

    storage.credentials = credentials

    logger.info("Downloading dataset from %s", input_path)

    await storage.download_object_to_path(input_path, temp_path)

    return temp_path


@task
def train(train_file: str) -> None:
    ray.data.read_parquet("/tmp/reviews.parquet").show()


@flow
async def train_model(input_path: str) -> None:
    train_file_path = await download_dataset(input_path)
    await train(train_file_path)


if __name__ == "__main__":
    asyncio.run(train_model())
