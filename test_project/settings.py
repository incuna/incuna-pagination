import os

import dj_database_url


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True
ALLOWED_HOSTS = []
STATIC_URL = '/static/'

SECRET_KEY = 'not-for-production'
PASSWORD_HASHERS = ('django.contrib.auth.hashers.MD5PasswordHasher',)

DATABASES = {
    'default': dj_database_url.config(default='postgres://localhost/pagination')
}
DEFAULT_FILE_STORAGE = 'inmemorystorage.InMemoryStorage'

INSTALLED_APPS = (
    'pagination',
    'pagination.tests',

    # Put contenttypes before auth to work around test issue.
    # See: https://code.djangoproject.com/ticket/10827#comment:12
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.core.context_processors.request',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

TEST_RUNNER = 'test_project.test_runner.Runner'
