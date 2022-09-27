from fastapi.testclient import TestClient
from serve import app
from mocks import *

client = TestClient(app)


# TODO Test FastAPI
@bind_test_database
def test_get_lemma():
    response = client.get("/lemma/nama")
    assert response is False
