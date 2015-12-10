import os

# flask app
DEBUG = False
SECRET_KEY = "I\xf9\x9cF\x1e\x04\xe6\xfaF\x8f\xe6)-\xa432"
CSRF_ENABLED = True
CSRF_SESSION_LKEY = 'dev_key_h8asSNJ9s9=+'
THREADED = False
ONLINE_LAST_MINUTES = 720

# questions
questions = {1: 'What is the meaning of life?', 2: ''}

# redis
redis_broker = 'redis://localhost:6379/0'

# api key
api_key = '733ed38f63b039090a0001dbbc2dd416187f054d53650d0fd7c0b834a293a30d'
username = 'IanJuma'
from_ = '+254711082306'  # AT number

# Database
db_auth = "hackathon2015"
DB_HOST = os.environ.get('RDB_HOST') or '127.0.0.1'
DB_PORT = os.environ.get('RDB_PORT') or 3306
TARGET_DB = 'octopus'
