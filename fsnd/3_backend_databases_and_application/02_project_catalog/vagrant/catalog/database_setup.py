"""
    File name: database_setup.py
    Author: Christian Eik
    Date created: 2018-06-10
    Date last modified: 2018-06-15
    Python Version: 2.7

    Create the database and tables for the catalog project.
"""

import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()


class Users(Base):
    """
    users table with the following columns:

        id = Column(Integer, primary_key=True)
        name = Column(String(250), nullable=False)
        email = Column(String(250), nullable=False)
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
        }


class Categories(Base):
    """
    categories table with the following columns:

        id = Column(Integer, primary_key=True)
        name = Column(String(250), nullable=False)
        parent_id = Column(Integer, ForeignKey('categories.id'))
    """

    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    parent_id = Column(Integer, ForeignKey('categories.id'))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
        }


class Products(Base):
    """
    products table with the following columns:

        id = Column(Integer, primary_key=True)
        name = Column(String(250), nullable=False)
        description = Column(String(500))
        price_cents = Column(Integer, nullable=False)
        created_at = Column(DateTime, default=datetime.datetime.utcnow)
        created_by = Column(Integer, ForeignKey('users.id'))

    created_by establishes a relationship to the users table.
    """

    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(500))
    price_cents = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_by = Column(Integer, ForeignKey('users.id'))
    creator = relationship(Users)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price_cents': self.price_cents,
            'created_at': self.created_at,
            'created_by': self.created_by,
            'creator_name': self.creator.name,
            'creator_email': self.creator.email,
        }


class ProductsCategories(Base):
    """
    products table with the following columns:

        id = Column(Integer, primary_key=True)
        product_id = Column(Integer, ForeignKey('products.id'))
        category_id = Column(Integer, ForeignKey('categories.id'))

    product_id and category_id establish a relationship to the products and
    categories table respectively.

    This table provides a many-to-many relationship between products and
    categories.
    """

    __tablename__ = 'products_categories'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship(Products)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship(Categories)
    created_by = Column(Integer, ForeignKey('users.id'))
    creator = relationship(Users)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'product_id': self.product_id,
            'product_name': self.product.name,
            'category_id': self.category_id,
            'category_name': self.category.name,
            'created_by': self.created_by,
            'creator_name': self.creator.name,
            'creator_email': self.creator.email,
        }


engine = create_engine('sqlite:///catalog_project.db')

Base.metadata.create_all(engine)

print("database successfully created")
