#! /usr/bin/env python
# -*- coding: utf-8 -*-

from app import app, logging
from flask import (request, make_response)
from _utils import get_witty_intent


@app.route('/api/shortcode/callback/', methods=['POST'])
def short_code_callback():
    if request.method == 'POST':

        # Reads the variables sent via POST from our gateway
        _from = request.values.get('from', None)
        to = request.values.get('to', None)
        text = request.values.get('text', None)
        date = request.values.get('date', None)
        id_ = request.values.get('id', None)

        try:
            # persist session variable
            # pass to queue
            intent = get_witty_intent(text=text)
            print intent

        except Exception as e:
            logging.error('Failed with - ', e)

        print _from, to, text, date, id_

        resp = make_response('Ok', 200)
        resp.headers['Content-Type'] = 'text/plain'
        resp.cache_control.no_cache = True
        return resp
    else:
        resp = make_response('Error', 400)
        resp.headers['Content-Type'] = 'text/plain'
        resp.cache_control.no_cache = True
        return resp
