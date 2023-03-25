
"""Flask config."""
from os import environ, path
from dotenv import load_dotenv

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, '.env'))


class Config:
    """Flask configuration variables."""

    FLASK_APP = environ.get('FLASK_APP')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
