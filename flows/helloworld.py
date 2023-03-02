from prefect import flow, task, get_run_logger


@task
def greet():
    logger = get_run_logger()
    logger.info("Hello, world!")


@flow
def main():
    greet()


if __name__ == '__main__':
    main()
