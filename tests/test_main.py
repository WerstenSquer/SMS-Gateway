from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_sending():
    response = client.post("/sending", params={
             "address": "Google",
             "phone_number": 88005553535,
             "message": "Hello"
    })
    print(response.url)
    assert response.status_code == 200, "Ошибка отправки"

def test_mailing():
    response = client.post("/mailing", params={
        "address": "Google",
        "phone_numbers": [88005553535, 89005553534],
        "message": "Hello"
    })
    print(response.url)
    assert response.status_code == 200, "Ошибка отправки"