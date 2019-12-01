import os

basedir = os.path.abspath(os.path.dirname(__file__))


def get_env_variable(name):
    """
    Return value for environment variable (name) if defined. If not defined,
    return KeyError.
    """
    try:
        return os.environ.get(name)
    except KeyError:
        message = f"Expected environment variable '{name}' not set"
        raise Exception(message)


def create_db_url(user, pw, url, db):
    """
    Create URL to connect to PostgreSQL, with psycopg2 as the driver.
    'user' and 'pw' are the user's database credentials.
    'url' is the name of the host and the port number. e.g. 127.0.0.1:5432
    'db' is the name of the database.
    """
    return f"postgresql+psycopg2://{user}:{pw}@{url}/{db}"


def get_env_db_url(env_setting):
    """
    Set database configuration variables depending on which environment
    you're working in. Environment variables are defined in .flaskenv file.

    Create URL to connect app to specific database using create_db_url() and
    return the resulting URL string.
    """
    if env_setting == "development":
        POSTGRES_USER = get_env_variable("DEV_POSTGRES_USER")
        POSTGRES_PW = get_env_variable("DEV_POSTGRES_PW")
        POSTGRES_URL = get_env_variable("DEV_POSTGRES_URL")
        POSTGRES_DB = get_env_variable("DEV_POSTGRES_DB")
    elif env_setting == "testing":
        POSTGRES_USER = get_env_variable("TESTING_POSTGRES_USER")
        POSTGRES_PW = get_env_variable("TESTING_POSTGRES_PW")
        POSTGRES_URL = get_env_variable("TESTING_POSTGRES_URL")
        POSTGRES_DB = get_env_variable("TESTING_POSTGRES_DB")
    elif env_setting == "production":
        POSTGRES_USER = get_env_variable("PROD_POSTGRES_USER")
        POSTGRES_PW = get_env_variable("PROD_POSTGRES_PW")
        POSTGRES_URL = get_env_variable("PROD_POSTGRES_URL")
        POSTGRES_DB = get_env_variable("PROD_POSTGRES_DB")


    return create_db_url(
        POSTGRES_USER, POSTGRES_PW, POSTGRES_URL, POSTGRES_DB)


# Get db URLs for each environment
DEV_DB_URL = get_env_db_url("development")
TESTING_DB_URL = get_env_db_url("testing")
PROD_DB_URL = get_env_db_url("production")


class Config(object):
    """
    Base Configuration class with default settings. Subclasses will
    override environment variables depending on current environment.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = DEV_DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL') or None
    POSTS_PER_PAGE = 25
    CACHE = {
        'CACHE_TYPE': 'redis',
        'CACHE_REDIS_HOST': os.environ.get('CACHE_REDIS_HOST') or 'localhost',
        'CACHE_REDIS_PORT': os.environ.get('CACHE_REDIS_PORT') or '6379',
        'CACHE_REDIS_URL': os.environ.get('CACHE_REDIS_URL') or \
        'redis://localhost:6379'
    }
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True


class TestingConfig(Config):
    """Test environment configuration."""
    SQLALCHEMY_DATABASE_URI = TESTING_DB_URL
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    """Production environment configuration."""
    SQLALCHEMY_DATABASE_URI = PROD_DB_URL
    DEBUG = False
    TESTING = False


class CacheConfig(object):
    CACHE_TYPE = 'redis'
    CACHE_KEY_PREFIX = 'fcache'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = '6379'
    CACHE_REDIS_URL = 'redis://localhost:6379'
