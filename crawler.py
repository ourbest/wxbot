import hashlib
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from wxpy import MP

import cutt
from models import db_session, BotArticle
from settings import logger


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
                    logger.info("[%s] ignore %s url %s" % (message.bot.bot_name, message, article.url))
                    continue
                article_content = _fetch(article.url)
                bs_article = BeautifulSoup(article_content, "lxml")

                content = bs_article.find(id='js_content')

                if content:
                    logger.info('[%s] 文章 %s - %s' % (message.bot.bot_name, message.chat.name, article.title))
                    _save_article(message.bot, message.chat.name, article.title, content, article.url, article.cover)

                    # bot = message.bot
                    # if bot.notify_dingding:
                    #     cutt.send_dingding_msg('%s推送了一篇文章【%s】%s'
                    #                            % (message.chat.name, articles[0].title, articles[0].url),
                    #                            bot.master_phone)
                else:
                    logger.warning(
                        '[%s] Cannot find js_content and content is %s' % (message.bot.bot_name, article_content))


def _fetch(url, text=True):
    val = requests.get(url, proxies={
        'http': 'http://10.9.131.47:3128',
        'https': 'http://10.9.131.47:3128'
    })
    return val.text if text else val.content


def _save_article(bot, user, title, content, url, cover):
    logger.info('[%s] Save article %s' % (bot.bot_name, title))
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

    # session = db_session()
    # msg = BotArticle(bot_name=bot.self.name, uid=hashlib.md5(url.encode('utf-8')).hexdigest(),
    #                 cover=cutt.upload_image(cover), status=1 if bot.auto_send else 0,
    #                 sender=user, title=title, key=key_prefix, created_at=datetime.now())

    # msg.content = str(content)
    # session.add(msg)

    # cutt.notify_internal(user, title, url, msg.content, msg.cover)
    cutt.notify_internal(user, title, url, str(content), cutt.upload_image(cover))

    # if bot.auto_send:
    #     cutt.post_article(bot.app_id, title, content)

    # session.commit()


def _test_url(title, url, cover=None):
    text = _fetch(url)
    root = BeautifulSoup(text, "lxml")
    content = root.find(id='js_content')
    images = content.find_all("img")

    for image in images:
        style = image['style'] if image.has_attr('style') else ''
        image_url = cutt.upload_image(image['data-src'])
        image.attrs.clear()
        image['src'] = image_url
        if style:
            image['style'] = style

    cutt.post_draft(title, str(content), cover)

    return str(content)
