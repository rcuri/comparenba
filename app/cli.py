import os
import click
from app import db
from app.populate_players_again import populate_database

def register(app):
    @app.cli.group()
    def populate():
        """Populate database commands"""
        pass

    @populate.command()
    def initiate():
        try:
            populate_database(db)
        except Exception as e:
            print("An error occurred.")
            print(e)
            db.session.rollback()
