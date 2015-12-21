import os

# default config
class BaseConfig(object):
	DEBUG = False
	SECRET_KEY = 'E\x134\xa2rw,.L\x0f\x92s\x9b^\x99\x9a\x8a\r\xd2\x96\xb3\xe8_K'
	SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
	# SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/trus_sensor'
	SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
	DEBUG = True


class ProductConfig(BaseConfig):
	DEBUG = False