import requests
import json
import pprint

headers = {'X-Auth-Token': '3b7bd33d925842878308aa20f4422129', 'X-Response-Control': 'minified'}
result = requests.get('http://api.football-data.org/v1/teams/86/fixtures', headers=headers)

response = json.loads(result.text)

pp = pprint.PrettyPrinter(indent=2)
pp.pprint(response)