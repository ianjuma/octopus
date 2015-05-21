#! /usr/bin/env python
# -*- coding: utf-8 -*-

from app import (app, logging, settings)
from flask import (make_response, abort, request)
from json import dumps
from _utils import (FetchUrl, MakeRequests)


@app.route('/api/ussd', methods=['POST'])
def receiveUSSD():
    """
    :param USSD object
    :return: get menu and all - USSD
    """
    if request.method != 'POST':
        abort(400)

    if not request.json:
        abort(400)

    metric = request.json.get('metric')
    granularity = request.json.get('granularity')
    start_date = request.json.get('startDate')
    end_date = request.json.get('endDate')
    username = request.json.get('username')
    apikey = settings.api_key
    _url = settings.ussd_url

    try:
        fetch = FetchUrl(_url, metric, username, apikey, granularity, start_date, end_date)
        url = fetch.form_url()
        print url
        req = MakeRequests(url, apikey, method='GET')
        result = req.send_()
        print result.text
        resp = make_response(result.text, 200)
        resp.headers['Content-Type'] = 'application/json'

        resp.cache_control.no_cache = True
        return resp
    except Exception, e:
        logging.warning('Failed on ussd -> /ussd')
        raise e


@app.route('/api/voice', methods=['POST'])
def get_shortcode():
    if not request.json:
        abort(400)

    if request.headers['Content-Type'] != 'application/json':
        abort(400)

    task_data = []
    task_data = dumps(task_data)

    resp = make_response(task_data, 200)
    resp.headers['Content-Type'] = 'application/json'
    resp.cache_control.no_cache = True
    return resp
