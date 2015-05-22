#! /usr/bin/env python
# -*- coding: utf-8 -*-

from app import (app, logging)
from flask import (make_response, abort, request)

# globals
from app import r
from app import g
from app import settings
from app import RqlError

from app import AfricasTalkingGateway, AfricasTalkingGatewayException


@app.route('/api/voice/callback/', methods=['POST'])
def voice_callback():
    if request.method == 'POST':
        if request.headers['Content-Type'] != 'application/x-www-form-urlencoded':
            abort(400)

        is_active = request.values.get('isActive')
        session_id = request.values.get('sessionId')
        caller_number = request.values.get('callerNumber')

        print "is_active -> ", is_active
        print caller_number

        if is_active == str(0):
            # Compose the response

            duration = request.values.get('durationInSeconds')
            currency_code = request.values.get('currencyCode')
            amount = request.values.get('amount')

            try:
                r.table('User').get(caller_number).update({'duration': duration, 'currencyCode': currency_code,
                                                           'sessionId': session_id, 'amount': amount}).run(g.rdb_conn)
            except RqlError:
                logging.error('Save user call info failed on voice callback')

            resp = make_response('OK', 200)
            resp.headers['Content-Type'] = "application/xml"
            resp.cache_control.no_cache = True
            return resp

        if is_active == str(1):
            dtmf_digits = request.values.get('dtmfDigits')
            if dtmf_digits is not None:
                if dtmf_digits == str(5):
                    api = AfricasTalkingGateway(apiKey_=settings.api_key, username_=settings.username)
                    """
                    try:
                        api.sendAirtime([{'phoneNumber': caller_number, 'amount': 'KES 10'}])
                    except AfricasTalkingGatewayException:
                        logging.error('Sending airtime failed')
                    """


                    response = '<?xml version="1.0" encoding="UTF-8"?>'
                    response += '<Response>'
                    response += '<Say playBeep="false" >You are right, sending you airtime!</Say>'
                    response += '</Response>'

                    resp = make_response(response, 200)
                    resp.headers['Content-Type'] = "application/xml"
                    resp.cache_control.no_cache = True
                    return resp

                else:
                    response = '<?xml version="1.0" encoding="UTF-8"?>'
                    response += '<Response>'
                    response += '<Say playBeep="false" >You are wrong, sorry!</Say>'
                    response += '</Response>'

                    resp = make_response(response, 200)
                    resp.headers['Content-Type'] = "application/xml"
                    resp.cache_control.no_cache = True
                    return resp

            else:
                # Compose the response
                response = '<?xml version="1.0" encoding="UTF-8"?>'
                response += '<Response>'
                response += '<GetDigits timeout="20" finishOnKey="#">'
                response += '<Say playBeep="false" >How many people are in the room? end with hash sign</Say>'
                response += '</GetDigits>'
                response += '</Response>'

                resp = make_response(response, 200)
                resp.headers['Content-Type'] = "application/xml"
                resp.cache_control.no_cache = True
                return resp

    else:
        resp = make_response('Bad Request', 400)
        resp.headers['Content-Type'] = "application/xml"
        resp.cache_control.no_cache = True
        return resp