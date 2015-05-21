from app import (app, logging, settings)
from flask import (abort, request, make_response, jsonify)
from _utils import (FetchUrl, MakeRequests, WriteBulkSmsCsv)

from app import r
from app import g
from app import RqlError


@app.route('/api/bulksms', methods=['POST'])
def process_sms():
    """
    :return: res
    """
    if not request.json:
        abort(400)

    if request.headers['Content-Type'] != 'application/json':
        abort(400)

    metric = request.json.get('metric')
    granularity = request.json.get('granularity')
    start_date = request.json.get('startDate')
    end_date = request.json.get('endDate')
    username = request.json.get('username')
    apikey = settings.api_key
    _url = settings.bulk_sms_url

    # join to another table
    try:
        fetch = FetchUrl(
            _url, metric, username, apikey, granularity, start_date, end_date)
        url = fetch.form_url()
        # print url
        req = MakeRequests(url, apikey, method='GET')
        result = req.send_()
        if result.status_code == 400 or result.status_code == 500:
            resp = make_response(jsonify({'Error': 'Bad Request'}), 400)
            resp.headers['Content-Type'] = 'application/json'
            resp.cache_control.no_cache = True
            return resp
        else:
            _output = WriteBulkSmsCsv(result.text, username, metric=metric)
            _output.to_csv()
            resp = make_response(result.text, 200)
            resp.headers['Content-Type'] = 'application/json'

            resp.cache_control.no_cache = True
            return resp
    except Exception, e:
        logging.warning('Failed on /sms -> /bulkSMS')
        raise e


@app.route('/oauthCallBack/', methods=['POST'])
def get_tasks():
    if request.method is 'POST':
        if request.headers['Content-Type'] != 'text/plain':
            abort(400)

        text = request.data
        sender = request.args.get('from')

        try:
            tasks = r.table('Client').get(sender).update(text).run(g.rdb_conn)
        except RqlError:
            logging.warning('DB code verify failed on /api/getTasks/')

            resp = make_response(jsonify({"Error": "503 DB error"}), 503)
            resp.headers['Content-Type'] = "application/json"
            resp.cache_control.no_cache = True
            return resp

        resp = make_response(tasks, 200)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp


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