from prefect import flow, task
from reviewsclassifier.workflows.common import get_secret_value, get_config_value
from dask import dataframe as dd


@task
def download_dataset(path: str) -> dd.DataFrame:
    """Downloads the dataset.

    Returns:
        dd.DataFrame: The dataset.
    """
    storage_options = {
        "key": get_secret_value('datalake-key'),
        "secret": get_secret_value('datalake-secret'),
        "client_kwargs": {"endpoint_url": get_config_value('datalake-endpoint')}
    }

    df = dd.read_csv(f"s3://{path}", storage_options=storage_options)

    return df


@task
def clean_data(df: dd.DataFrame) -> dd.DataFrame:
    """Cleans the data.

    Args:
        df (dd.DataFrame): The data to clean.

    Returns:
        dd.DataFrame: The cleaned data.
    """

    df = df.drop(columns=['ProfileName', 'UserId', 'ProductId','Id','HelpfulnessNumerator','HelpfulnessDenominator','Time','Summary'])

    return df


@flow
def prepare_dataset(input_path: str):
    df = download_dataset(input_path)
    df = clean_data(df)


if __name__ == "__main__":
    input_path = 'raw/reviews/2023/01/27/reviews.csv'
    prepare_dataset(input_path) 