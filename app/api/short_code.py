#! /usr/bin/env python
# -*- coding: utf-8 -*-

from app import app, logging
from flask import (request, make_response)
from _utils import get_witty_intent

import requests
import json

headers = {'X-Auth-Token': '3b7bd33d925842878308aa20f4422129', 'X-Response-Control': 'minified'}
base_url = 'http://api.football-data.org/v1/'


epl_team_id = {'arsenal': 57, 'man-u': 66, 'liverpool': 64, 'man-city': 65, 'leicester': 338, 'birmingham': 332,
               'southampton': 340, 'stoke': 70, 'everton': 62, 'west-brom': 74, 'watford': 346,
               'bournemouth': 405, 'tottenham': 73, 'swansea': 72, 'norwich': 68, 'fulham': 63, 'aston-villa': 58,
               'newcastle': 67, 'wigan': 75}

from AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException

username = "IanJuma"
apikey   = "58fdfbbbcf36e06bbcce9ba869184ec705cf5b51f9a1b6babbf990ec50e4453f"
gateway = AfricasTalkingGateway(username, apikey)


def send_message(to, message):
    try:
        print "Sending message"
        results = gateway.sendMessage(to, message)
        for recipient in results:
            print 'number=%s;status=%s;messageId=%s;cost=%s' % (recipient['number'],
                                                                recipient['status'],
                                                                recipient['messageId'],
                                                                recipient['cost'])
    except AfricasTalkingGatewayException, e:
        print 'Encountered an error while sending: %s' % str(e)


class Football():
    def __init__(self):
        pass

    @staticmethod
    def get_head_to_head(self, team_one, team_two):
        pass

    @staticmethod
    def get_next_match(team_name="Arsenal"):
        team_id = epl_team_id.get(team_name.split()[0].lower())
        print "Getting team result"

        url = base_url + 'teams/%s/fixtures/' % team_id
        result = requests.get(url, headers=headers)

        response = json.loads(result.text)
        for match in response.get('fixtures'):
            if match.get('status') != 'FINISHED':
                playing_date = match.get('date')
                playing_date = playing_date.split('T')[0]

                fixture = "Next Match: %s are playing %s on %s" % (match.get('homeTeamName'),
                                                                     match.get('awayTeamName'), playing_date)

                return fixture

    def football_info(self):
        pass

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
            print json.get('outcomes')[0].get('intent')

            if json.get('outcomes')[0].get('intent') == 'next_match':
                # team_name = json.get('outcomes')[0]['entities']['team'][0]['value']
                result = Football.get_next_match(team_name='Arsenal')
                send_message(_from, result)

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
