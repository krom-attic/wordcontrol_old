from .settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(ROOT_DIR, 'testdata',
                             'sqlite3_test.db'),  # Database with test data
    }
}

ALLOWED_HOSTS = []

STATIC_ROOT = ''

INSTALLED_APPS.append('debug_toolbar')