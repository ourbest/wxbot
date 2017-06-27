import re

import requests

CUTT_HOST = 'http://cms.cutt.com'

session = requests.session()
session.has_logged = False


def login_cutt():
    resp = session.post(CUTT_HOST + '/j_security_check.json',
                        {'j_username': 'monotonic.chs@qq.com', 'j_password': 'fMs3DteCSa', 'type': 'CMS'}).json()

    if resp.get('result') == 0:
        session.has_logged = True


def upload_image(url):
    if not session.has_logged:
        login_cutt()

    # resp = session.post(CUTT_HOST + '/image/uploadImgUrl.json', {'url': url}).json()
    resp = session.post(CUTT_HOST + '/image/getImage.json', {'url': url}).json()
    return ('http://qn.cutt.com/' + resp.get('data') + '/2') if resp.get('code') == 0 else url


def post_article(app_id, title, content):
    if not session.has_logged:
        login_cutt()

    resp = session.post(CUTT_HOST + '/cut/saveMp.json', {
        'title': title,
        'content': content,
        'p_id': app_id
    }).json()
    return resp.get('result')


def post_draft(title, html, cover):
    if not session.has_logged:
        login_cutt()

    resp = session.post(CUTT_HOST + '/cut/draft.json', {
        'title': title,
        'imageId': cover[19:-2],
        'content': 'ZhiyueMD<style>#js_content {font-size: 16px;word-wrap: break-word;-webkit-hyphens: auto;-ms-hyphens: auto;hyphens: auto;width: 740px;margin-left: auto;margin-right: auto;}#js_content table {margin-bottom: 10px;border-collapse: collapse;display: table;width: 100% !important;}#js_content * { max-width: 100% !important;box-sizing: border-box !important;-webkit-box-sizing: border-box !important;word-wrap: break-word !important;}</style>%s' % html
    }).json()

    return resp.get('result')


IMG_RE = re.compile(r'<img src="http://qn.cutt.com/(.+?)/2"/>', re.IGNORECASE)


def convert_html(html):
    md = IMG_RE.sub(r'![图片](\1)', html)
    return 'ZhiyueMD' + md
