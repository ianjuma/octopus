from app import app
from flask import (abort, request, make_response)


@app.route('/api/ussd/callback/', methods=['POST'])
def ussd_callback():
    if request.method == 'POST':
        if request.headers['Content-Type'] != 'application/x-www-form-urlencoded':
            abort(400)

        # Reads the variables sent via POST from our gateway
        session_id = request.values.get("sessionId", None)
        service_code = request.values.get("serviceCode", None)
        phone_number = request.values.get("phoneNumber", None)
        text = request.values.get("text", None)

        menu_text = "END Africa's-Talking Show and Tell.\n"
        menu_text += "You're registered we'll call you and ask you a few questions."
        menu_text += "You stand a chance to win airtime"

        if request.values.get('text') is '':
            # load menu
            menu_text = "END Africa's-Talking Show and Tell.\n"
            menu_text += "You're registered we'll call you and ask you a few questions."
            menu_text += "You stand a chance to win airtime"

            resp = make_response(menu_text, 200)
            resp.headers['Content-Type'] = "text/plain"
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
    menu_text = """END Africa's-Talking Show and Tell Demo. \n
            1. You're  registered we'll call you and ask you a few questions\n
            2. You stand a chance to win airtime \n
            """
    return menu_text


def ussd_proceed(ussd_text):
    return "CON %s" % ussd_text


def ussd_stop(ussd_text):
    return "END %s" % ussd_text