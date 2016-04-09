from wordcontrol.settings.prod_settings import *

# Make this unique, and don't share it with anybody.
SECRET_KEY = '=&izv7jn!ylg9p$w1_*62+*s_j@1u19g*_4=4^*cq8eqe*q7on'

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# INSTALLED_APPS are listed in the base settings

# TODO Get PASSWORD from somewhere
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        # 'NAME': os.path.join(BASE_DIR, 'sqlite3.db'),  # Or path to database file if using sqlite3.
        'NAME': os.path.join(BASE_DIR, '_testdata', 'sqlite3_test.db'),  # Database with test data
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',              # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',              # Set to empty string for default.
    }
}

# TODO Add STATIC_ROOT for test environment
# STATIC_ROOT = '/home/kotimaa/www/site1/public_html/static/'

# TODO Add MEDIA_ROOT for test environment
MEDIA_ROOT = ''

# TODO Enable with HTTPS:
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True

# TODO Configure email backend for test environment
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# EMAIL_FILE_PATH = '/tmp/app-messages'
