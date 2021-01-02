import logging
import os

SENTRY_DSN = 'http://c7445f10efde4e1499765af810268806:c43aacb712a84b188b0860d80fa42f7a@10.9.144.173:9000/6'
SECRET_KEY = 'A0Zr98jdai12oqwjo/3yX R~XHH!jmN]LWX/,?RT'
JS_VERSION = 'd15891dfaa7139aeea09'

DINGDING_TOKEN = 'd3f5c74d4dea6d2bd4836a97c45110770d1fc48addefb519e31dbeaf1f740767'
PWD = 'woshijianwangyuangong'
IMG_DOMAIN = 'qn.jwshq.cn'
TG_DOMAIN = 'tg.jwshq.cn'


def load_settings():
    import settings
    for k, v in os.environ.items():
        if v and k.startswith('BOT_'):
            name = k[4:]
            if hasattr(settings, name):
                setattr(settings, name, v)


load_settings()

logging_path = 'bots/logs'

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
