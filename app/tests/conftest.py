import pytest
from fastapi.testclient import TestClient

@pytest.fixture(scope="module")
def client_mock():
    return None
