from qiniu import Auth, put_data

qiniu_access_key = 'TKO16BTj6tlUja1wNjRQu1tZnvx8sXFfoHdKJrOA'
qiniu_secret_key = 'TZH53PQ_hDOx2RaXgr5OEm_m4onpNNECUKpzc9sF'

qiniu_bucket = 'mpresources'

qiniu_auth = Auth(qiniu_access_key, qiniu_secret_key)

qiniu_root = 'http://os23y083b.bkt.clouddn.com/'


def upload_to_qiniu(key, content, mime_type='application/octet-stream'):
    token = qiniu_auth.upload_token(qiniu_bucket, key, 3600)
    info, ret = put_data(token, key, content, mime_type=mime_type)
    if ret.status_code == 200:
        return qiniu_root + key
