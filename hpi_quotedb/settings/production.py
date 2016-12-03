from .development import *
import os

QUOTEDB_DEBUG_USERNAME = False

ALLOWED_HOSTS = ["quotedb"]

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': os.environ['QUOTEDB_DB_NAME'],
		'HOST': os.environ['QUOTEDB_DB_HOST'],
		'PASSWORD': os.environ['QUOTEDB_DB_PASSWORD'],
		'USER': os.environ['QUOTEDB_DB_USER'],
	}
}

SERVER_BASE_PATH = os.environ['QUOTEDB_SERVER_BASE_PATH']
STATIC_URL = '/' + SERVER_BASE_PATH + 'static/'
