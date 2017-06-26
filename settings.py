import os

SENTRY_DSN = 'https://c6eb05490aeb4f0088e45320b06160aa:74d3695c209944eb975a9e2d6dff2b04@sentry.io/183612'
SECRET_KEY = 'A0Zr98jdai12oqwjo/3yX R~XHH!jmN]LWX/,?RT'
JS_VERSION = '0d21017595c41b7bd284'

QINIU_ACCESS_KEY = 'TKO16BTj6tlUja1wNjRQu1tZnvx8sXFfoHdKJrOA'
QINIU_SECRET_KEY = 'TZH53PQ_hDOx2RaXgr5OEm_m4onpNNECUKpzc9sF'
QINIU_BUCKET = 'mpresources'
QINIU_ROOT = 'http://os23y083b.bkt.clouddn.com/'


def load_settings():
    import settings
    for k, v in os.environ.items():
        if v and k.startswith('BOT_'):
            name = k[4:]
            if hasattr(settings, name):
                setattr(settings, name, v)

load_settings()