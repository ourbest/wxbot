import os

from sqlalchemy import create_engine, Column, String, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from settings import logger

engine = create_engine(
    'sqlite:///data/bot.db',
    echo=True,
    convert_unicode=True,
    pool_recycle=120,
    pool_reset_on_return='commit')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    Base.metadata.create_all(bind=engine)


def commit():
    db_session().commit()


class BotArticle(Base):
    __tablename__ = 'bot_article'
    uid = Column(String(32), primary_key=True)
    bot_name = Column(String(80))
    sender = Column(String(80))
    title = Column(String(255))
    key = Column(String(255))
    cover = Column(String(255))
    created_at = Column(DateTime)
    status = Column(Integer)

    @property
    def content(self):
        path = 'data/content/%s/%s-%s.html' % (self.created_at.strftime('%y%m%d'), self.uid, self.title)
        content = ""
        if os.path.exists(path):
            with open(path, 'rt', encoding='utf-8') as fd:
                content = fd.read()
        # else:
        #     resp = requests.get(settings.QINIU_ROOT + self.key + ".gz")
        #     if resp.ok:
        #         content = zlib.decompress(resp.content).decode('utf-8')
        return content

    @content.setter
    def content(self, value):
        path = 'data/content/%s' % self.created_at.strftime('%y%m%d')
        os.makedirs(path, exist_ok=True)
        with open("%s/%s-%s.html" % (path, self.uid, self.title), "wt", encoding='utf-8') as fd:
            fd.write(value)


#
# class BotMessage(Base):
#     __tablename__ = 'bot_message'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     bot_name = Column(String(80))
#     sender = Column(String(80))
#     chat = Column(String(80))
#     type = Column(String(20))
#     message = Column(String(255))
#     url = Column(String(255))
#     created_at = Column(DateTime)
#

try:
    try:
        Base.metadata.create_all(engine)
    except:
        init_db()
        Base.metadata.create_all(engine)
except:
    logger.warning('error', exc_info=1)
