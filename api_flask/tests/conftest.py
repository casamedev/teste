import pytest 

from api_flask.app import create_app, minimal_app
from api_flask.extensions.db import db

@pytest.fixture(scope="module")
def min_app():
    app = minimal_app(FORCE_ENV_FOR_DYNACONF="testing")
    return app

@pytest.fixture(scope="module")
def app():
    app = create_app(FORCE_ENV_FOR_DYNACONF="testing")
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()





