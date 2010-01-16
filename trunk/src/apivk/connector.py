import urllib, hashlib, random
import simplejson as json
#import json # python 2.6
from . import unixtime

api_version='2.0'

class Connector():
    def __init__(self, api_id, api_secret):
        self.api_id = api_id
        self.api_secret = api_secret
        self.random = 0

    def _random(self):
        while(True):
            r = random.randint(0, 1000000)
            if (r != self.random):
                break

    def _sig(self, params):
        m = hashlib.md5()
        list = params.items()
        list.sort()
        str = ["%s=%s" % (k, v) for k, v in list]
        m.update(''.join(str))
        m.update(self.api_secret)
        return m.hexdigest()

    def params(self, method_params):
        self._random()
        p = {'api_id': self.api_id,
             'format': 'JSON',
             'timestamp': unixtime.timestamp(),
             'random': self.random,
             'v': api_version}
        p.update(method_params)
        p.update(sig=self._sig(p))
        return p


def req(method_params, conn):
    """sync request and return object"""
    p = conn.params(method_params)
    data = urllib.urlencode(p)
    response = urllib.urlopen('http://api.vkontakte.ru/api.php', data)
    str = response.read()
    return json.loads(str)
