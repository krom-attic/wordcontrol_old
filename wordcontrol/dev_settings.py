from wordcontrol.settings import *

# Make this unique, and don't share it with anybody.
SECRET_KEY = '=&izv7jn!ylg9p$w1_*62+*s_j@1u19g*_4=4^*cq8eqe*q7on'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []

INSTALLED_APPS.append('debug_toolbar')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(BASE_DIR, '_testdata',
                             'sqlite3_test.db'),  # Database with test data
    }
}

# Absolute path to the directory static files should be collected to.
# STATIC_ROOT isn't used

# Additional locations of static files
# STATICFILES_DIRS isn't used