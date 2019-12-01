import os
import click
from app import db
from app.populate_players import populate_database

def register(app):
    """Register shell script commands."""
    @app.cli.group()
    def populate():
        """Populate database commands."""
        pass

    @populate.command()
    def initiate():
        """Populate database with db variable from app."""
        try:
            populate_database(db)
        except Exception as e:
            print("An error occurred.")
            print(e)
            db.session.rollback()
