import os

environ = os.environ


class Environment(object):
    LOCAL = 'local'
    DEV = 'dev'
    PRD = 'prd'


class Config(object):
    # - config related to redis
    REDIS_ENDPOINT = environ.get('REDIS_ENDPOINT', '127.0.0.1')
    REDIS_PORT = environ.get('REDIS_PORT', '6379')
    DISPATCHER_URL = environ.get('DISPATCHER_URL', '127.0.0.1')


class LocalConfig(Config):
    DEBUG = True
    AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')


class DevConfig(Config):
    DEBUG = False


class PrdConfig(Config):
    DEBUG = False

config = {
    Environment.LOCAL: LocalConfig,
    Environment.DEV: DevConfig,
    Environment.PRD: PrdConfig
}
