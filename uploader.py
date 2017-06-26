from qiniu import Auth, put_data

from settings import *

qiniu_auth = Auth(QINIU_ACCESS_KEY, QINIU_SECRET_KEY)


def upload_to_qiniu(key, content, mime_type='application/octet-stream'):
    token = qiniu_auth.upload_token(QINIU_BUCKET, key, 3600)
    info, ret = put_data(token, key, content, mime_type=mime_type)
    if ret.status_code == 200:
        return QINIU_ROOT + key
