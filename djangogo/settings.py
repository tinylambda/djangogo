"""
Django settings for djangogo project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import atexit
import os
import copy
import configparser
from core.utils import ConfigWriterWithRepeatKeys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j-s&#fnl*ua%x3r61m^at!m6g(cd%ioxh0m=mb!kfg4l%f@(ej'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_beat',
    'rest_framework',
    'rest_framework.authtoken',
    'accounts',
    'core',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djangogo.urls'

PROJECT_TAG = 'djangogo_default_project'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'djangogo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = f'/tmp/{PROJECT_TAG}/static_root/'  # Change this as needed

AUTH_USER_MODEL = 'accounts.User'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'default': {
            'format': '{levelname}\t{asctime}\t{pathname}\t{lineno:d}\t{process:d}\t{message}',
            'style': '{',
        }
    },

    'handlers': {
        'console_log_handler': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        }
    },

    'loggers': {
        'default': {
            'handlers': ['console_log_handler'],
            'level': 'INFO',
            'propagate': False,
        }
    }
}


CORS_ORIGIN_WHITELIST = [
    "http://127.0.0.1:4200",
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

CORS_ALLOW_CREDENTIALS = True


CELERY_BROKER_URL = 'redis://:rpassword@127.0.0.1:6379/2'

CELERY_ACCEPT_CONTENT = ['application/json']

CELERY_ENABLE_UTC = False

CELERY_TIMEZONE = 'Asia/Shanghai'

CELERY_WORKER_PREFETCH_MULTIPLIER = 1

CELERY_TASK_SERIALIZER = 'json'

CELERY_TASK_CREATE_MISSING_QUEUES = True

CELERY_TASK_ACKS_LATE = True

CELERY_TASK_ROUTES = {
    'chaos.celery.debug_task': {'queue': 'queueDebug'},
}

CELERY_TASK_DEFAULT_QUEUE = 'celeryDefault'

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

CELERY_BEAT_MAX_LOOP_INTERVAL = 5


UWSGI_CONFIG = ConfigWriterWithRepeatKeys()
UWSGI_CONF_FILENAME = os.path.join(BASE_DIR, 'run', f'uwsgi.{PROJECT_TAG}.ini')

UWSGI_INSTANCE_CONFIG = {
    'env': 'DJANGO_SETTINGS_MODULE=djangogo.settings',
    'chdir': BASE_DIR,
    'module': WSGI_APPLICATION.replace('.application', ':application'),
    'master': 'true',
    'pidfile': os.path.join(BASE_DIR, 'run', f'uwsgi.{PROJECT_TAG}.pid'),
    'http': ['0.0.0.0:8000'],
    'socket': '127.0.0.1:0',
    'harakiri': '20',
    'vacuum': 'true',
    'processes': '2',
    'threads': '2',
    'enable-threads': 'true',
    'no-threads-wait': 'true',
    'max-requests': '5000',
    'max-requests-delta': '3',
    'lazy-apps': 'true',
    'touch-chain-reload': os.path.join(BASE_DIR, 'run', f'uwsgi.{PROJECT_TAG}.touch'),
    'disable-logging': 'false',
    'log-master': 'true',  # delegate logging to master process
    'stats': '0.0.0.0:9191',
    'stats-http': 'true',
    'static-map': [f'/static={STATIC_ROOT}'],
}

UWSGI_CONFIG.add_section('uwsgi')
for setting_key in UWSGI_INSTANCE_CONFIG:
    setting_value = UWSGI_INSTANCE_CONFIG[setting_key]
    UWSGI_CONFIG.set('uwsgi', setting_key, setting_value)


CIRCUSD_CONFIG = configparser.ConfigParser()
CIRCUSD_CONF_FILENAME = os.path.join(BASE_DIR, 'run', f'circusd.{PROJECT_TAG}.ini')
CIRCUSD_PID_FILENAME = os.path.join(BASE_DIR, 'run', f'circusd.{PROJECT_TAG}.pid')
CIRCUSD_LOG_ROOT_DIR = f'/tmp/log/{PROJECT_TAG}/circus'

CIRCUSD_STATIC_CONFIG_LIST = [
    {
        'name': 'circus',
        'settings': {
            'endpoint': 'tcp://127.0.0.1:5555',
            'endpoint_owner': 'None',
            'pubsub_endpoint': 'tcp://127.0.0.1:5556',
            'statsd': 'False',
            'stats_endpoint': 'tcp://127.0.0.1:5557',
            'stats_close_outputs': 'False',
            'check_delay': '5',
            'stream_backend': 'thread',
            'warmup_delay': '0',
            'debug': 'False',
            'debug_gc': 'False',
            'pidfile': os.path.join(BASE_DIR, 'run', f'circusd.{PROJECT_TAG}.pid'),
            'umask': '002',
            'loglevel': 'INFO',
            'logoutput': '-',
            'loggerconfig': ''
        }
     },
]

for CIRCUSD_STATIC_CONFIG in CIRCUSD_STATIC_CONFIG_LIST:
    section_name = CIRCUSD_STATIC_CONFIG['name']
    settings = CIRCUSD_STATIC_CONFIG['settings']

    CIRCUSD_CONFIG.add_section(section_name)
    for setting_key in settings:
        setting_value = settings[setting_key]
        CIRCUSD_CONFIG.set(section_name, setting_key, setting_value)


CIRCUS_WATCHER_DEFAULT_SETTINGS = {
    'cmd': '/bin/cat',
    'args': '',
    'shell': 'False',
    'shell_args': 'None',
    'working_dir': BASE_DIR,
    # 'uid': '',  # current uid is the default
    # 'gid': '',  # current gid is the default
    'copy_env': 'True',  # If true, the local env vars will be copied and passed to the workers when spawning them.
    'copy_path': 'False',  # If true, sys.path is passed to the subprocess env using PYTHONPATH. copy_env has to be True
    'warmup_delay': '1',
    'autostart': 'False',
    'numprocesses': '1',
    'stderr_stream.class': 'FileStream',
    'stderr_stream.filename': os.path.join(CIRCUSD_LOG_ROOT_DIR, '{watcher_name:s}.error.log'),
    'stderr_stream.time_format': '%%Y-%%m-%%d %%H:%%M:%%S',
    'stderr_stream.max_bytes': '1073741824',
    'stderr_stream.backup_count': '5',
    'stdout_stream.class': 'FileStream',
    'stdout_stream.filename': os.path.join(CIRCUSD_LOG_ROOT_DIR, '{watcher_name:s}.info.log'),
    'stdout_stream.time_format': '%%Y-%%m-%%d %%H:%%M:%%S',
    'stdout_stream.max_bytes': '1073741824',
    'stdout_stream.backup_count': '5',
    'close_child_stdin': 'True',
    'close_child_stdout': 'False',
    'close_child_stderr': 'False',
    'send_hup': 'False',
    'stop_signal': 'INT',
    'stop_children': 'False',
    'max_retry': '2',
    'graceful_timeout': '30',
    'priority': '0',
    'singleton': 'True',
    'use_sockets': 'False',
    # 'max_age': '100000',  # Default disabled
    # 'max_age_variance': ,  # Variate above
    'virtualenv': os.path.join(BASE_DIR, 'venv'),  # root of a virtualenv directory. need copy_env to be True
    # 'virtualenv_py_ver': '',  # specify python version, must be used with virtualenv
    'respawn': 'True',  # If set to False, the processes handled by a watcher will not be respawned automatically.
    # 'use_papa': 'False',
}

CIRCUS_SOCKETS = [
    {
        'name': 'djangogo_in_asgi_socket',
        'settings': {
            'host': '0.0.0.0',
            'port': '20000',
        }
    }
]

CIRCUS_ENVS = [
    {
        'name': 'djangogo_http',
        'settings': {
        }
    },
    {
        'name': 'djangogo_in_asgi',
        'settings': {
        }
    },
]

CIRCUS_WATCHERS = [
    {
        'name': 'djangogo_http',
        'settings': {
            'cmd': 'python manage.py uwsgi start',
            'stop_signal': 'INT',
            'singleton': 'True',
            'autostart': 'True',
            'use_sockets': 'False',
        }
    },
    {
        'name': 'djangogo_in_asgi',
        'settings': {
            'cmd': 'python manage.py daphne start --fd $(circus.sockets.djangogo_in_asgi_socket) '
                   '--app djangogo.asgi:application',
            'use_sockets': 'True',
            'singleton': 'False',
            'autostart': 'False',
            'numprocesses': '3',
        }
    },
]

for CIRCUS_SOCKET in CIRCUS_SOCKETS:
    name = CIRCUS_SOCKET['name']
    settings = CIRCUS_SOCKET['settings']
    section_name = f'socket:{name}'

    CIRCUSD_CONFIG.add_section(section_name)
    for setting_key in settings:
        setting_value = settings[setting_key]
        CIRCUSD_CONFIG.set(section_name, setting_key, setting_value)

for CIRCUS_ENV in CIRCUS_ENVS:
    name = CIRCUS_ENV['name']
    settings = CIRCUS_ENV['settings']
    section_name = f'env:{name}'
    for setting_key in settings:
        setting_value = settings[setting_key]
        CIRCUSD_CONFIG.set(section_name, setting_key, setting_value)

for CIRCUS_WATCHER in CIRCUS_WATCHERS:
    name = CIRCUS_WATCHER['name']
    watcher_settings = CIRCUS_WATCHER['settings']
    settings = copy.copy(CIRCUS_WATCHER_DEFAULT_SETTINGS)
    settings.update(watcher_settings)
    section_name = f"watcher:{name}"
    render_context = {"watcher_name": name}

    CIRCUSD_CONFIG.add_section(section_name)
    for setting_key in settings:
        setting_value = settings[setting_key]
        setting_value = setting_value.format(**render_context)
        CIRCUSD_CONFIG.set(section_name, setting_key, setting_value)


@atexit.register
def cleanup():
    """
    Will be called before the worker process exits
    Add more cleanup as you need.
    """
    pass


