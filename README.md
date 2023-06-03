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

## Run load tests

### Run simple load tests
Perform simple load test by just visiting pages without interacting with any buttons or uploading any files.

```bash
locust -f tests/load_tests/simple_load_tests.py
```

Remember to put Host information without backlash at the end, for example:
- `http://localhost:8501`  <- this is correct
- `http://localhost:8501/` <- this is incorrect


You can start the locust and simultaneously use the app yourself (or run functional tests), so you can see how the response time changes and ensure that there are no failures.