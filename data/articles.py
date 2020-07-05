#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Initializing columns for tables: Articles, Categories """

import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase

association_table = sqlalchemy.Table("association", SqlAlchemyBase.metadata,
                                     sqlalchemy.Column("articles",
                                                       sqlalchemy.Integer,
                                                       sqlalchemy.ForeignKey(
                                                           "articles.id")),
                                     sqlalchemy.Column("categories",
                                                       sqlalchemy.Integer,
                                                       sqlalchemy.ForeignKey(
                                                           "categories.id"))
                                     )


class Article(SqlAlchemyBase):
    """ Article model initialization class """

    __tablename__ = "articles"
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    coords = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    thumbnail_img = sqlalchemy.Column(sqlalchemy.String)
    article_imgs = sqlalchemy.Column(sqlalchemy.String)
    text = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    article_category_id = sqlalchemy.Column(sqlalchemy.Integer,
                                            sqlalchemy.ForeignKey(
                                                "categories.id"))
    category = orm.relation("Category",
                            secondary="association",
                            backref="articles")


class Category(SqlAlchemyBase):
    """ Category model initialization class """

    __tablename__ = "categories"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    name_of_category = sqlalchemy.Column(sqlalchemy.String, nullable=False)
