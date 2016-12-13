#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import socket
import os
from datetime import timedelta

if socket.gethostname() == 'hp2':
    DEBUG = False
    HOST = '127.0.0.1'
else:
    DEBUG = True
    HOST = '10.145.17.17'
    #HOST = '10.145.17.27'

ALLOWED_HOSTS = ['*']

ADMINS = (
    ('Khodyrev Dmitry', 'chaos777@mail.ru'),
)

MANAGERS = ADMINS
#APPEND_SLASH = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mscstatdb',              
        'USER': 'admin',                
        'PASSWORD': 'admin11',          
        'HOST': HOST,
        'PORT': '',                     
    }
}

########## Celery

os.environ["CELERY_LOADER"] = "django"
#os.environ['DJANGO_SETTINGS_MODULE'] = 'mscstat.settings'

# Sensible settings for celery
CELERY_ENABLE_UTC  = True
CELERY_TIMEZONE = 'Europe/Moscow'
CELERY_ALWAYS_EAGER = False # for debuging True
CELERY_ACKS_LATE = True
CELERY_TASK_PUBLISH_RETRY = True
CELERY_DISABLE_RATE_LIMITS = False

# адрес redis сервера
BROKER_URL = "redis://"+HOST+":6379/0"
# храним результаты выполнения задач так же в redis
CELERY_RESULT_BACKEND = "redis://"+HOST+":6379/0"
# Время, через которое хранимый в результат будет удалён: 7 дней
CELERY_TASK_RESULT_EXPIRES = 600#7*86400
# это нужно для мониторинга наших воркеров
CELERY_SEND_EVENTS = True
# место хранения периодических задач (данные для планировщика)
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"

CELERY_TASK_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ['application/json']

CELERYCAM_EXPIRE_SUCCESS = timedelta(days=1)
CELERYCAM_EXPIRE_ERROR = timedelta(days=3)
CELERYCAM_EXPIRE_PENDING = timedelta(days=5)

CELERYD_MAX_TASKS_PER_CHILD = 1

import djcelery
djcelery.setup_loader()

########## END Celery

TIME_ZONE = 'Europe/Moscow'

LANGUAGE_CODE = 'ru-RU'
DATE_FORMAT = 'Y-m-d'
DATETIME_FORMAT = 'Y-m-d H:i'
DATE_INPUT_FORMATS = ('%Y-%m-%d',)
DATETIME_INPUT_FORMATS = ('%Y-%m-%d %H:%M',)

SITE_ID = 1

USE_I18N = True

USE_L10N = False

USE_TZ = False

AUTH_USER_MODEL = 'mscstatauth.User'

PROJECT_PATH = os.path.dirname(__file__)
MEDIA_ROOT = os.path.join(os.path.split(PROJECT_PATH)[0],"mscstatapp/media")

MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(os.path.split(PROJECT_PATH)[0],"mscstatapp/static")

STATIC_URL = '/static/'

STATICFILES_DIRS = (

)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#   'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = 't!ji14js0k%pl0^p5&box0=xo7q8#@q1v%p92$d(o=$cq-q9nj'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(os.path.split(PROJECT_PATH)[0],"mscstatapp/templates")
        ],
        #'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                'django.template.context_processors.request'
            ],
            'loaders': [
                'admin_tools.template_loaders.Loader',
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                'django.template.loaders.eggs.Loader',
            ]
        },
    },
]
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'mscstat.urls'

WSGI_APPLICATION = 'mscstat.wsgi.application'

INSTALLED_APPS = (

    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.admin',
    'rest_framework',
    'djcelery',
    'mscstatauth',
    "rapidsms",
    "rapidsms.router.db",
    'smart_selects',
    'mscstatapp',
    'smsapp',
)

#INTERNAL_IPS = ('127.0.0.1',)
#INSTALLED_APPS += ('debug_toolbar', )

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.DjangoModelPermissions',),
    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework.authentication.SessionAuthentication',),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'PAGINATE_BY_PARAM': 'limit',
    'DATETIME_INPUT_FORMATS': ('%Y-%m-%d %H:%M',),
    'DATETIME_FORMATS': ('%Y-%m-%d %H:%M',),  
}
########## Rapid SMS
INSTALLED_BACKENDS = {
    "kannel-beeline-smpp" : {
        "ENGINE":  "rapidsms.backends.kannel.KannelBackend",
        "sendsms_url": "http://10.145.17.17:13013/cgi-bin/sendsms",
        "sendsms_params": {
             "from": "mscstat",
             "username": "rapidsms",
             "password": "rapidsms1511"
        },
        "coding": 2,
        "charset": "utf-8",
        "encode_errors": "ignore", # strip out unknown (unicode) characters
    },
}
#RAPIDSMS_ROUTER = "rapidsms.router.blocking.BlockingRouter"
#RAPIDSMS_ROUTER = "rapidsms.router.celery.CeleryRouter"
RAPIDSMS_ROUTER = "rapidsms.router.db.DatabaseRouter"
DB_ROUTER_DEFAULT_BATCH_SIZE = 200
SMS_APPS = ['smsapp']
########## END Rapid SMS

ADMIN_TOOLS_INDEX_DASHBOARD = 'mscstatapp.dashboard.CustomIndexDashboard'
ADMIN_TOOLS_THEMING_CSS = 'css/admin_tools_theming.css'

########## TESTRUNNER CONFIGURATION
TEST_RUNNER = 'django.test.runner.DiscoverRunner'
########## END TESTRUNNER CONFIGURATION

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': HOST+":11211",
    }
}

import logging, copy
from django.utils.log import DEFAULT_LOGGING

LOGGING = copy.deepcopy(DEFAULT_LOGGING)
LOGGING['filters']['suppress_deprecated'] = {'()': 'mscstat.settings.SuppressDeprecated'}
LOGGING['handlers']['console']['filters'].append('suppress_deprecated')
LOGGING['handlers']['file'] = {'level' : 'DEBUG'}
LOGGING['handlers']['file']['class'] = 'logging.FileHandler'
LOGGING['handlers']['file']['filename'] = os.path.join(os.path.split(PROJECT_PATH)[0],"log/debug.log")
LOGGING['loggers']['django.request'] = {'handlers':['file']}
LOGGING['loggers']['django.request']['level'] = ('DEBUG')
LOGGING['loggers']['django.request']['propagate'] = True

class SuppressDeprecated(logging.Filter):
    def filter(self, record):
        WARNINGS_TO_SUPPRESS = [
            'RemovedInDjango110Warning',
        ]
        # Return false to suppress message.
        return not any([warn in record.getMessage() for warn in WARNINGS_TO_SUPPRESS])