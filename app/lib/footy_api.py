import requests
import json

headers = {'X-Auth-Token': '3b7bd33d925842878308aa20f4422129', 'X-Response-Control': 'minified'}
base_url = 'http://api.football-data.org/v1/'


epl_team_id = {'arsenal': 57, 'man-u': 66, 'liverpool': 64, 'man-city': 65, 'leicester': 338, 'birmingham': 332,
               'southampton': 340, 'stoke': 70, 'everton': 62, 'west-brom': 74, 'watford': 346,
               'bournemouth': 405, 'tottenham': 73, 'swansea': 72, 'norwich': 68, 'fulham': 63, 'aston-villa': 58,
               'newcastle': 67, 'wigan': 75}


class Football():
    def __init__(self):
        pass

    @staticmethod
    def get_head_to_head(self, team_one, team_two):
        pass

    @staticmethod
    def get_next_match(team_name):
        team_id = epl_team_id.get(team_name.split()[0].lower())

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