import json
import os
import subprocess
import sys
import tempfile
from typing import Literal

import pandas as pd

from src import config


class AutoMLTrainer:
    """
    Trains models using AutoML.
    Training is performed in a subprocess.
    Results are saved in a temporary folder. The temporary folder is created in constructor and deleted in destructor.
    """

    def __init__(
        self,
        df: pd.DataFrame,
        target_col_name: str,
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
    ):
        # save parameters
        self.target_col_name = target_col_name
        self.problem_type = problem_type
        self.eval_metric = eval_metric
        self.algorithms = algorithms
        self.total_time_limit = total_time_limit
        self.mode = mode
        self.shuffle = shuffle
        self.stratify = stratify
        self.split_type = split_type
        self.train_ratio = train_ratio

        # create temporary directory
        self.tempdir = tempfile.TemporaryDirectory(
            dir=config.TEMP_DIRS_DIRECTORY_NAME,
            # ignore_cleanup_errors=True    # only python 3.10+
        )

        # save dataframe to csv inside temporary directory
        df.to_csv(os.path.join(self.tempdir.name, config.DATA_FILENAME))

    def _save_parameters_to_json_file(self) -> None:
        """
        Saves parameters to a json file inside temporary directory.
        """
        parameters = {
            "target_col_name": self.target_col_name,
            "problem_type": self.problem_type,
            "eval_metric": self.eval_metric,
            "algorithms": self.algorithms,
            "total_time_limit": self.total_time_limit,
            "mode": self.mode,
            "shuffle": self.shuffle,
            "stratify": self.stratify,
            "split_type": self.split_type,
            "train_ratio": self.train_ratio,
        }
        with open(
            os.path.join(self.tempdir.name, config.TRAINING_PARAMETERS_FILENAME), "w"
        ) as f:
            json.dump(parameters, f)

    def train(self) -> None:
        """
        Trains models using AutoML in a subprocess.
        """
        # save parameters to json file inside temporary directory
        self._save_parameters_to_json_file()

        # create an empty directory for generated report
        os.mkdir(os.path.join(self.tempdir.name, config.REPORT_DIRECTORY_NAME))

        # run automl_training_script.py in a subprocess
        with open(os.path.join(self.tempdir.name, config.LOGS_FILENAME), "w") as f:
            subprocess.run(
                [sys.executable, "automl_training_script.py", self.tempdir.name],
                stdout=f,
                stderr=f,
                shell=(
                    sys.platform == "win32"
                ),  # Adding this line for Windows compatibility
            )

    def __repr__(self) -> str:
        return f"AutoMLTrainer(tempdir={self.tempdir.name}, target_col_name={self.target_col_name}, problem_type={self.problem_type}, eval_metric={self.eval_metric}, algorithms={self.algorithms}, total_time_limit={self.total_time_limit}, mode={self.mode}, shuffle={self.shuffle}, stratify={self.stratify})"

    def __del__(self):
        # delete temporary directory
        try:
            self.tempdir.cleanup()
        except PermissionError:
            print(
                f"Could not delete temporary directory {self.tempdir.name}. Please delete it manually."
            )
