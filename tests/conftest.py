from spoonerist import app
import pytest


@pytest.yield_fixture
def client():
    app.config['TESTING'] = True
    app.config['DEBUG'] = False
    with app.test_client() as c:
        yield c
