#! /usr/bin/env python
# -*- coding: utf-8 -*-

from app import (app, logging)
from flask import (make_response, request)

# globals
from app import settings

from app import AfricasTalkingGateway, AfricasTalkingGatewayException

username = "IanJuma"
apikey = "19d19757b8fa132c676109af3f79c246bffcb0835098d3eef5ce42dd84eb966a"
gateway = AfricasTalkingGateway(username, apikey)


@app.route('/api/voice/callback/', methods=['POST'])
def voice_callback():
    if request.method == 'POST':
        is_active = request.values.get('isActive', None)
        session_id = request.values.get('sessionId', None)
        caller_number = request.values.get('callerNumber', None)
        direction = request.values.get('direction', None)

        try:
            # store session info
            pass
        except Exception as e:
            logging.error('Storing fail -> ', e)

        print "is_active -> ", is_active
        print caller_number, session_id

        if direction == "inbound":
            response = '<?xml version="1.0" encoding="UTF-8"?>'
            response += '<Response>'
            response += '<Say maxDuration="5" playBeep="false"> I am Lucy, vote for me! </Say>'
            response += '</Response>'

            resp = make_response(response, 200)
            resp.headers['Content-Type'] = "application/xml"
            resp.cache_control.no_cache = True
            return resp

        if is_active == str(0):
            # Compose the response
            duration = request.values.get('durationInSeconds', None)
            currency_code = request.values.get('currencyCode', None)
            amount = request.values.get('amount', None)
            # update session info to Redis

            print duration, currency_code, amount

            response = '<?xml version="1.0" encoding="UTF-8"?>'
            response += '<Response>'
            response += '<Say playBeep="false" >You are right, sending you airtime!</Say>'
            response += '</Response>'

            resp = make_response(response, 200)
            resp.headers['Content-Type'] = "application/xml"
            resp.cache_control.no_cache = True
            return resp

        if is_active == str(1):
            dtmf_digits = request.values.get('dtmfDigits', None)
            if dtmf_digits is not None:
                if dtmf_digits == str(6):
                    api = AfricasTalkingGateway(
                        apiKey_=settings.api_key, username_=settings.username)
                    try:
                        api.sendAirtime([{'phoneNumber':
                                        caller_number, 'amount': 'KES 10'}])
                    except AfricasTalkingGatewayException:
                        logging.error('Sending airtime failed')

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
                response += '<Say playBeep="false" >How old is Africa\'s Talking? end with hash sign</Say>'
                response += '</GetDigits>'
                response += '</Response>'

                results = gateway.call("+254711082306", "+254721339381")

                for result in results:
                    print "Status : %s; phoneNumber : %s " % (result['status'],
                                                              result['phoneNumber'])

                resp = make_response(response, 200)
                resp.headers['Content-Type'] = "application/xml"
                resp.cache_control.no_cache = True
                return resp

    else:
        resp = make_response('Bad Request', 400)
        resp.headers['Content-Type'] = "application/xml"
        resp.cache_control.no_cache = True
        return resp
