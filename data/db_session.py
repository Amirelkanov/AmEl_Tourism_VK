#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlalchemy as sa
import sqlalchemy.ext.declarative as dec
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session, scoped_session

SqlAlchemyBase = dec.declarative_base()
__factory, __scoped_session = None, None


def global_init(db_url):
    global __factory, __scoped_session

    if __factory:
        return

    engine = sa.create_engine(db_url, echo=False)

    __factory = orm.sessionmaker(bind=engine)
    __scoped_session = scoped_session(__factory)

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __scoped_session
    return __scoped_session
