from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache
from flask_cors import CORS
from elasticsearch import Elasticsearch
import os


db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
cache = Cache()


def create_app(config_class='config.ProductionConfig'):
    """
    Flask app factory using ProductionConfig (config_class) configuration.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    cache.init_app(app, config=app.config['CACHE'])

    # Register blueprints
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')


    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
            if app.config['ELASTICSEARCH_URL'] else None

    return app


from app import models
