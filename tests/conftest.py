import pytest

import pandora


@pytest.fixture
def app():
    app = pandora.create_app()
    yield app

@pytest.fixture
def client(app):
    return app.test_client()
