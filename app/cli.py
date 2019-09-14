import os
import click
from app.populate_players import populate_database
from app import db


def register(app):
    @app.cli.group()
    def populate():
        """Populate database commands"""
        pass

    @populate.command()
    def initiate():
        try:
            populate_database(db)
        except:
            print("An error occurred.")
            db.session.rollback()
