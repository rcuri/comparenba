import os
import click
from app import db
from app.populate_players import populate_database
from app.player_images import populate_images


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

    @populate.command()
    def images():
        try:
            populate_images(db)
        except:
            print("An error occurred with the images.")
            db.session.rollback()
