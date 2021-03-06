import base64
import re
from datetime import datetime

import requests

import settings
from settings import logger

CUTT_HOST = 'http://cms.cutt.com'

session = requests.session()
session.has_logged = False


def login_cutt():
    resp = session.post(CUTT_HOST + '/j_security_check.json',
                        {'j_username': 'monotonic.chs@qq.com', 'j_password': 'x', 'type': 'CMS'}).json()

    if resp.get('result') == 0:
        session.has_logged = True


def upload_image(url):
    if not session.has_logged:
        login_cutt()

    # resp = session.post(CUTT_HOST + '/image/uploadImgUrl.json', {'url': url}).json()
    resp = session.post(CUTT_HOST + '/image/getImage.json', {'url': url}).json()
    if not resp.get('data'):
        raw = requests.get(url).content
        resp = session.post(CUTT_HOST + '/image/getImage.json', {'url': to_data_url(raw)}).json()
    return ('http://qn.cutt.com/%s/2' % resp.get('data')) if resp.get('code') == 0 and resp.get('data') else url


def post_article(app_id, title, content):
    if not session.has_logged:
        login_cutt()

    logger.info('Send to cutt: %s' % title)
    resp = session.post(CUTT_HOST + '/cut/saveMp.json', {
        'title': title,
        'content': to_cutt_md(content),
        'p_id': app_id
    }).json()
    return resp.get('result')


def post_draft(title, html, cover):
    if not session.has_logged:
        login_cutt()

    resp = session.post(CUTT_HOST + '/cut/draft.json', {
        'title': title,
        'imageId': cover[19:-2],
        'content': to_cutt_md(html)
    }).json()

    return resp.get('result')


def to_cutt_md(html):
    return 'ZhiyueMD<style>#js_content {font-size: 16px;word-wrap: break-word;-webkit-hyphens: auto;' \
           '-ms-hyphens: auto;hyphens: auto;width: 740px;margin-left: auto;margin-right: auto;}' \
           '#js_content table {margin-bottom: 10px;border-collapse: collapse;display: table;width: 100%% !important;}' \
           '#js_content * { max-width: 100%% !important;box-sizing: border-box !important;' \
           '-webkit-box-sizing: border-box !important;word-wrap: break-word !important;}</style>%s' % html


def to_data_url(image):
    base_encoded = base64.b64encode(image).decode()
    return 'data:image/png;base64,%s' % base_encoded


IMG_RE = re.compile(r'<img src="http://qn.cutt.com/(.+?)/2"/>', re.IGNORECASE)


def convert_html(html):
    md = IMG_RE.sub(r'![图片](\1)', html)
    return 'ZhiyueMD' + md


def send_dingding_msg(msg, phone):
    # https://oapi.dingtalk.com/robot/send?access_token=114b9ee24111a47f7dd9864195f905ed766c92ddb3c1b346b70d6bf3d4a3ae0d
    url = 'https://oapi.dingtalk.com/robot/send?access_token=' + settings.DINGDING_TOKEN
    dingding_msg = {
        'msgtype': 'text',
        'text': {
            'content': msg
        },
        'at': {
            'atMobiles': [phone],
            'isAtAll': False
        }
    } if phone else {
        'msgtype': 'text',
        'text': {
            'content': msg
        }
    }
    requests.post(url, json=dingding_msg)
