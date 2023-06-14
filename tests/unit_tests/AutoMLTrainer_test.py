import json
import os

from src import config as src_config
from tests.unit_tests.utils import (
    example_automl_trainer_parameters,
    example_AutoMLTRainer,
)


# temporary directory tests
def test_AutoMLTrainer_destructor():
    """
    Test if destructor deletes temporary directory
    """
    # create AutoMLTrainer object
    auto_ml_trainer = example_AutoMLTRainer()

    # save temporary directory path
    tempdir_path = auto_ml_trainer.tempdir.name

    # check if temporary directory exists
    assert os.path.exists(tempdir_path)

    # delete AutoMLTrainer object
    del auto_ml_trainer

    # check if temporary directory was deleted
    assert not os.path.exists(tempdir_path)


def test_AutoMLTrainer_destructor_when_temporary_directory_in_use():
    """
    Test if destructor deletes temporary directory when it is in use
    """
    # create AutoMLTrainer object
    auto_ml_trainer = example_AutoMLTRainer()

    # save temporary directory path
    tempdir_path = auto_ml_trainer.tempdir.name

    # check if temporary directory exists
    assert os.path.exists(tempdir_path)

    # create a file inside temporary directory and keep it open
    with open(f"{tempdir_path}/test_file.txt", "w") as f:
        f.write("test")

        # delete AutoMLTrainer object
        del auto_ml_trainer

    # check if temporary directory was deleted
    assert not os.path.exists(tempdir_path)


def test_AutoMLTrainer_destructor_when_temporary_directory_does_not_exist():
    """
    Test if destructor does not raise an error when temporary directory does not exist
    """
    # create AutoMLTrainer object
    auto_ml_trainer = example_AutoMLTRainer()

    # save temporary directory path
    tempdir_path = auto_ml_trainer.tempdir.name

    # check if temporary directory exists
    assert os.path.exists(tempdir_path)

    # delete temporary directory
    auto_ml_trainer.tempdir.cleanup()

    # delete AutoMLTrainer object
    del auto_ml_trainer

    # check if temporary directory was deleted
    assert not os.path.exists(tempdir_path)


def test_AutoMLTrainer_destructor_when_temporary_directory_is_not_empty():
    """
    Test if destructor deletes temporary directory when it is not empty
    """
    # create AutoMLTrainer object
    auto_ml_trainer = example_AutoMLTRainer()

    # save temporary directory path
    tempdir_path = auto_ml_trainer.tempdir.name

    # check if temporary directory exists
    assert os.path.exists(tempdir_path)

    # create a file inside temporary directory
    with open(f"{tempdir_path}/test_file.txt", "w") as f:
        f.write("test")

    # delete AutoMLTrainer object
    del auto_ml_trainer

    # check if temporary directory was deleted
    assert not os.path.exists(tempdir_path)


# parameters test
def test_AutoMLTrainer_save_parameters_to_json_file():
    """
    Test if _save_parameters_to_json_file method correctly saves parameters to a json file.
    """
    test_parameters = example_automl_trainer_parameters()

    # create AutoMLTrainer object
    auto_ml_trainer = example_AutoMLTRainer(
        type="simple",
        problem_type=test_parameters["problem_type"],
        metric=test_parameters["metric"],
        algorithms=test_parameters["algorithms"],
        total_time_limit=test_parameters["total_time_limit"],
        mode=test_parameters["mode"],
        shuffle=test_parameters["shuffle"],
        stratify=test_parameters["stratify"],
        split_type=test_parameters["split_type"],
        train_ratio=test_parameters["train_ratio"],
    )

    # save parameters to json file
    auto_ml_trainer._save_parameters_to_json_file()

    json_file_name = (
        f"{auto_ml_trainer.tempdir.name}/{src_config.TRAINING_PARAMETERS_FILENAME}"
    )

    # check if json file exists
    assert os.path.exists(json_file_name)

    # check if json file contains correct parameters
    with open(
        json_file_name,
        "r",
    ) as f:
        assert test_parameters == json.load(f)

    # delete AutoMLTrainer object
    del auto_ml_trainer
