import sys
sys.path.append('../src')

from apivk import *
import apivk_secure as secure

import time
from threading import Thread

api_id = '1788474'
api_secret = 'apisecuresecret'
uid = '1857932'

q = VKQueue(api_id, api_secret, 3, 3)

def sync(label, params):
    print 'sync req', label
    event = q.add(params)
    try:
        res = event.wait()
        print 'sync req', label, '=', res
    except VKError, e:
        print 'sync req', label, ' ERROR ', e.code, ',', e.msg

def on_success(obj):
    print 'on_success ', obj
def on_error(error_code, error_msg, request_params):
    print 'error  ', error_code, ': ', error_msg

def async(label, params):
        print 'async req', label
        q.add(params, on_success, on_error)

def params_vkerror():
    return {'method':'secure.notExistedMethod'}
def params(status):
    return secure.saveAppStatus(uid, status)

sync('sync1', params('1'))
sync('sync1', params('1'))
sync('sync2', params('2'))
sync('sync3-error', params_vkerror())
sync('sync4', params('4'))

count = 5
async('Async1', params('async1'))
Thread(target=sync, args=('sync1', params('1'))).start()
Thread(target=sync, args=('sync2', params('2'))).start()
Thread(target=sync, args=('sync3-error', params_vkerror())).start()
Thread(target=sync, args=('sync4', params('4'))).start()
async('Async2', params('async2'))

time.sleep(5)

for x in xrange(50):
    Thread(target=sync, args=('SYNC %s'%x, params(x))).start()
    async('ASYNC%s'%x, params('ASYNC%s'%x))

