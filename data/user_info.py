#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlalchemy

from .db_session import SqlAlchemyBase


class VKUserInfo(SqlAlchemyBase):
    """ VK User info model initialization class """

    __tablename__ = 'vk_user_info'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    coords = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    page = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=1)
