import apivk.secure as secure
import time
from threading import Thread
from apivk.vkqueue import VKQueue, VKError, VKQueueTimeout

api_id = '1788474'
api_secret = 'apisecuresecret'
uid = '1857932'

q = VKQueue(api_id, api_secret, 2)

def sync(label, count):
    for x in xrange(count):
        status = label + ' ' + str(x)
        print status
        res = q.sync(secure.saveAppStatus(uid, status))
        print status, res

def on_success(obj):
    print 'on_success ', obj
def on_error(error_code, error_msg, request_params):
    print 'error  ', error_code, ': ', error_msg

def async(label, count):
    for x in xrange(count):
        status = label + ' ' + str(x)
        print status
        q.async(secure.saveAppStatus(uid, status), on_success, on_error)

def sync_vkerror():
    print 'sync_vkerror'
    try:
        res = q.sync({'method':'secure.notExistedMethod'})
        print 'res:', res
    except VKError as e:
        print 'e=',e

def sync_timeout():
    time.sleep(1)
    try:
        res = q.sync(secure.saveAppStatus(uid, 'TIMEOUT'), 0.1)
        print 'res:', res
    except VKQueueTimeout as e:
        print 'e=',e


count = 5
Thread(target=async, args=('Async1', count)).start()
Thread(target=sync, args=('sync1', count)).start()
Thread(target=sync, args=('sync2', count)).start()
Thread(target=sync, args=('sync3', count)).start()
Thread(target=sync, args=('sync4', count)).start()
Thread(target=sync, args=('sync5', count)).start()
Thread(target=async, args=('Async2', count)).start()

Thread(target=sync_vkerror).start()
Thread(target=sync_timeout).start()
