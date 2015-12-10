import os
from gevent.pywsgi import WSGIServer
from gevent import monkey
monkey.patch_all()

from app import app

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8001))
    app.config['DEBUG'] = True
    app.config['use_reloader'] = True
    app.config['threaded'] = True

    http_server = WSGIServer(('127.0.0.1', port), app)
    http_server.serve_forever()
    # app.run(port=port, host='0.0.0.0')
    # this can be omitted if using gevent wrapped around gunicorn
