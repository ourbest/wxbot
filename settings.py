import logging
import os

SENTRY_DSN = 'https://c6eb05490aeb4f0088e45320b06160aa:74d3695c209944eb975a9e2d6dff2b04@sentry.io/183612'
SECRET_KEY = 'A0Zr98jdai12oqwjo/3yX R~XHH!jmN]LWX/,?RT'
JS_VERSION = '6823e50770363aaa15ee'



def load_settings():
    import settings
    for k, v in os.environ.items():
        if v and k.startswith('BOT_'):
            name = k[4:]
            if hasattr(settings, name):
                setattr(settings, name, v)


load_settings()

logging_path = 'data/logs'

if not os.path.exists(logging_path):
    os.makedirs(logging_path, exist_ok=True)

LOGGING = {
    "version": 1,
    "handlers": {
        "debug": {
            'level': 'DEBUG',
            'class': 'commons.SafeRotatingFileHandler',
            'when': 'midnight',
            "formatter": "simple",
            "filename": logging_path + "/debug.log"
        },

        "wxbot": {
            'level': 'DEBUG',
            'class': 'commons.SafeRotatingFileHandler',
            'when': 'midnight',
            "formatter": "simple",
            "filename": logging_path + "/wxbot.log"
        },

        'access_file': {
            'level': 'INFO',
            'class': 'commons.SafeRotatingFileHandler',
            'filename': logging_path + "/access.log",
            'when': 'midnight',
            'formatter': 'generic',
            'encoding': 'utf-8',
        },
    },
    "loggers": {
        'root': {
            'level': 'INFO',
            'handlers': ["debug"],
        },

        'wxbot': {
            'level': 'INFO',
            'propagate': False,
            'handlers': ["wxbot"],
        },
        'werkzeug': {
            'level': 'INFO',
            'handlers': ['debug'],
            'propagate': False,
        },
        'gunicorn.access': {
            'level': 'INFO',
            'handlers': ['access_file'],
            'propagate': False,
        },
    },

    "formatters": {
        "simple": {
            "format": "%(asctime)s - %(levelname)s - %(message)s"
        },
        'generic': {
            'format': '%(message)s'
        },
    }
}

logger = logging.getLogger('wxbot')
