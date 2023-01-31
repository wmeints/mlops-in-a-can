import asyncio

from prefect.deployments import Deployment
from prefect_aws.s3 import MinIOCredentials, S3Bucket

from flows.prepare_dataset import prepare_dataset


async def deploy_flow(fn: callable, name: str, default_params: dict = {}):
    flows_storage = await S3Bucket.load("flows")

    print(flows_storage.dict())

    deployment = await Deployment.build_from_flow(
        fn,
        name,
        storage=flows_storage,
    )

    await deployment.apply()

    return deployment


async def main():
    await deploy_flow(prepare_dataset, "prepare-dataset")


if __name__ == "__main__":
    asyncio.run(main())
