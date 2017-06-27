from datetime import datetime

from sqlalchemy import create_engine, Column, String, DateTime, func, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(
    'sqlite:///bot.db',
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


class BotMessage(Base):
    __tablename__ = 'bot_message'
    id = Column(Integer, primary_key=True, autoincrement=True)
    bot_name = Column(String(80))
    sender = Column(String(80))
    chat = Column(String(80))
    type = Column(String(20))
    message = Column(String(255))
    url = Column(String(255))
    created_at = Column(DateTime)


Base.metadata.create_all(engine)