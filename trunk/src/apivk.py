__all__=["VKQueue", "VKError", "VKAuth"]

#####################
### common imports
import urllib2, threading, hashlib, re

#######################
### sync vk unixtime
import time
def vktime():
    md5 = hashlib.md5()
    api_id='1788474'
    secret='secret'
    md5.update('api_id=%s'%api_id)
    md5.update('format=JSON')
    md5.update('method=getServerTime')
    md5.update('v=2.0')
    md5.update(secret)
    url="http://api.vkontakte.ru/api.php?api_id=%s&format=JSON&method=getServerTime&v=2.0&sig=%s" %(api_id, md5.hexdigest()) 
    r = urllib2.urlopen(url).read()
    m = re.match('\{"response":([0-9]+)\}', r)
    if (m):
        return int(m.group(1))
    else:
        return int(time.time())

DELTA_UNIXTIME = vktime() - int(time.time())
def timestamp():
    return int(time.time())+DELTA_UNIXTIME
###########
### VKAuth
class VKAuth:
    def __init__(self, api_id, api_secret):
        self.api_id = api_id
        self.api_secret = api_secret

    def check(self, id, auth_key):
        m = hashlib.md5()
        m.update(self.api_id)
        m.update('_')
        m.update(id)
        m.update('_')
        m.update(self.api_secret)
        return m.hexdigest()==auth_key

############
### vkqueue
PRIORITY_QUEUE=True
try:
    from Queue import PriorityQueue as Q # only in python 2.6
except ImportError:
    from Queue import Queue as Q
    PRIORITY_QUEUE=False

class VKQueue():
    def __init__(self,
                 api_id,
                 api_secret,
                 req_per_second = 5,
                 threads_count = 5,
                 max_queue_size = 1000):
        self.q = Q(max_queue_size)
        req = VKReq(api_id, api_secret)
        req_interval = float(threads_count)/req_per_second
        for x in xrange(threads_count):
            t = VKThread(self.q, req, req_interval)
            t.start()

    def add(self, params, fok = None, ferror = None, prior = 0):
        """add request in queue

        fok(obj) - call on success response

        ferror(error_code, error_message, request_params) - call on
        error in response

        request_params = [{"key": "xxx", "value": "yyy"}, ...]

        return VKEvent
        """
        event = VKEvent(fok, ferror)
        if PRIORITY_QUEUE:
            self.q.put((prior, (params, event)), False)
        else:
            self.q.put((params, event), False)
        return event

##############
### VKEvent
class VKEvent():
    def __init__(self, fok, ferror):
        self.event=threading.Event()
        self.fok = fok
        self.ferror = ferror
        self.e = False
    def ok(self, data):
        self.data = data
        if (self.fok):
            self.fok(data)
        self.event.set()
    def error(self, exception):
        self.e = exception
        if self.ferror:
            self.ferror(self.e.code, self.e.msg, self.e.rp)
        self.event.set()
    def fatal(self, exception):
        self.e = exception
        self.event.set()
    def wait(self):
        self.event.wait()
        if self.e:
            raise self.e
        else:
            return self.data

#################
### Exceptions
class VKError(Exception):
    def __init__(self, code, msg, rp):
        self.code = code
        self.msg = msg
        self.rp = rp
    def __str__(self):
        return 'VKError %s "%s"'%(self.code, self.msg)

#############
### Parser
try:
    import simplejson as json
except ImportError:
    import json # only in python 2.6

def vkparse(data):
    """ parse raw data from vk

    return object on raise VKError"""
    r = json.loads(data)
    if r.has_key('response'):
        return r['response']
    else:
        r = r['error']
        error_code = int(r['error_code'])
        raise VKError(error_code, r['error_msg'], r['request_params'])

###############
### VKThread
DEFAULT_THREAD_SLEEP=0.1
class VKThread(threading.Thread):
    def __init__(self, queue, vkreq, req_interval):
        threading.Thread.__init__(self)
        self.q = queue
        self.req = vkreq
        self.req_interval = req_interval

    def run(self):
        q=self.q
        req=self.req
        while True:
            item = q.get()
            if PRIORITY_QUEUE:
                (prior, (params, event)) = item
            else:
                (params, event) = item
            sleep = self.req_interval
            while True:
                t = time.time()
                try:
                    resp = urllib2.urlopen(req.get(params)).read()
                    data = vkparse(resp)
                except VKError, e:
                    if (e.code == 6):
                        time.sleep(sleep)
                        sleep += 0.5*self.req_interval
                        continue
                    else:
                        event.error(e)
                        break
                except Exception, e:
                    event.fatal(e)
                    break
                else:
                    event.ok(data)
                    break
                finally:
                    t = self.req_interval + t - time.time()
                    if t>0 :
                        time.sleep(t)
                    else:
                        time.sleep(DEFAULT_THREAD_SLEEP)

############
### VKReq
import urllib, random
API_VERSION='2.0'
class VKReq():
    def __init__(self, api_id, api_secret):
        self.api_id = api_id
        self.api_secret = api_secret
        self.random = 0

    def _update_random(self):
        while(True):
            r = random.randint(0, 1000000)
            if (r != self.random):
                self.random = r
                break

    def _sig(self, params):
        m = hashlib.md5()
        list = params.items()
        list.sort()
        str = ["%s=%s" % (k, v) for k, v in list]
        m.update(''.join(str))
        m.update(self.api_secret)
        return m.hexdigest()

    def _params(self, method_params):
        self._update_random()
        p = {'api_id': self.api_id,
             'format': 'JSON',
             'timestamp': timestamp(),
             'random': self.random,
             'v': API_VERSION}
        p.update(method_params)
        p.update(sig=self._sig(p))
        return p

    def get(self, method_params):
        """return urllib2.Request"""
        p = self._params(method_params)
        data = urllib.urlencode(p)
        return urllib2.Request('http://api.vkontakte.ru/api.php', data)

