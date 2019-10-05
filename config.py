import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'SECRET_KEY'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ELASTICSEARCH_URL = 'https://1pth9505od:59sv268usq@ivy-346702352.us-east-1.bonsaisearch.net:443'
    #os.environ.get('ELASTICSEARCH_URL') or None
    POSTS_PER_PAGE = 25
