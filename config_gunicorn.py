#!/usr/bin/env python

import os


def num_cpu():
    if not hasattr(os, 'sysconf'):
        raise RuntimeError('No sysconf detected.')
    return os.sysconf('SC_NPROCESSORS_ONLN')


bind = '127.0.0.1:8000'
workers = 4
worker_class = 'gevent'
debug = False
daemon = True
pidfile = '/tmp/gunicorn.pid'
logfile = '/tmp/gunicorn.log'
