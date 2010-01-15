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

    def req(self, params):
        """sync request and return object"""
        #random
        while(True):
            r = random.randint(0, 1000000)
            if (r != self.random):
                break
        #params
        p = {'api_id': self.api_id,
             'format': 'JSON',
             'timestamp': unixtime.timestamp(),
             'random': self.random,
             'v': api_version}
        p.update(params)
        p.update(sig=self._sig(p))
        data = urllib.urlencode(p)
        #request
        response = urllib.urlopen('http://api.vkontakte.ru/api.php', data)
        str = response.read()
        #json
        return json.loads(str)

    def _sig(self, params):
        m = hashlib.md5()
        list = params.items()
        list.sort()
        str = ["%s=%s" % (k, v) for k, v in list]
        m.update(''.join(str))
        m.update(self.api_secret)
        return m.hexdigest()
