from wordcontrol.settings.base_settings import *

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = False

ALLOWED_HOSTS = ['1.kotimaa.cz8.ru', 'kotimaa.ru']

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

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = os.environ['TIME_ZONE']

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = '/home/kotimaa/www/site1/public_html/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# TODO Enable with HTTPS:
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True

# TODO See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/ for production optimisations