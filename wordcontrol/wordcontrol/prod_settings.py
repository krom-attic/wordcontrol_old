from wordcontrol.settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        # 'NAME': os.path.join(PROJECT_DIR, 'sqlite3.db'),  # Or path to database file if using sqlite3.
        'NAME': os.path.join(PROJECT_DIR, 'sqlite3_test.db'),  # Database with test data
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',              # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',              # Set to empty string for default.
    }
}

ALLOWED_HOSTS = ['1.kotimaa.cz8.ru']

STATIC_ROOT = '/home/kotimaa/www/site1/public_html/static/'

# INSTALLED_APPS come from base settings