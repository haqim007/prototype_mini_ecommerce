import os


class Config(object):
    """
    Parent configuration class
    The Config class contains the general settings that we want all environments to have by default.
    Other environment classes inherit from it and can be used to set settings that are only unique to them.
    Additionally, the dictionary app_config is used to export the 4 environments we've specified.
    It's convenient to have it so that we can import the config under its name tag in future.
    """

    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class DevelopmentConfig(Config):
    """ Configuration for development """
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TESTING_URL')
    DEBUG = True
    FLASK_ENV = "testing"


class StagingConfig(Config):
    """ Configuration for staging """
    DEBUG = True


class ProductionConfig(Config):
    """ Configuration for production """
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig
}
