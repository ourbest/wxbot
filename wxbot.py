import logging
import logging.config
import os
import sys
import traceback
import uuid
from time import strftime

import requests
from flask import Flask, session, render_template, jsonify, send_file, request
from werkzeug.exceptions import Unauthorized
from wxpy import Message

import bots
import cutt
import settings
from models import db_session, BotArticle
from settings import logger

app = Flask(__name__)

app.secret_key = settings.SECRET_KEY


@app.route('/')
def index():
    return render_template("index.html", version=settings.JS_VERSION)


@app.route('/bot/login', methods=['POST'])
def login():
    if settings.PWD == request.values.get('pwd'):
        session['login'] = True

    return jsonify(error=not is_login())


@app.route('/dist/<file>')
def dist(file):
    return send_file('static/dist/' + file, cache_timeout=24 * 30 * 3600)


@app.route('/bot/bots')
def get_bots():
    return jsonify(bots=list(bots.running_bots.keys()), master=bots.master_bot.self.name if bots.master_bot else '')


@app.before_request
def after_request():
    if request.path in ('/', '/bot/login', '/favicon.ico') or request.path.find('/dist') == 0:
        pass
    elif not is_login():
        raise Unauthorized()


@app.errorhandler(Exception)
def exceptions(e):
    ts = strftime('[%Y-%b-%d %H:%M]')
    tb = traceback.format_exc()
    logger.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s',
                 ts,
                 request.remote_addr,
                 request.method,
                 request.scheme,
                 request.full_path,
                 tb)

    if isinstance(e, Unauthorized):
        return "401", 401

    return "Internal Server Error", 500


@app.route('/bot/qr')
def get_qr():
    bot = bots.anonymous_bots[get_session_id()]

    qr = bot.get_qr()
    qr.seek(0)
    return send_file(qr, mimetype="image/png", cache_timeout=0)


@app.route('/bot/logout')
def logout():
    name = request.values.get('name')
    if bots.master_bot and bots.master_bot.name == name:
        return jsonify(code=2, message='不可以注销管理机器人')
    bot = bots.running_bots.get(name)
    if not bot:
        return jsonify(code=1, message="没有这个机器人")
    bot.logout()

    return jsonify(code=0)


@app.route('/bot/info')
def get_bot_info():
    name = request.values.get('name')
    bot = bots.running_bots.get(name)
    if not bot:
        return jsonify(code=1, message="没有这个机器人")
    return jsonify(code=0,
                   config={
                       'auto_accept': bot.auto_accept,
                       'crawler_articles': bot.crawler_articles,
                       'app_id': bot.app_id,
                       'auto_send': bot.auto_send,
                       'notify_dingding': bot.notify_dingding,
                       'master_phone': bot.master_phone,
                   },
                   friends=bot.friends().stats_text(),
                   mps=bot.mps().stats_text())


@app.route('/bot/post')
def post_items():
    bot = bots.running_bots.get('ourbest')
    if not bot:
        return jsonify(code=1, message="没有这个机器人")

    items = requests.get('https://tg.appgc.cn/api/jd/wx/items').json()
    if items.data:
        groups = items.data.groups
        for item in items.data.items:
            if item.type == 'Text':
                for group in groups:
                    grp = bot.groups().search(group)
                    if grp:
                        grp.send_msg(item.text)
            else:
                img = item.text
                content = requests.get('http://qn.zhiyueapp.cn/%s' % img).content

                path = "data/%s" % img
                with open(path, "w") as fd:
                    fd.write(content)
                for group in groups:
                    grp = bot.groups().search(group)
                    if grp:
                        grp.send_image(path)

                os.remove(path)


@app.route('/bot/qr/status')
def get_qr_status():
    bot = bots.anonymous_bots[get_session_id()]
    status = bot.check_login()
    message = "请扫描二维码"
    name = ""
    if status == '200':
        message = '登录成功'

        bot.post_login()

        del bots.anonymous_bots[get_session_id()]
        name = bot.self.name
    elif status == '201':
        message = '客户端确认'
    elif status == '408':
        message = '二维码已过期，请重新扫描'

    return jsonify(code=status, message=message, name=name)


@app.route('/bot/send/cutt', methods=['POST'])
def send_to_cutt():
    name = request.values.get('name')
    bot = bots.running_bots.get(name)
    app_id = '324160' if not bot else bot.app_id

    uid = request.values.get('id')
    if uid:
        article = BotArticle.query.filter_by(uid=uid).first()
        if article:
            cutt.post_article(app_id, article.title, article.content)
            # resp = requests.get(settings.QINIU_ROOT + article.key + ".gz")
            # if resp.ok:
            #     content = zlib.decompress(resp.content).decode('utf-8')
            #
            #     cutt.post_draft(article.title, content, article.cover)
            #     article.status = 1
            #     db_session().commit()
            article.status = 1
            db_session().commit()

    return jsonify(code=0)


@app.route('/bot/article/remove', methods=['POST'])
def remove_article():
    uid = request.values.get('id')
    article = BotArticle.query.filter_by(uid=uid).first()
    if article:
        session = db_session()
        article.status = -1
        session.commit()
    return jsonify(code=0)


def get_session_id():
    sid = session.get('sid')
    if not sid:
        sid = uuid.uuid4()
        session['sid'] = sid
    return sid


def is_login():
    return session.get('login')


@app.route('/favicon.ico')
def favicon():
    return '404', 404


@app.teardown_request
def shutdown_session(f=None):
    db_session.remove()


@app.route('/bot/article')
def web_page():
    uid = request.values.get('id')
    if uid:
        article = BotArticle.query.filter_by(uid=uid).first()
        if article:
            # path = 'data/content/%s/%s.html' % (article.created_at.strftime('%y%m%d'), uid)
            # if os.path.exists(path):
            #     with open(path, 'rt', encoding='utf-8') as fd:
            #         content = fd.read()
            #         return render_template('article.html', title=article.title,
            #                                author=article.sender, content=content)
            # else:
            #     resp = requests.get(settings.QINIU_ROOT + article.key + ".gz")
            #     if resp.ok:
            #         content = zlib.decompress(resp.content).decode('utf-8')
            #         return render_template('article.html', title=article.title,
            #                                author=article.sender, content=content)
            return render_template('article.html', title=article.title,
                                   author=article.sender, content=article.content)

    return '404', 404


@app.route('/bot/friends')
def friends():
    name = request.values.get('name')
    bot = bots.running_bots.get(name)
    if not bot:
        return jsonify(code=1, message="没有这个机器人")
    return jsonify(code=0, friends=[{'name': x.name,
                                     'sex': x.sex,
                                     'province': x.province,
                                     'remark_name': x.remark_name,
                                     'signature': x.signature,
                                     'city': x.city} for x in bot.friends()])


@app.route('/bot/mps')
def mps():
    name = request.values.get('name')
    bot = bots.running_bots.get(name)
    if not bot:
        return jsonify(code=1, message="没有这个机器人")
    return jsonify(code=0, mps=[{'name': x.name,
                                 'sex': x.sex,
                                 'province': x.province,
                                 'remark_name': x.remark_name,
                                 'signature': x.signature,
                                 'city': x.city} for x in bot.mps()])


@app.route('/bot/groups')
def groups():
    name = request.values.get('name')
    bot = bots.running_bots.get(name)
    if not bot:
        return jsonify(code=1, message="没有这个机器人")
    return jsonify(code=0, groups=[{'name': x.name,
                                    'owner': x.owner.name,
                                    'members': len(x.members)} for x in bot.groups()])


@app.route('/bot/messages')
def messages():
    name = request.values.get('name')
    bot = bots.running_bots.get(name)
    if not bot:
        return jsonify(code=1, message="没有这个机器人")

    return jsonify(code=0, messages=[{
        'sender': x.member.name if isinstance(x, Message) and x.member else x.sender.name,
        'chat': x.chat.name,
        'type': x.type,
        'message': x.text,
        'created_at': x.create_time.strftime('%Y-%m-%d %H:%M:%S')
    } for x in bot.messages][::-1])


@app.route('/bot/articles')
def articles():
    name = request.values.get('name')
    page = request.values.get('page')
    try:
        if not page:
            page = 0
        else:
            page = int(page)
    except:
        page = 0

    msgs = BotArticle.query.filter(BotArticle.bot_name == name, BotArticle.status >= 0) \
        .order_by(BotArticle.created_at.desc()).offset(100 * page).limit(100).all()
    return jsonify(code=0,
                   total=BotArticle.query.filter(BotArticle.bot_name == name, BotArticle.status >= 0).count(),
                   articles=[{
                       'sender': x.sender,
                       'title': x.title,
                       'cover': x.cover,
                       'id': x.uid,
                       'status': x.status,
                       'created_at': x.created_at.strftime('%Y-%m-%d %H:%M:%S')
                   } for x in msgs])


@app.route('/bot/master/assign')
def set_master():
    name = request.values.get('name')
    bot = bots.running_bots.get(name)

    if not bot:
        return jsonify(code=1, message="没有这个机器人")

    if bots.master_bot:
        bots.master_bot.self_msg('确认切换监控账号为【%s】吗？\n请回复【确认替换】' % name)
        bots.master_bot.to_confirm_replace = bot
        return jsonify(code=2, message='已发送确认信息')

    bots.set_master_bot(bot)
    return jsonify(code=0, message='设置成功')


@app.route('/bot/master')
def get_master():
    return jsonify(code=0 if bots.master_bot else 1, name=bots.master_bot.name if bots.master_bot else '')


@app.route('/bot/config', methods=['POST'])
def set_config():
    name = request.values.get('name')
    bot = bots.running_bots.get(name)
    key = request.values.get('key')

    if not bot:
        return jsonify(code=1, message="没有这个机器人")

    if hasattr(bot, key):
        value = request.values.get('value')
        if key == 'app_id' or value not in ('true', 'false'):
            # bot.app_id = value
            setattr(bot, key, value)
        else:
            setattr(bot, key, 'true' == value)
        bot.save_config()
    return jsonify(code=0, message='设置成功')


@app.route('/bot/article/content')
def get_article_content():
    uid = request.values.get('id')
    if uid:
        article = BotArticle.query.filter_by(uid=uid).first()
        if article:
            # path = 'data/content/%s/%s.html' % (article.created_at.strftime('%y%m%d'), uid)
            # if os.path.exists(path):
            #     with open(path, 'rt', encoding='utf-8') as fd:
            #         content = fd.read()
            #         return jsonify(code=0, content=content)
            #
            # resp = requests.get(settings.QINIU_ROOT + article.key + ".gz")
            # if resp.ok:
            #     content = zlib.decompress(resp.content).decode('utf-8')
            #     return jsonify(code=0, content=content)
            content = article.content
            if content:
                return jsonify(code=0, content=content)

    return '404', 404


@app.route('/bot/article/content/update', methods=['POST'])
def update_article_content():
    uid = request.values.get('id')
    content = request.values.get('content')
    if uid:
        article = BotArticle.query.filter_by(uid=uid).first()
        if article:
            path = 'data/content/%s' % article.created_at.strftime('%y%m%d')
            os.makedirs(path, exist_ok=True)
            with open("%s/%s.html" % (path, uid), "wt", encoding='utf-8') as fd:
                fd.write(content)
            #
            # uploader.upload_to_qiniu(article.key + ".gz",
            #                          zlib.compress(content.encode('utf-8')))
            return jsonify(code=0, message='OK')

    return '404', 404


def init():
    from raven.contrib.flask import Sentry
    Sentry(app, dsn=settings.SENTRY_DSN)
    if not bots.running_bots:
        bots.load_bots()
    logging.config.dictConfig(settings.LOGGING)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'prod':
        init()
        app.run(host="0.0.0.0")
    else:
        logger.info('App start')
        if app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
            init()

        app.run(debug=True)
else:
    init()
