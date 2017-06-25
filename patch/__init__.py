import io
import logging
import os

import time

from itchat import utils, config
from itchat.components.login import push_login
from itchat.utils import test_connect

logger = logging.getLogger('itchat')


def itchat():
    pass


def auto_login(self, hotReload=False, statusStorageDir='itchat.pkl',
               enableCmdQR=False, picDir=None, qrCallback=None,
               loginCallback=None, exitCallback=None):
    if not test_connect():
        logger.info("You can't get access to internet or wechat domain, so exit.")
        return

    self.useHotReload = hotReload
    if hotReload:
        if self.load_login_status(statusStorageDir,
                                  loginCallback=loginCallback, exitCallback=exitCallback):
            return
        self.login(enableCmdQR=enableCmdQR, picDir=picDir, qrCallback=qrCallback,
                   loginCallback=loginCallback, exitCallback=exitCallback)
        self.dump_login_status(statusStorageDir)
        self.hotReloadDir = statusStorageDir
    else:
        self.login(enableCmdQR=enableCmdQR, picDir=picDir, qrCallback=qrCallback,
                   loginCallback=loginCallback, exitCallback=exitCallback)


def login_success(self, picDir=None, loginCallback=None, exitCallback=None):
    logger.info('Loading the contact, this may take a little while.')
    self.web_init()
    self.show_mobile_login()
    self.get_contact(True)
    if hasattr(loginCallback, '__call__'):
        r = loginCallback()
    else:
        utils.clear_screen()
        if os.path.exists(picDir or config.DEFAULT_QR):
            os.remove(picDir or config.DEFAULT_QR)
        logger.info('Login successfully as %s' % self.storageClass.nickName)
    self.start_receiving(exitCallback)
    self.isLogging = False


def login(self, enableCmdQR=False, picDir=None, qrCallback=None,
          loginCallback=None, exitCallback=None):
    if self.alive or self.isLogging:
        logger.warning('itchat has already logged in.')
        return
    self.isLogging = True
    while self.isLogging:
        uuid = push_login(self)
        if uuid:
            qrStorage = io.BytesIO()
        else:
            logger.info('Getting uuid of QR code.')
            while not self.get_QRuuid():
                time.sleep(1)
            logger.info('Downloading QR code.')
            qrStorage = self.get_QR(enableCmdQR=enableCmdQR,
                                    picDir=picDir, qrCallback=qrCallback)
            logger.info('Please scan the QR code to log in.')
        isLoggedIn = False
        while not isLoggedIn:
            status = self.check_login()
            if hasattr(qrCallback, '__call__'):
                qrCallback(uuid=self.uuid, status=status, qrcode=qrStorage.getvalue())
            if status == '200':
                isLoggedIn = True
            elif status == '201':
                if isLoggedIn is not None:
                    logger.info('Please press confirm on your phone.')
                    isLoggedIn = None
            elif status != '408':
                break
        if isLoggedIn:
            break
        logger.info('Log in time out, reloading QR code.')
    else:
        return  # log in process is stopped by user
