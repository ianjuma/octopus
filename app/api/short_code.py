from app import (app, logging)
from flask import (abort, request, make_response, jsonify)
from app import settings


@app.route('/api/shortcode/callback/', methods=['POST'])
def short_code_callback():
    if request.method == 'POST':
        if request.headers['Content-Type'] != 'application/json':
            abort(400)

        # Reads the variables sent via POST from our gateway
        _from = request.values.get('from')
        to = request.values.get('to')
        text = request.values.get('text')
        date = request.values.get('date')

        print _from, to, text, date
    else:
        resp = make_response('Error', 400)
        resp.headers['Content-Type'] = 'text/plain'
        resp.cache_control.no_cache = True
        return resp