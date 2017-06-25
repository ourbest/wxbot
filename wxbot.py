import uuid
from collections import defaultdict

import requests
import zlib

import sys
from flask import Flask, session, render_template, jsonify, send_file, request

import uploader
from bots import AsyncBot
from models import db_session, BotArticle, BotMessage

app = Flask(__name__)

bots = dict()

anonymous_bots = defaultdict(AsyncBot)

app.secret_key = 'A0Zr98jdai12oqwjo/3yX R~XHH!jmN]LWX/,?RT'


@app.route('/')
def index():
    return render_template("index.html", version='e5d8236bbffa72544c41')


@app.route('/dist/<file>')
def dist(file):
    return send_file('static/dist/' + file)


@app.route('/bot/bots')
def get_bots():
    return jsonify(bots=list(bots.keys()))


@app.route('/bot/qr')
def get_qr():
    bot = anonymous_bots[get_session_id()]

    qr = bot.get_qr()
    qr.seek(0)
    return send_file(qr, mimetype="image/png", cache_timeout=0)


@app.route('/bot/logout')
def logout():
    name = request.values.get('name')
    bot = bots.get(name)
    if not bot:
        return jsonify(code=1, message="没有这个机器人")
    bot.logout()
    del bots[name]
    return jsonify(code=0)


@app.route('/bot/info')
def get_bot_info():
    name = request.values.get('name')
    bot = bots.get(name)
    if not bot:
        return jsonify(code=1, message="没有这个机器人")
    return jsonify(code=0, friends=bot.friends().stats_text(), mps=bot.mps().stats_text())


@app.route('/bot/qr/status')
def get_qr_status():
    bot = anonymous_bots.get(get_session_id())
    status = bot.check_login()
    message = ""
    name = ""
    if status == '200':
        message = '登录成功'
        bot.post_login()
        if bot.self.name in bots:
            bots[bot.self.name].logout()

        del anonymous_bots[get_session_id()]
        bots[bot.self.name] = bot
        name = bot.self.name
    elif status == '201':
        message = '客户端确认'
    elif status == '408':
        message = 'QR过期'

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
            resp = requests.get(uploader.qiniu_root + article.key + ".gz")
            if resp.ok:
                content = zlib.decompress(resp.content).decode('utf-8')
                return render_template('article.html', title=article.title,
                                       author=article.sender, content=content)

    return '404', 404


@app.route('/bot/friends')
def friends():
    name = request.values.get('name')
    bot = bots.get(name)
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
    bot = bots.get(name)
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
    bot = bots.get(name)
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


if __name__ == '__main__':
    if sys.argv and sys.argv[0] == 'prod':
        app.run(host="0.0.0.0")
    else:
        app.run(debug=True)
