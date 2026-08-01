import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__), "..."))

import pytest
from backend.app import create_app, db as _db


@pytest.fixture
def app():
    app = create_app("testing")
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db(app):
    return db