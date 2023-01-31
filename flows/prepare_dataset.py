import asyncio
from datetime import datetime
from os import makedirs, path
from typing import Tuple
import uuid

import pandas as pd
from prefect import flow, task
from prefect.logging import get_run_logger
from prefect_aws.credentials import MinIOCredentials
from prefect_aws.s3 import S3Bucket
from sklearn.model_selection import train_test_split


@task
async def download_dataset(path: str) -> pd.DataFrame:
    """Downloads the dataset.

    Returns:
        dd.DataFrame: The dataset.
    """

    logger = get_run_logger()
    storage = await S3Bucket.load("raw")
    credentials = await MinIOCredentials.load("datalake-credentials")

    storage.credentials = credentials

    logger.info("Downloading the data from %s", path)

    await storage.download_object_to_path(path, '/tmp/reviews.csv')
    df = pd.read_csv('/tmp/reviews.csv')

    return df


@task
async def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans the data.

    Args:
        df (dd.DataFrame): The data to clean.

    Returns:
        dd.DataFrame: The cleaned data.
    """

    df = df.drop(columns=[
        'ProfileName',
        'UserId',
        'ProductId',
        'Id',
        'HelpfulnessNumerator',
        'HelpfulnessDenominator',
        'Time',
        'Summary'])

    return df


@task
async def split_dataset(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Splits the dataset.

    Args:
        df (dd.DataFrame): The dataset to split.

    Returns:
        dd.DataFrame: The split dataset.
    """

    df_train, df_test = train_test_split(
        df, test_size=0.2, shuffle=True, stratify=df['Score'])

    return df_train, df_test


@task
async def save_dataset(df: pd.DataFrame, output_path: str) -> None:
    logger = get_run_logger()
    storage = await S3Bucket.load("cleaned")
    credentials = await MinIOCredentials.load("datalake-credentials")
    temp_output_path = f"/tmp/{uuid.uuid4()}.parquet"

    storage.credentials = credentials

    logger.info("Saving the output to %s", temp_output_path)

    makedirs(path.dirname(temp_output_path), exist_ok=True)

    df.to_parquet(
        temp_output_path,
        engine='pyarrow',
        compression='snappy')
    logger.info("Uploading the output to %s", output_path)

    await storage.upload_from_path(temp_output_path, f"{output_path}")


@flow
async def prepare_dataset(input_path: str):
    run_date = datetime.utcnow()

    df = await download_dataset(input_path)
    df = await clean_data(df)

    df_train, df_test = await split_dataset(df)

    await save_dataset(
        df_train,
        f"/reviews/train/{run_date.year}/{run_date.month}/{run_date.day}/reviews.parquet"
    )

    await save_dataset(
        df_test,
        f"/reviews/test/{run_date.year}/{run_date.month}/{run_date.day}/reviews.parquet"
    )


if __name__ == "__main__":
    input_path = "reviews/2023/1/reviews.csv"
    asyncio.run(prepare_dataset(input_path))
