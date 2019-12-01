import pytest
from dotenv import load_dotenv
load_dotenv('.flaskenv')
from test.support.configure_test import app
from app import db
from flask import url_for
from app.models import Player
from config import TestingConfig


def test_player_db_create(app):
    """Test Player table creation."""
    app = app(TestingConfig)

    test_model_to_insert = Player(
        player_name='Test Name'
    )
    db.session.add(test_model_to_insert)
    db.session.commit()

    assert db.session.query(Player).one()


def test_player_db_empty(app):
    """Test if Player table is empty upon creation."""
    app = app(TestingConfig)

    assert db.session.query(Player).count() == 0


def test_player_db_delete(app):
    """Test Player record deletion."""
    app = app(TestingConfig)

    test_model_to_insert = Player(
        player_name='Test Name'
    )

    db.session.add(test_model_to_insert)
    db.session.commit()

    assert db.session.query(Player).one()

    db.session.delete(test_model_to_insert)
    db.session.commit()

    assert db.session.query(Player).filter_by(
        player_name='Test Name').first() is None


def test_valid_player_field(app):
    """Verify Player fields saved properly."""
    app = app(TestingConfig)

    test_model_to_insert = Player(
        player_name='Test Name',
        player_image='testname.jpg',
        position='PG',
        first_nba_season=2019,
        field_goal_made=100.3,
        field_goal_attempted = 100.3,
        field_goal_pct = 33.3,
        three_pt_made = 100.3,
        three_pt_attempted = 100.3,
        three_pt_pct = 33.3,
        free_throw_made = 100.3,
        free_throw_attempted = 100.3,
        free_throw_pct = 33.3,
        true_stg_pct = 33.3,
        points = 33.3,
        off_reb = 33.3,
        def_reb = 33.3,
        tot_reb = 33.3,
        assists = 33.3,
        steals = 33.3,
        blocks = 33.3,
        turnovers = 33.3,
    )

    db.session.add(test_model_to_insert)
    db.session.commit()

    assert db.session.query(Player).filter_by(player_name='Test Name').one()
    assert db.session.query(Player).first().player_name == 'Test Name'
    assert db.session.query(Player).first().player_image == 'testname.jpg'
    assert db.session.query(Player).first().position == 'PG'
    assert db.session.query(Player).first().first_nba_season == 2019
    assert db.session.query(Player).first().field_goal_made == 100.3
    assert db.session.query(Player).first().field_goal_attempted == 100.3
    assert db.session.query(Player).first().field_goal_pct == 33.3
    assert db.session.query(Player).first().three_pt_made == 100.3
    assert db.session.query(Player).first().three_pt_attempted == 100.3
    assert db.session.query(Player).first().three_pt_pct == 33.3
    assert db.session.query(Player).first().free_throw_made == 100.3
    assert db.session.query(Player).first().free_throw_attempted == 100.3
    assert db.session.query(Player).first().free_throw_pct == 33.3
    assert db.session.query(Player).first().true_stg_pct == 33.3
    assert db.session.query(Player).first().points == 33.3
    assert db.session.query(Player).first().off_reb == 33.3
    assert db.session.query(Player).first().def_reb == 33.3
    assert db.session.query(Player).first().tot_reb == 33.3
    assert db.session.query(Player).first().assists == 33.3
    assert db.session.query(Player).first().steals == 33.3
    assert db.session.query(Player).first().blocks == 33.3
    assert db.session.query(Player).first().turnovers == 33.3


def test_to_dict_function(app):
    """Test Player's to_dict() function."""
    app = app(TestingConfig)

    test_model_to_insert = Player(
        player_name="Test Name",
        player_image="testname.jpg",
        position="PG",
        first_nba_season=2019,
        field_goal_made=100.3,
        field_goal_attempted = 100.3,
        field_goal_pct = 33.3,
        three_pt_made = 100.3,
        three_pt_attempted = 100.3,
        three_pt_pct = 33.3,
        free_throw_made = 100.3,
        free_throw_attempted = 100.3,
        free_throw_pct = 33.3,
        true_stg_pct = 33.3,
        points = 33.3,
        off_reb = 33.3,
        def_reb = 33.3,
        tot_reb = 33.3,
        assists = 33.3,
        steals = 33.3,
        blocks = 33.3,
        turnovers = 33.3,
    )

    db.session.add(test_model_to_insert)
    db.session.commit()
    data = test_model_to_insert.to_dict()
    print(data)

    assert data['id'] == 1
    assert data['player_name'] == 'Test Name'
    assert data['player_image'] == 'testname.jpg'
    assert data['positions'] == 'PG'
    assert data['first_nba_season'] == 2019
    assert data['shooting']['field_goal_made'] == 100.3
    assert data['shooting']['field_goal_attempted'] == 100.3
    assert data['shooting']['field_goal_pct'] == 33.3
    assert data['shooting']['three_pt_made'] == 100.3
    assert data['shooting']['three_pt_attempted'] == 100.3
    assert data['shooting']['three_pt_pct'] == 33.3
    assert data['shooting']['free_throw_made'] == 100.3
    assert data['shooting']['free_throw_attempted'] == 100.3
    assert data['shooting']['free_throw_pct'] == 33.3
    assert data['shooting']['true_stg_pct'] == 33.3
    assert data['shooting']['points'] == 33.3
    assert data['off_reb'] == 33.3
    assert data['def_reb'] == 33.3
    assert data['tot_reb'] == 33.3
    assert data['assists'] == 33.3
    assert data['steals'] == 33.3
    assert data['blocks'] == 33.3
    assert data['turnovers'] == 33.3
    assert data['_links']['self'] == url_for(
        'api.get_player_id', id=data['id'])


def test_player_db_repr(app):
    """Test Player object representation."""
    app = app(TestingConfig)

    test_model_to_insert = Player(
        player_name='Test Name'
    )

    db.session.add(test_model_to_insert)
    db.session.commit()

    assert str(db.session.query(Player).first()) == '<Player: Test Name>'
