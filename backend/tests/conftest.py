import pytest

from app import create_app
from app.extensions.database import db as database


@pytest.fixture()
def app():
    app = create_app("testing")
    with app.app_context():
        database.create_all()
        yield app
        database.session.remove()
        database.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def auth_header(client):
    client.post("/signup", json={
        "username": "expense_owner",
        "password": "secure-password",
        "password_confirmation": "secure-password",
    })
    response = client.post("/login", json={
        "username": "expense_owner",
        "password": "secure-password",
    })
    return {"Authorization": f"Bearer {response.get_json()['token']}"}
