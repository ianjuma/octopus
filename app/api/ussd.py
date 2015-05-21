from app import (app, logging, settings)
from flask import (abort, request, make_response, jsonify)

from app import r
from app import g
from app import RqlError


@app.route('/api/getUSSD/', methods=['POST'])
def ussd_callback():
    if request.method is 'POST':
        if request.headers['Content-Type'] != 'text/plain':
            abort(400)

        # Reads the variables sent via POST from our gateway
        session_id = request.args.get("sessionId")
        service_code = request.args.get("serviceCode")
        phone_number = request.args.get("phoneNumber")
        text = request.args.get("text")

        if request.args.get('text') is '':
            # load menu
            menu_text = """CON Africa's-Talking Show and Tell Demo \n
            - You're  registered we'll call you and ask you a few questions\n
            - You stand a chance to win airtime \n
            END
            """

            resp = make_response(menu_text, 200)
            resp.headers['Content-Type'] = "text/plain"
            resp.cache_control.no_cache = True
            return resp

        try:
            tasks = r.table('User').insert({'phoneNumber': phone_number, 'serviceCode': service_code,
                                            'sessionId': session_id, 'text': text}).run(g.rdb_conn)
            # push to queue
        except RqlError:
            logging.warning('DB code verify failed on /api/ussd/ - > callback')

            resp = make_response(jsonify({"Error": "503 DB error"}), 503)
            resp.headers['Content-Type'] = "application/json"
            resp.cache_control.no_cache = True
            return resp

        resp = make_response(tasks, 200)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp


def display_menu():
    menu_text = """CON Africa's-Talking Show and Tell Demo \n
            1. You're  registered we'll call you and ask you a few questions\n
            2. You stand a chance to win airtime \n
            END
            """
    return menu_text


def ussd_proceed(ussd_text):
    return "CON %s" % ussd_text


def ussd_stop(ussd_text):
    return "END %s" % ussd_text