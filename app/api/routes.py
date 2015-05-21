#! /usr/bin/env python
# -*- coding: utf-8 -*-

from app import (app, logging)
from flask import (render_template, make_response)


@app.route('/', methods=['GET'])
def index():
    """
    render index page
    :return: index template
    """
    # join to another table
    try:
        resp = make_response(render_template('index.html'))
        resp.cache_control.no_cache = True
        return resp
    except Exception, e:
        logging.warning('Failed on -> /')
        raise e