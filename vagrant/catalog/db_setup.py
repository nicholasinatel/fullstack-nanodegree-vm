# SQL Alchemy
# Configuration
# Class
# Table
# Mapper
# --------------------------------

# CONFIGURATION --------------------------------------------------------------------------------
# sys module provides functions and variables to manipulate python environment
import sys
# For Handling Unicode In SQL and Python
from sqlalchemy.types import TypeDecorator, Unicode
# For the Mapper code
from sqlalchemy import Column, ForeignKey, Integer, String, Float
# Declarative base for the configuration and class code
from sqlalchemy.ext.declarative import declarative_base
# Foreign Key for the Mapper
from sqlalchemy.orm import relationship
# Configuration for
from sqlalchemy import create_engine
# Setup when beginning the class
# Special Alchemy Classes - declarative_base to inherit
Base = declarative_base()
# CLASS ------------------------------------------------------
# TABLE -------
# MAPPER

class CoerceUTF8(TypeDecorator):
    """Safely coerce Python bytestrings to Unicode
    before passing off to the database."""

    impl = Unicode

    def process_bind_param(self, value, dialect):
        if isinstance(value, str):
            value = value.decode('utf-8')
        return value

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(CoerceUTF8, nullable=False)
    description = Column(CoerceUTF8)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    # This COlumn has strin with max 80 characters,
    # and nullable = false means not allowed to create withou name
    
    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'user_id': self.user_id
        }

class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(CoerceUTF8, nullable=False)
    active = Column(String(10))
    dy = Column(String(10))
    price = Column(String(10))
    description = Column(CoerceUTF8)
    category_id = Column(Integer, ForeignKey('category.id')) # Creates foreign key relationship between tables
    # takes the relationship to the class
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        # Returns object data in easily serializeable format
        return {
            'id': self.id,
            'name': self.name,
            'active': self.active,
            'dy': self.dy,
            'price': self.price,
            'description': self.description,
            'user_id': self.user_id
        }

class Rentability(Base):
    __tablename__ = 'rentability'
    id = Column(Integer, primary_key=True)
    month = Column(String(5), nullable=False)
    money = Column(Float)
    percent = Column(Float)
    item_id = Column(Integer, ForeignKey('item.id'))
    item = relationship(Item)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        # Returns object data in easily serializeable format
        return {
            'id': self.id,
            'month': self.month,
            'money': self.money,
            'percent': self.percent,
            'user_id': self.user_id
        }

# Create an instance of our create_engine class and point a DB to use
engine = create_engine('sqlite:///catalog.db')
# Goes to the DB and adds classes we will soon create
Base.metadata.create_all(engine)
