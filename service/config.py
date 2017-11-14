import logging
import os


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'b6b85744de85640f47976b784aa335e9af9a542b7d381e88'
    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOGGING_LOCATION = 'setlistfm_service.log'
    LOGGING_LEVEL = logging.DEBUG
    BOOTSTRAP_SERVE_LOCAL = False
    SETLIST_PORT = 6001
    SETLIST_HOST = '0.0.0.0'
    SETLIST_FM_API_KEY = 'EMPTY_SETLIST_FM_API_KEY'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False
    SECRET_KEY = '217c76c9032c421e62a18960e4930f753d24ad75bc5b0e07'


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    SECRET_KEY = '3eab94077f627bb9b27afc24e693631d52fe3c44af20f1f5'


config = {
    "development": "service.config.DevelopmentConfig",
    "testing": "service.config.TestingConfig",
    "default": "service.config.DevelopmentConfig"
}


def configure_app(app):
    config_name = os.getenv('FLASK_CONFIGURATION', 'default')
    app.config.from_object(config[config_name])
    app.config.from_pyfile('config.cfg', silent=True)
    print('SERVICE_SETLIST_CONFIG_FILE={0}'.format(os.environ.get('SERVICE_SETLIST_CONFIG_FILE')))
    app.config.from_envvar('SERVICE_SETLIST_CONFIG_FILE', silent=True)
    # Configure logging
    handler = logging.FileHandler(app.config['LOGGING_LOCATION'])
    handler.setLevel(app.config['LOGGING_LEVEL'])
    formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
