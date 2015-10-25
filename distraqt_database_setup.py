import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

# class Restaurant(Base):
#     __tablename__ = 'restaurant'

#     id = Column(Integer, primary_key=True)
#     name = Column(String(250), nullable=False)

#test class in DB for the distraqt app
class Category(Base):
	__tablename__ = 'category'

	id = Column(Integer, primary_key=True)
	block = Column(String(250), nullable=False)

	@property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }

class flowBlock(Base):
    __tablename__ = 'flow_block'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    # price = Column(String(8))
    # course = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            # 'price': self.price,
            # 'course': self.course,
        }


engine = create_engine('sqlite:///distraqt.db')

Base.metadata.create_all(engine)