from app import (app, logging)
from flask import (abort, request, make_response, jsonify)

from app import r
from app import g
from app import RqlError
from app import settings

from _utils import consume_call


@app.route('/api/ussd/callback/', methods=['POST'])
def ussd_callback():
    if request.method == 'POST':
        # if request.headers['Content-Type'] != 'text/plain':
        #    abort(400)
        print request.values
        # Reads the variables sent via POST from our gateway
        session_id = request.values.get("sessionId")
        service_code = request.values.get("serviceCode")
        phone_number = request.values.get("phoneNumber")
        text = request.values.get("text")
        print phone_number

        menu_text = """CON Africa's-Talking Show and Tell Demo \n
        - You're  registered we'll call you and ask you a few questions\n
        - You stand a chance to win airtime \n
        END
        """

        if request.values.get('text') is '':
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
            user = r.table('User').get(phone_number).run(g.rdb_conn)

            # no user found so save
            if user is not None:
                r.table('User').insert({'phoneNumber': phone_number, 'serviceCode': service_code,
                                        'sessionId': session_id, 'text': text}).run(g.rdb_conn)

                # make call
                consume_call(settings.from_, phone_number)

                resp = make_response(menu_text, 200)
                resp.headers['Content-Type'] = "text/plain"
                resp.cache_control.no_cache = True
                return resp
            else:
                # user found - can't play
                toast = """CON Africa's-Talking Show and Tell Demo \n
                - Sorry you can only play Once \n
                END
                """
                resp = make_response(toast, 200)
                resp.headers['Content-Type'] = "text/plain"
                resp.cache_control.no_cache = True
                return resp

        except RqlError:
            logging.warning('DB code verify failed on /api/ussd/ - > callback')

            resp = make_response(jsonify({"Error": "503 DB error"}), 503)
            resp.headers['Content-Type'] = "application/json"
            resp.cache_control.no_cache = True
            return resp

        resp = make_response(menu_text, 200)
        resp.headers['Content-Type'] = "text/plain"
        resp.cache_control.no_cache = True
        return resp
    else:
        resp = make_response('Error', 400)
        resp.headers['Content-Type'] = "text/plain"
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