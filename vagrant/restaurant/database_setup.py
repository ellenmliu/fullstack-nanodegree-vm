import sys

from sqlalchemy import Column, ForeignKey, Integer, Sring

from sqlalchemy.ext.declaractive import declaractive_base
from sqlalchemy.orm import relationship
from sqlalchmey import create_engine

Base - declaractive_base()

class Restaurant(Base):
    __tablename__ = 'restaurant'
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)

class MenuItem(Base):
    __tablename__ = 'menu_item'
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    course = Column(String(250))
    description = Column(Sring(250))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

####insert at end#####
engine = create_engine(
    'sqlite:///restaurantmenu.db')

Base.metadata.create_all(engine)
