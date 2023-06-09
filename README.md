<!-- Python 3.9 badge -->
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)

# DartML
Welcome to **DartML**! This app lets you build Machine Learning models **without writing a single line of code**!


# How to install and run the app

## Install requirements

### Using pip
```bash
pip install -r requirements.txt
```

### Using conda
You can change `new_env_name` to any name you like.

```bash
conda create --name new_env_name python=3.9
pip install -r requirements.txt
```

## Run the app
```bash
streamlit run 0_🏠_Home.py
```

## Change the app mode (single-user to multi-user)
You can change the app mode by toggling the `SINGLE_USER_ADVANCED_APP_VERSION` variable in src/config.py file.

## Testing

### Load tests
- These tests check how app behaves under heavy load.
- Used package: [locust](https://locust.io/).

#### Run simple load tests
Perform simple load test by just visiting pages without interacting with any buttons or uploading any files.

```bash
locust -f tests/load_tests/simple_load_tests.py
```

Remember to put Host information without backlash at the end, for example:
- `http://localhost:8501`  <- this is correct
- `http://localhost:8501/` <- this is incorrect


You can start the locust and simultaneously use the app yourself (or run functional tests), so you can see how the response time changes and ensure that there are no failures.


### Functional tests
- These tests check whether app visually looks and behaves as expected.
- Used package: [seleniumbase](https://seleniumbase.io/).

#### Run functional tests
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

## Project structure

### in English
```
.
├── 0_🏠_Home.py                    # Home page streamlit view.
├── pages                           # Streamlit views for other pages of the app.
│   ├── 1_🧪_Sample.py              # Sample page streamlit view.
│   ├── 2_🔍_Explore.py             # Explore page streamlit view.
│   ├── 4_🛠️_Modify_&_Model.py      # Modify & Model page streamlit view.
│   └── 5_📊_Assess.py              # Assess page streamlit view.
├── src                             # Source code of the app.
│   ├── config.py                   # Configurations for the app.
│   ├── sample                      # Code used specifically in the Sample page.
│   ├── explore                     # Code used specifically in the Explore page.
│   ├── modify_and_model            # Code used specifically in the Modify & Model page.
│   ├── assess                      # Code used specifically in the Assess page.
│   ├── general_views               # Smaller streamlit views used in multiple pages.
│   └── session_state               # Functions related to handling app's session state.
├── tests                           # Tests for the app.
│   ├── functional_tests            # Functional tests.
│   └── load_tests                  # Load tests.
│   └── unit_tests                  # Unit tests.
├── docs                            # Documentation for the app.
├── example_data                    # Example data used in the app.
├── README.md                       # project description you are reading right now
├── requirements.txt                # dependencies for pip
└── .streamlit                      # configurations for streamlit (theme)
    └── config.toml                 # configurations for streamlit (theme)
```

<!-- ### in Polish
```
.
├── 0_🏠_Home.py                    # Widok definiujący wygląd strony Home.
├── pages                           # Widoki definiujące wygląd poszczególnych stron aplikacji.
│   ├── 1_🧪_Sample.py              # Widok definiujący wygląd strony Sample.
│   ├── 2_🔍_Explore.py             # Widok definiujący wygląd strony Explore.
│   ├── 4_🛠️_Modify_&_Model.py      # Widok definiujący wygląd strony Modify & Model.
│   └── 5_📊_Assess.py              # Widok definiujący wygląd strony Assess.
├── src                             # Kod źródłowy aplikacji.
│   ├── config.py                   # Pllik konfiguracyjny aplikacji.
│   ├── sample                      # Kod używany tylko na stronie Sample.
│   ├── explore                     # Kod używany tylko na stronie Explore.
│   ├── modify_and_model            # Kod używany tylko na stronie Modify & Model.
│   ├── assess                      # Kod używany tylko na stronie Assess.
│   ├── general_views               # Mniejsze używane na wielu stronach.
│   └── session_state               # Funkcje związane z obsługą danych zapisywanych w sesji.
├── tests                           # Testy aplikacji.
│   ├── functional_tests            # Testy funkcjonalne.
│   └── load_tests                  # Testy obciążeniowe.
│   └── unit_tests                  # Testy jednostkowe.
├── docs                            # Dokumentacja wygenerowana z komentarzy w kodzie.
├── example_data                    # Przykładowe dane używane w aplikacji.
├── README.md                       # Opis projektu, który właśnie czytasz.
├── requirements.txt                # Zależności dla pip.
└── .streamlit                      # Konfiguracja streamlit (motyw).
    └── config.toml                 # Konfiguracja streamlit (motyw).
``` -->

## Generate documentation from docstrings

### using doxygen
```bash
doxygen
```

### using pdoc
```bash
pdoc src
```

## Manually run autoformat and code quality check
```bash
pre-commit run --all-files
```
