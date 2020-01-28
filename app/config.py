import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	DEBUG = False
	TESTING = False
	CSRF_ENABLED = True
	SECRET_KEY = 'sausage'
	

class Production_config(Config):
	DEBUG = False

class Staging_config(Config):
	DEVELOPMENT = True
	DEBUG = True

class Development_config(Config):
	DEVELOPMENT = True
	DEBUG = True

class Testing_config(Config):
	TESTING = True
