import pytest
import os
from dotenv import load_dotenv
load_dotenv('.flaskenv')
from test.support.configure_test import app
from config import (
    get_env_db_url,
    TestingConfig,
    DevelopmentConfig,
    ProductionConfig,
)


def test_development_config(app):
    """Test DevelopmentConfig configuration."""
    app = app('config.DevelopmentConfig')
    DB_URL = get_env_db_url('development')
    assert app.config['DEBUG']
    assert not app.config['TESTING']
    assert app.config['SQLALCHEMY_DATABASE_URI'] == DB_URL

def test_testing_config(app):
    """Test TestingConfig configuration."""
    app = app('config.TestingConfig')
    DB_URL = get_env_db_url("testing")
    assert app.config["DEBUG"]
    assert app.config["TESTING"]
    assert not app.config["PRESERVE_CONTEXT_ON_EXCEPTION"]
    assert app.config["SQLALCHEMY_DATABASE_URI"] == DB_URL


def test_production_config(app):
    """Test ProductionConfig configuration."""
    app = app('config.ProductionConfig')
    DB_URL = get_env_db_url("production")
    assert not app.config["DEBUG"]
    assert not app.config["TESTING"]
    assert app.config["SQLALCHEMY_DATABASE_URI"] == DB_URL
