# thesis
Engineering thesis app in streamlit


# Installation

## Using conda
You can change `new_env_name` to any name you like.

```bash
conda create --name new_env_name python=3.9
pip install -r requirements.txt
```

# Testing

## Load tests
- These tests check how app behaves under heavy load.
- Used package: [locust](https://locust.io/).

### Run simple load tests
Perform simple load test by just visiting pages without interacting with any buttons or uploading any files.

```bash
locust -f tests/load_tests/simple_load_tests.py
```

Remember to put Host information without backlash at the end, for example:
- `http://localhost:8501`  <- this is correct
- `http://localhost:8501/` <- this is incorrect


You can start the locust and simultaneously use the app yourself (or run functional tests), so you can see how the response time changes and ensure that there are no failures.


## Functional tests
- These tests check whether app visually looks and behaves as expected.
- Used package: [seleniumbase](https://seleniumbase.io/).

### Run functional tests
First you need to specify the `HOST_URL` in `tests/functional_tests/config.py` file. By default it's set to `http://localhost:8501`.

Run all tests:
```bash
pytest tests/functional_tests/functional_tests.py --chrome --headless
```

Run single test (`test_explore_page` in this example):
```bash
pytest tests/functional_tests/functional_tests.py --chrome --headless -k test_explore_page
```

- You can specify the number of concurrent users by adding `-n=<number_of_users>` flag.
- You can remove the `--headless` flag if you want to make the testing browser visible.
- You can change `--edge` to any browser you like, for example `--chrome` or `--firefox`.
- You can make it slower by adding `--slow` flag.
- You can highlight assertions by adding `--demo` flag.
- You can add `-k <test_name>` flag to run only specific test.
