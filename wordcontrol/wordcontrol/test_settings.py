from wordcontrol.settings import *

DEBUG = False
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