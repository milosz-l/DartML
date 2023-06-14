from typing import Literal

import pandas as pd

from src.modify_and_model.AutoMLTrainer import AutoMLTrainer


def example_dataframe(type: Literal["real", "simple"]) -> pd.DataFrame:
    """
    Returns an example dataframe. Used for testing.
    args:
        type: "real" is Hotel_Reservations.csv, "simple" is a simple dataframe
    """
    if type == "real":
        return pd.read_csv("example_data/Hotel_Reservations.csv")
    elif type == "simple":
        return pd.DataFrame(
            {
                "a": [1, 2, 3],
                "b": [4, 5, 6],
                "c": ["a", "b", "c"],
                "d": [7, 8, 9],
                "e": [10, 11, 12],
            }
        )
    else:
        raise ValueError(f"Invalid DataFrame type: {type}")


def example_AutoMLTRainer(
    type: Literal["real", "simple"] = "simple",
    problem_type: Literal[
        "binary classification", "multiclass classification", "regression", "auto"
    ] = "auto",
    metric: str = "",
    algorithms: list[str] = [
        "Baseline",
        "Linear",
        "Decision Tree",
        "Random Forest",
        "Xgboost",
    ],
    total_time_limit: int = 30,
    mode: Literal["Explain", "Perform", "Compete"] = "Compete",
    shuffle: bool = True,
    stratify: bool = False,
    split_type: Literal["split", "kfold"] = "split",
    train_ratio: float = 0.75,
) -> AutoMLTrainer:
    """
    Returns an example AutoMLTrainer object. Used for testing.
    args:
        type: "real" is for Hotel_Reservations.csv, "simple" is for a simple dataframe
    """
    if type == "real":
        df = example_dataframe(type="real")
    elif type == "simple":
        df = example_dataframe(type="simple")
    else:
        raise ValueError(f"Invalid example object type: {type}")
    return AutoMLTrainer(
        df=df,
        target_col_name=df.columns[-1],
        problem_type=problem_type,
        metric=metric,
        algorithms=algorithms,
        total_time_limit=total_time_limit,
        mode=mode,
        shuffle=shuffle,
        stratify=stratify,
        split_type=split_type,
        train_ratio=train_ratio,
    )


def example_automl_trainer_parameters() -> dict:
    """
    Returns example parameters for AutoMLTrainer. Used for testing.
    """
    return {
        "target_col_name": "e",
        "problem_type": "auto",
        "metric": None,
        "algorithms": [
            "Baseline",
            "Linear",
            "Decision Tree",
            "Random Forest",
            "Xgboost",
        ],
        "total_time_limit": 30,
        "mode": "Compete",
        "shuffle": True,
        "stratify": True,
        "split_type": "split",
        "train_ratio": 0.75,
    }
