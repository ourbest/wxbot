import hashlib
import logging
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from wxpy import MP

import cutt
from models import db_session, BotArticle

logger = logging.getLogger(__name__)


def crawler(message):
    # bot = message.bot
    if message.chat.__class__ == MP:
        articles = message.articles
        """
        title: 标题
        summary: 摘要
        url: 文章 URL
        cover: 封面或缩略图 URL
        """
        if articles:
            for article in articles:
                if article.url.startswith('https://open.weixin.qq.com/connect/oauth2/authorize'):
                    continue
                bs_article = BeautifulSoup(_fetch(article.url), "lxml")

                content = bs_article.find(id='js_content')

                if content:
                    logger.info('[%s] 文章 %s - %s' % (message.bot.bot_name, message.chat.name, article.title))
                    _save_article(message.bot, message.chat.name, article.title, content, article.url, article.cover)


def _fetch(url, text=True):
    return requests.get(url).text if text else requests.get(url).content


def _save_article(bot, user, title, content, url, cover):
    key_prefix = 'mp/%s/%s/%s' % (user, datetime.now().strftime('%y%m%d'), title)

    images = content.find_all("img")

    for image in images:
        # img_path = os.path.join(image['data-src'].split('/')[4])
        # image_content = _fetch(image['data-src'], text=False)
        image_url = cutt.upload_image(image['data-src'])
        # uploader.upload_to_qiniu(key_prefix + "/images/" + img_path, image_content)
        image.attrs.clear()
        # del image['data-src']
        image['src'] = image_url

    # uploader.upload_to_qiniu(key_prefix + ".gz",
    #                          zlib.compress(str(content).encode('utf-8')))  # , mime_type="text/html")
    # uploader.upload_to_qiniu(key_prefix + ".url", url)
    # uploader.upload_to_qiniu(key_prefix + ".cover", _fetch(cover, text=False))

    session = db_session()
    msg = BotArticle(bot_name=bot.self.name, uid=hashlib.md5(url.encode('utf-8')).hexdigest(),
                     cover=cutt.upload_image(cover), status=0,
                     sender=user, title=title, key=key_prefix, created_at=datetime.now())

    msg.content = str(content)
    session.add(msg)

    if bot.auto_send:
        cutt.post_article(bot.app_id, title, content)
        msg.status = 1

    session.commit()


def _test_url(title, url, cover=None):
    text = _fetch(url)
    root = BeautifulSoup(text, "lxml")
    content = root.find(id='js_content')
    images = content.find_all("img")

    for image in images:
        image_url = cutt.upload_image(image['data-src'])
        image.attrs.clear()
        image['src'] = image_url

    cutt.post_draft(title, str(content), cover)

    return str(content)
