import os

# flask app
DEBUG = False
SECRET_KEY = "I\xf9\x9cF\x1e\x04\xe6\xfaF\x8f\xe6)-\xa432"
CSRF_ENABLED = True
CSRF_SESSION_LKEY = 'dev_key_h8asSNJ9s9=+'
THREADED = False
ONLINE_LAST_MINUTES = 720

# urls
base_url = 'http://134.213.48.187:8080/'
bulk_sms_url = 'http://134.213.48.187:8080/bulkSms/sent?'
ussd_url = 'http://134.213.48.187:8080/ussd/hop/success?'

# redis
redis_broker = 'redis://localhost:6379/0'


# api key
api_key = '733ed38f63b039090a0001dbbc2dd416187f054d53650d0fd7c0b834a293a30d'
username = 'IanJuma'
from_ = '+254711082306'


# rethink
rethinkdb_auth = "hackathon2015"
RDB_HOST = os.environ.get('RDB_HOST') or '127.0.0.1'
RDB_PORT = os.environ.get('RDB_PORT') or 29019
TARGET_DB = 'octopus'
