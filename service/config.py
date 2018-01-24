import logging
import os


class BaseConfig(object):
    DEBUG = False
    TESTING = False
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



class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True



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
