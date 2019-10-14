import os

basedir = os.path.abspath(os.path.dirname(__file__))

def get_env_variable(name):
    try:
        return os.environ.get(name)
    except KeyError:
        message = "Expected environment variable '{}' not set".format(name)
        raise Exception(message)


def create_db_url(user, pw, url, db):
    return f"postgresql+psycopg2://{user}:{pw}@{url}/{db}"

def get_env_db_url(env_setting):
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


    return create_db_url(POSTGRES_USER, POSTGRES_PW, POSTGRES_URL, POSTGRES_DB)

# get db urls for each environment
DEV_DB_URL = get_env_db_url("development")
TESTING_DB_URL = get_env_db_url("testing")
PROD_DB_URL = get_env_db_url("production")

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = DEV_DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL') or None
    POSTS_PER_PAGE = 25
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = TESTING_DB_URL
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = PROD_DB_URL
    DEBUG = False
    TESTING = False
