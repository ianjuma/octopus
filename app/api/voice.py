#! /usr/bin/env python
# -*- coding: utf-8 -*-

from app import (app, logging)
from app import AfricasTalkingGateway, AfricasTalkingGatewayException
from flask import (make_response, abort, request, jsonify)

# globals
from app import r
from app import g
from app import RqlError


@app.route('/api/voice/callback/', methods=['POST'])
def voice_callback():
    if request.method is 'POST':
        if request.headers['Content-Type'] != 'text/plain':
            abort(400)

        is_active = request.args.get('isActive')
        session_id = request.args.get('sessionId')
        caller_number = request.args.get('callerNumber')

        if is_active is 1:
            # Compose the response
            response = '<?xml version="1.0" encoding="UTF-8"?>'
            response += '<Response>'
            response += '<GetDigits timeout="20" finishOnKey="#">'
            response += '<Say>How many people are in the room? end with hash sign</Say>'
            response += '</GetDigits>'
            response += '<Say>We did not get your answer. Good bye</Say>'
            response += '</Response>'

            dtmf_digits = request.args.get('dtmfDigits')

            resp = make_response(response, 200)
            resp.headers['Content-Type'] = "application/xml"
            resp.cache_control.no_cache = True
            return resp

        else:
            duration = request.args.get('durationInSeconds')
            currency_code = request.args.get('currencyCode')
            amount = request.args.get('amount')

            try:
                r.table('User').get(caller_number).update({'duration': duration, 'currencyCode': currency_code,
                                                           'sessionId': session_id, 'amount': amount}).run(g.rdb_conn)
            except RqlError:
                logging.error('Save user call info failed on voice callback')