import sys
from os.path import join, abspath, dirname
DEBUG = True
TEMPLATE_DEBUG = DEBUG
PROJECT_ROOT = abspath(dirname(dirname(__file__)))
JCROP_MODULE_PATH = abspath(join(PROJECT_ROOT, '..'))
sys.path.insert(0, JCROP_MODULE_PATH)

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(PROJECT_ROOT, 'dev.db'),
    }
}
TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
MEDIA_ROOT = join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = join(PROJECT_ROOT, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = ()
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
SECRET_KEY = 'hh^b+3k8p#u018vf*dt5eljpo(nq&amp;cuj8ui0n+f#mk(2adyrcd'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)
ROOT_URLCONF = 'example.urls'
WSGI_APPLICATION = 'example.wsgi.application'
TEMPLATE_DIRS = (
    join(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'sorl.thumbnail',
    'django_jcrop',
    'example',
)
