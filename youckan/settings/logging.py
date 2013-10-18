# -*- coding: utf-8 -*-
import sys

from youckan.settings.common import conf

# Different log files for web server and workers
logname = 'django'
if 'celeryd' in sys.argv:
    if '-Q' in sys.argv:
        position = sys.argv.index('-Q') + 1
        logname = 'celeryd.{}'.format(sys.argv[position])
    else:
        logname = 'celeryd'
elif 'celerycam' in sys.argv:
    logname = 'celerycam'
elif 'flower' in sys.argv:
    logname = 'flower'

LOG_LEVEL = conf['log']['level'].upper()

# Custom logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(asctime)s %(levelname)s %(message)s',
            'datefmt': '%Y/%m/%d %H:%M:%S',
        },
        'parseable': {
            'format': '[%(asctime)s][%(levelname)s][%(module)s] %(message)s',
            'datefmt': '%Y/%m/%d %H:%M:%S',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': LOG_LEVEL,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': conf['log']['file'].format(name=logname),
            'formatter': 'parseable',
            'when': 'midnight',
            'backupCount': '30',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'WARNING',
        },
        'django': {
            'handlers': ['null'],
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'youckan': {
            'level': LOG_LEVEL,
        },
        'youckan.error': {
            'level': 'ERROR',
        },
        'celery': {
            'level': LOG_LEVEL,
        },
    }
}
