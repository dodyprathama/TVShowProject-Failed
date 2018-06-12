from sqlalchemy.orm import relationship, backref, joinedload
from sqlalchemy import Column, DateTime, String, Integer, Float, ForeignKey, func, UniqueConstraint

from pprint import pprint

from db.base import Base, inverse_relationship, create_tables 

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)

    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class TVShow(Base):
    __tablename__ = 'tvshow'
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)
    api_id = Column(Integer)

    name = Column(String)
    image = Column(String)

    def parse_json(self, data):
        try:
            self.api_id = data['id']
        except:
            self.api_id = ''
        try:
            self.name = data['name']
        except:
            self.name = ''
        try:
            self.url = data['_links']['self']['href']
        except:
            self.url = None
        try:
            self.image = data['image']['medium']
        except:
            self.image = 'http://via.placeholder.com/210x295'

class Like(Base):
    __tablename__ = 'like'
    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref=inverse_relationship('likes'))

    tvshow_id = Column(Integer, ForeignKey('tvshow.id'))
    tvshow = relationship(TVShow, backref=inverse_relationship('like_by'))
