import sys
import uuid
import zlib

import requests
from flask import Flask, session, render_template, jsonify, send_file, request

import bots
import settings
from models import db_session, BotArticle, BotMessage

app = Flask(__name__)

app.secret_key = settings.SECRET_KEY


@app.route('/')
def index():
    return render_template("index.html", version=settings.JS_VERSION)


@app.route('/dist/<file>')
def dist(file):
    return send_file('static/dist/' + file, cache_timeout=24 * 30 * 3600)


@app.route('/bot/bots')
def get_bots():
    return jsonify(bots=list(bots.running_bots.keys()), master=bots.master_bot.self.name if bots.master_bot else '')


@app.route('/bot/qr')
def get_qr():
    bot = bots.anonymous_bots[get_session_id()]

    qr = bot.get_qr()
    qr.seek(0)
    return send_file(qr, mimetype="image/png", cache_timeout=0)


@app.route('/bot/logout')
def logout():
    name = request.values.get('name')
    if bots.master_bot.name == name:
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
    return jsonify(code=0, friends=bot.friends().stats_text(), mps=bot.mps().stats_text())


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


def get_session_id():
    sid = session.get('sid')
    if not sid:
        sid = uuid.uuid4()
        session['sid'] = sid
    return sid


@app.teardown_request
def shutdown_session(f=None):
    db_session.remove()


@app.route('/bot/article')
def web_page():
    uid = request.values.get('id')
    if uid:
        article = BotArticle.query.filter_by(uid=uid).first()
        if article:
            resp = requests.get(settings.QINIU_ROOT + article.key + ".gz")
            if resp.ok:
                content = zlib.decompress(resp.content).decode('utf-8')
                return render_template('article.html', title=article.title,
                                       author=article.sender, content=content)

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
    msgs = BotMessage.query.filter(BotMessage.bot_name == name) \
        .order_by(BotMessage.created_at.desc()).limit(200).all()
    return jsonify(code=0, messages=[{
        'sender': x.sender,
        'chat': x.chat,
        'type': x.type,
        'message': x.message,
        'created_at': x.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for x in msgs])


@app.route('/bot/articles')
def articles():
    name = request.values.get('name')
    msgs = BotArticle.query.filter(BotArticle.bot_name == name) \
        .order_by(BotArticle.created_at.desc()).limit(200).all()
    return jsonify(code=0, articles=[{
        'sender': x.sender,
        'title': x.title,
        'id': x.uid,
        'created_at': x.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for x in msgs])


@app.route('/bot/master/assign')
def set_master():
    name = request.values.get('name')
    bot = bots.running_bots.pop(name)

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


from raven.contrib.flask import Sentry

sentry = Sentry(app, dsn=settings.SENTRY_DSN)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'prod':
        app.run(host="0.0.0.0")
    else:
        app.run(debug=True)
