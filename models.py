from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

engine = create_engine('sqlite:///test.db')

Session = sessionmaker(bind=engine)

session = Session()


class Guest(Base):
    __tablename__ = 'guests'

    id = Column(Integer, primary_key=True)
    json_string = Column(Text())
    
    def __init__(self, json_string):
        self.json_string = json_string

    def __repr__(self):
        return '<User %r>' % self.json_string


