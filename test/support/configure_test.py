import pytest
from app import create_app, db
from config import get_env_db_url
from config import TestingConfig


@pytest.yield_fixture
def app():
    """app function for pytest testing."""
    def _app(config_class):
        """
        Create app with config_class. If using TestingConfig, start with
        empty database and create tables.
        """
        app = create_app(config_class)
        # Push test context to access app
        app.test_request_context().push()

        if config_class is TestingConfig:
            # Always start with empty db
            db.drop_all()
            from app.models import Player
            db.create_all()

        return app

    yield _app

    # Teardown. Drop database if using TestingConfig.
    db.session.remove()
    if str(db.engine.url) == TestingConfig.SQLALCHEMY_DATABASE_URI:
        db.drop_all()
