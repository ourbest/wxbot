import io
import tempfile

import atexit
import itchat
from itchat.components.login import push_login
from pyqrcode import QRCode
from wxpy import User, Chat, Bot, Messages
from wxpy.api.messages import Registered, MessageConfig
from wxpy.compatible import PY2
from wxpy.utils import enhance_webwx_request, wrap_user_name, enhance_connection

import crawler
from models import BotMessage, db_session


def bot_func(message):
    try:
        bot = message.bot
        session = db_session()
        msg = BotMessage(bot_name=bot.self.name, sender=message.member.name if message.member else message.sender.name,
                         chat=message.chat.name, type=message.type, message=message.text, url=message.url)
        session.add(msg)
        session.commit()
        print(message)

        articles = message.articles
        if articles:
            crawler.crawler(message)
        if message.chat in (bot.file_helper, bot.self):
            message.reply_msg("😊")
    finally:
        db_session.remove()


class AsyncBot(Bot):
    def __init__(self):
        self.core = itchat.Core()
        itchat.instanceList.append(self)

        enhance_connection(self.core.s)

        self.cache_path = None

        self.messages = Messages()
        self.registered = Registered(self)

        self.isLogging = True
        self.puid_map = None

        self.is_listening = False
        self.listening_thread = None
        if PY2:
            from wxpy.compatible.utils import TemporaryDirectory
            self.temp_dir = TemporaryDirectory(prefix='wxpy_')
        else:
            self.temp_dir = tempfile.TemporaryDirectory(prefix='wxpy_')

        atexit.register(self._cleanup)

    def get_qr(self):
        push_login(self.core)
        self.core.get_QRuuid()
        uuid = self.core.uuid
        qrStorage = io.BytesIO()
        qrCode = QRCode('https://login.weixin.qq.com/l/' + uuid)
        qrCode.png(qrStorage, scale=10)
        return qrStorage

    def check_login(self):
        return self.core.check_login()

    def post_login(self, logout_callback=None):
        self.core.web_init()
        self.core.show_mobile_login()
        self.core.get_contact(True)
        self.core.start_receiving(logout_callback)
        self.isLogging = False

        enhance_webwx_request(self)

        self.self = User(self.core.loginInfo['User'], self)
        self.file_helper = Chat(wrap_user_name('filehelper'), self)

        self.start()
        self.register_func()
        self.file_helper.send('机器人上线了')

    def register_func(self):
        self.registered.append(MessageConfig(self, bot_func, chats=None, msg_types=None,
                                             except_self=False, run_async=True, enabled=True))
