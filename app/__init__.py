# -*- coding: utf-8 -*-
__version__ = '0.1'

from flask import Flask
from flask import g
from flask import abort

import rethinkdb as r
from rethinkdb import (RqlRuntimeError, RqlDriverError, RqlError)

from AfricasTalkingGateway import (
    AfricasTalkingGateway, AfricasTalkingGatewayException)
from datetime import timedelta

import logging
import settings
import redis

app = Flask('app')
app.config.from_pyfile('settings.py', silent=True)


red = redis.StrictRedis(host='localhost', port=6379, db=0)
app.config['ONLINE_LAST_MINUTES'] = settings.ONLINE_LAST_MINUTES
app.secret_key = settings.SECRET_KEY

app.permanent_session_lifetime = timedelta(minutes=5760)
logging.basicConfig(filename='octopus.log', level=logging.DEBUG)


def db_setup():
    connection = r.connect(host=settings.RDB_HOST, port=settings.RDB_PORT,
                           auth_key=settings.rethinkdb_auth)
    try:
        r.db_create(settings.TARGET_DB).run(connection)
        r.db(settings.TARGET_DB).table_create('User').run(connection)
        logging.info('Database setup completed')
    except RqlError:
        logging.info('App database already exists')
    except RqlRuntimeError:
        logging.info('App database already exists')
    finally:
        connection.close()


@app.before_request
def before_request():
    try:
        logging.info('before_request')
        g.rdb_conn = r.connect(host=settings.RDB_HOST, port=settings.RDB_PORT,
                               db=settings.TARGET_DB, auth_key=settings.rethinkdb_auth)

    except RqlDriverError:
        logging.info('DB Connect Failed')
        abort(503, "No database connection could be established")


@app.teardown_request
def teardown_request(exception):
    try:
        logging.info('teardown_request')
        g.rdb_conn.close()
    except AttributeError:
        logging.info('Database failure - check your connection', exception)


from api import routes
from api import voice
