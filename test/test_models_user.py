import pytest
from dotenv import load_dotenv
load_dotenv('.flaskenv')
from test.support.configure_test import app
from app import db
from flask import url_for
from app.models import User
from config import TestingConfig


def test_user_db_create(app):
    """Test User table creation."""
    app = app(TestingConfig)

    test_model_to_insert = User(
        username='testuser',
    )
    db.session.add(test_model_to_insert)
    db.session.commit()

    assert db.session.query(User).one()


def test_user_db_empty(app):
    """Test if User table is empty upon creation."""
    app = app(TestingConfig)

    assert db.session.query(User).count() == 0


def test_user_db_delete(app):
    """Test User record deletion."""
    app = app(TestingConfig)

    test_model_to_insert = User(
        username='testuser',
    )

    db.session.add(test_model_to_insert)
    db.session.commit()

    assert db.session.query(User).one()

    db.session.delete(test_model_to_insert)
    db.session.commit()

    assert db.session.query(User).filter_by(
        username='testuser').first() is None


def test_user_name(app):
    """Test User's username field."""
    app = app(TestingConfig)

    test_model_to_insert = User(
        username='testuser'
    )
    db.session.add(test_model_to_insert)
    db.session.commit()

    assert db.session.query(User).first().username == 'testuser'


def test_user_hash(app):
    """Test User's hash_password() and verify_password() function."""
    app = app(TestingConfig)

    test_model_to_insert = User(
        username='testuser',
    )
    test_model_to_insert.hash_password('password')
    db.session.add(test_model_to_insert)
    db.session.commit()

    assert not db.session.query(User).first().hash_password == 'password'
    assert db.session.query(User).first().verify_password('password')
