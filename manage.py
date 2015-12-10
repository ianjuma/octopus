import os
from gevent.pywsgi import WSGIServer
from gevent import monkey
monkey.patch_all()

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from app import app


def push_to_server():
    # just use git hooks already
    pass


def background_task(instance):
    # gunicorn -c config_gunicorn.py instance:app
    pass


def runserver(instance):
    port = int(os.environ.get("PORT", 8001))
    instance.config['DEBUG'] = True
    instance.config['use_reloader'] = True
    instance.config['threaded'] = True
    print 'Awesome running at - ' + str(port)

    http_server = WSGIServer(('0.0.0.0', port), instance)
    http_server.serve_forever()


if __name__ == '__main__':
    manager = Manager()
    manager.run(commands=None)
    # run(app)
