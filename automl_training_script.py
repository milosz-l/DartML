import json
import sys
from typing import Literal

import pandas as pd
from supervised.automl import AutoML

from src import config


def perform_X_y_split(df: pd.DataFrame, target_label: str):
    """
    Performs X y split on given dataframe.
    args:
        df: dataframe to split
        target_label: name of the target column
    """
    X = df.drop(columns=target_label)
    y = df[target_label]
    return X, y


def train_automl(
    df: pd.DataFrame,
    target_col_name: str,
    tmpdirname: str,
    problem_type: Literal[
        "binary classification", "multiclass classification", "regression", "auto"
    ],
    eval_metric: str,
    algorithms: list[str],
    total_time_limit: int,
    mode: Literal["Explain", "Perform", "Compete"],
    shuffle: bool,
    stratify: bool,
    split_type: Literal["split", "kfold"],
    train_ratio: float,
) -> None:
    """
    Trains AutoML model.
    args:
        target_col_name: name of the target column
        tmpdirname: path to the temporary directory, where all the results are saved
        problem_type: problem type
        eval_metric: evaluation metric
        algorithms: list of algorithms to train
        total_time_limit: total time limit for training in seconds
        mode: mode of training
        shuffle: whether to shuffle the data
        stratify: whether to stratify the data
    """
    X, y = perform_X_y_split(df, target_col_name)

    if split_type == "split":
        configured_validation_strategy = {
            "validation_type": "split",
            "train_ratio": train_ratio,
            "shuffle": shuffle,
            "stratify": stratify,
            "random_seed": config.RANDOM_STATE,
        }
    else:  # validation type is kfold
        configured_validation_strategy = {
            "validation_type": "kfold",
            "k_folds": 5,
            "shuffle": shuffle,
            "stratify": stratify,
            "random_seed": config.RANDOM_STATE,
        }

    # create AutoML object
    if problem_type == "auto":
        automl = AutoML(
            results_path=tmpdirname,
            mode=mode,
            ml_task=problem_type,
            algorithms=algorithms,
            validation_strategy=configured_validation_strategy,
            total_time_limit=total_time_limit,
        )
    else:
        problem_type = problem_type.replace(" ", "_")
        automl = AutoML(
            results_path=tmpdirname,
            mode=mode,
            ml_task=problem_type,
            algorithms=algorithms,
            validation_strategy=configured_validation_strategy,
            total_time_limit=total_time_limit,
            eval_metric=eval_metric,
        )

    automl.fit(X, y)


def main():
    # get tempdir name from argument
    tempdirname = sys.argv[1]

    # get parameters from json file
    with open(f"{tempdirname}/{config.TRAINING_PARAMETERS_FILENAME}") as f:
        training_parameters = json.load(f)

    # access the parameters
    target_col_name = training_parameters["target_col_name"]
    problem_type = training_parameters["problem_type"]
    metric = training_parameters["metric"]
    algorithms = training_parameters["algorithms"]
    total_time_limit = training_parameters["total_time_limit"]
    mode = training_parameters["mode"]
    shuffle = training_parameters["shuffle"]
    stratify = training_parameters["stratify"]
    split_type = training_parameters["split_type"]
    train_ratio = training_parameters["train_ratio"]

    # get data from csv file
    df = pd.read_csv(f"{tempdirname}/{config.DATA_FILENAME}")

    # train automl
    train_automl(
        df=df,
        target_col_name=target_col_name,
        tmpdirname=f"{tempdirname}/{config.REPORT_DIRECTORY_NAME}",
        problem_type=problem_type,
        eval_metric=metric,
        algorithms=algorithms,
        total_time_limit=total_time_limit,
        mode=mode,
        shuffle=shuffle,
        stratify=stratify,
        split_type=split_type,
        train_ratio=train_ratio,
    )


if __name__ == "__main__":
    main()
