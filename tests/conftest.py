import pytest


BASE_URL = "http://localhost:8000"
FLIGHT_ID = "AAA01"
PASSPORT_ID_CORRECT = "BC1500"
FIRST_NAME_CORRECT = "Shauna"
LAST_NAME_ID_CORRECT = "Davila"

@pytest.fixture(scope="session")
def api():
    return BASE_URL

@pytest.fixture(scope="session")
def flight_id():
    return FLIGHT_ID

@pytest.fixture(scope="session")
def passport_id_correct():
    return PASSPORT_ID_CORRECT

@pytest.fixture(scope="session")
def first_name_correct():
    return FIRST_NAME_CORRECT

@pytest.fixture(scope="session")
def last_name_correct():
    return LAST_NAME_ID_CORRECT