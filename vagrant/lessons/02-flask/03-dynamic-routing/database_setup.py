# SQL Alchemy
# Configuration
# Class
# Table
# Mapper
# --------------------------------

# CONFIGURATION --------------------------------------------------------------------------------
# sys module provides functions and variables to manipulate python environment
import sys
# For the Mapper code
from sqlalchemy import Column, ForeignKey, Integer, String
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
class Restaurant(Base):
    __tablename__ = 'restaurant'
    name = Column(String(80), nullable=False)
    # This COlumn has strin with max 80 characters,
    # and nullable = false means not allowed to create withou name
    id = Column(Integer, primary_key=True)


class MenuItem(Base):
    __tablename__ = 'menu_item'
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    # Creates foreign key relationship between tables
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    # takes the relationship to the class Restaurant
    restaurant = relationship(Restaurant)

# Create an instance of our create_engine class and point a DB to use
engine = create_engine('sqlite:///restaurantmenu.db')
# Goes to the DB and adds classes we will soon create
Base.metadata.create_all(engine)

