__author__ = 'at'

from urllib import urlencode
from json import loads
import csv
import requests


class NotFoundException(BaseException):
    pass


class GatewayTimedOut(BaseException):
    pass


class WriteBulkSmsCsv():
    def __init__(self, json, username, metric='cost'):
        """
        :param json
        :param username
        :param metric - cost, count
        :return: csv
        """
        self.json = json
        self.username = username
        self.metric = metric

    def to_csv(self):
        file_name = 'exports/' + self.username + 'bulkSMS' + '.csv'
        fd = open(file_name, "wb")
        try:
            writer = csv.writer(fd)
            if self.metric == 'cost':
                json = loads(self.json)
                result = json.get('responses')

                writer.writerow(('# No', 'Date', 'Count'))
                for index in xrange(len(result.get('networkCostStats'))):
                    date = result.get('networkCostStats')[index].get('date')
                    count = result.get('networkCostStats')[index].get('elements').get('Safaricom (Kenya)')
                    writer.writerow((index, date, count))

            elif self.metric == 'count':
                json = loads(self.json)
                result = json.get('responses')

                # TODO: sender id stats, missing stats - pandas
                for index in xrange(len(result.get('networkCountStats'))):
                    date = result.get('networkCountStats')[index].get('date')
                    telecoms = result.get('networkCountStats')[index].get('elements')
                    count = 0
                    for t, statCount in telecoms.iteritems():
                        count += int(statCount)

                    writer.writerow(('# No', 'Date', 'Count'))
                    writer.writerow((index, date, count))

        except NotFoundException, e:
            raise e
        finally:
            fd.close()


class FetchUrl(object):
    """
    Form urls, parse and
    """
    def __init__(self, base_url, metric, username, apikey, granularity, start_date, end_date):
        """
        :param base_url:
        :param metric:
        :param username:
        :param apikey:
        :param granularity:
        :param start_date:
        :param end_date:
        :return: url object
        """
        self.base_url = base_url
        self.metric = metric
        self.username = username
        self.apikey = apikey
        self.granularity = granularity
        self.start_date = start_date
        self.end_date = end_date

    def form_url(self):
        query_args = {'granularity': self.granularity, 'startDate': self.start_date,
                      'endDate': self.end_date, 'metric': self.metric, 'username': self.username}
        _url = urlencode(query_args)
        return self.base_url + _url

    def get_apikey(self):
        return self.apikey


class MakeRequests(object):
    """
    Some request helper classes
    """
    def __init__(self, url, apikey, method='GET'):
        """
        :param url:
        :param apikey:
        :param method:
        :return: None
        """
        self.method = method
        self.url = url
        self.apikey = apikey

    def send_(self):
        """
        :param self
        :return: response object
        """
        if self.method is 'GET':
            headers = {'apikey': self.apikey}
            r = requests.get(self.url, headers=headers)
            return r


def make_call():
    pass


def send_text():
    pass