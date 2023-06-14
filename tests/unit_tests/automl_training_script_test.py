import os
import tempfile

from pandas.testing import assert_frame_equal

from automl_training_script import perform_X_y_split, train_automl
from src import config
from tests.unit_tests.utils import example_automl_trainer_parameters, example_dataframe


def test_perform_X_y_split():
    """
    Test if perform_X_y_split function correctly splits DataFrame into X and y.
    """
    example_df = example_dataframe(type="simple")
    example_target_col_name = example_df.columns[-1]
    X_expected = example_df.drop(columns=example_target_col_name)
    y_expected = example_df[example_target_col_name]
    X_actual, y_actual = perform_X_y_split(example_df, example_target_col_name)
    assert_frame_equal(X_expected, X_actual)
    assert y_expected.equals(y_actual)


def test_train_automl():
    """
    Test if train_automl function generates report after automl training.
    """
    df = example_dataframe(type="simple")
    target_col_name = df.columns[-1]
    parameters = example_automl_trainer_parameters()

    # trian_automl in temporary directory
    with tempfile.TemporaryDirectory(dir=config.TEMP_DIRS_DIRECTORY_NAME) as tmpdirname:
        train_automl(
            df=df,
            target_col_name=target_col_name,
            tmpdirname=tmpdirname,
            problem_type=parameters["problem_type"],
            eval_metric=parameters["eval_metric"],
            algorithms=parameters["algorithms"],
            total_time_limit=3,
            mode=parameters["mode"],
            shuffle=parameters["shuffle"],
            stratify=parameters["stratify"],
            split_type=parameters["split_type"],
            train_ratio=parameters["train_ratio"],
        )

        # check if main report file has been created
        assert os.path.isfile(
            os.path.join(
                tmpdirname,
                "leaderboard.csv",
            )
        )

    # make sure that temporary directory has been deleted
    assert not os.path.exists(tmpdirname)
