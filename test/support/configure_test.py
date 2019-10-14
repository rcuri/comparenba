import pytest

from app import create_app, db
from config import get_env_db_url
from config import TestingConfig

@pytest.yield_fixture
def app():
    def _app(config_class):
        app = create_app(config_class)
        app.test_request_context().push()

        if config_class is TestingConfig:
            # always start with empty db
            db.drop_all()
            from app.models import Player
            db.create_all()

        return app

    yield _app
    db.session.remove()
    if str(db.engine.url) == TestingConfig.SQLALCHEMY_DATABASE_URI:
        db.drop_all()
