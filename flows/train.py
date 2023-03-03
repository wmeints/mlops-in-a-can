import asyncio
from os import makedirs

import mlflow
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from prefect import flow, task
from prefect.filesystems import Azure
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score


def get_or_create_experiment() -> str:
    experiment = mlflow.get_experiment_by_name('iris')

    if experiment is None:
        experiment_id = mlflow.create_experiment('iris')
    else:
        experiment_id = experiment.experiment_id

    return experiment_id


@task
async def download_dataset():
    raw_storage = await Azure.load("raw")
    await raw_storage.get_directory("iris/2023/03/02", "data/raw")


@task
async def train_model(num_estimators: int) -> RandomForestClassifier:
    experiment_id = get_or_create_experiment()

    with mlflow.start_run(experiment_id=experiment_id) as run:
        mlflow.log_param('num_estimators', num_estimators)

        df = pd.read_csv('data/raw/iris.csv')
        features = df.drop('species', axis=1)
        target = df['species']

        features_train, features_test, target_train, target_test = train_test_split(features, target, test_size=0.2)
        model = RandomForestClassifier(n_estimators=num_estimators)

        model.fit(features_train, target_train)
        pred_test = model.predict(features_test)

        precision = precision_score(target_test, pred_test, average='micro')
        recall = recall_score(target_test, pred_test, average='micro')
        f1 = f1_score(target_test, pred_test, average='micro')

        matrix = confusion_matrix(target_test, pred_test)
        figure = plt.figure()
        sns.heatmap(matrix, annot=True, annot_kws={"size": 16})

        mlflow.log_metric('precision', precision)
        mlflow.log_metric('recall', recall)
        mlflow.log_metric('f1', f1)
        mlflow.log_figure(figure, 'figures/confusion_matrix.png')

        makedirs('models/classifier', exist_ok=True)

        mlflow.sklearn.save_model(
            model, "models/classifier",
            pip_requirements=["scikit-learn", "pandas"])

        mlflow.log_artifacts('models/classifier', 'model')
        mlflow.register_model(f'runs:/{run.info.run_id}/model', 'iris_classifier')


@flow
async def train(num_estimators: int = 100):
    await download_dataset()
    await train_model(num_estimators)


if __name__ == "__main__":
    asyncio.run(train(100))
