# для настройки баз данных
import json
import os

from sqlalchemy import Column, ForeignKey, Integer, String, Text, Date

# для определения таблицы и модели
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta

# для создания отношений между таблицами
from sqlalchemy.orm import relationship, session

# для настроек
from sqlalchemy import create_engine
from datetime import datetime

# создание экземпляра declarative_base
Base = declarative_base()


# здесь создаем наши модели
class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    text = Column(Text, nullable=False)
    date = Column(Date, default=datetime.utcnow)


basedir = os.path.abspath(os.path.dirname(__file__))
path_db = 'sqlite:///' + os.path.join(basedir, 'database.db?check_same_thread=False')

engine = create_engine(path_db)
Base.metadata.create_all(engine)
