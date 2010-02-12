import apivk_secure as secure
from apivk import *

def on_success(obj):
    print 'on_success ', obj

def on_error(error_code, error_msg, request_params):
    print 'error  ', error_code, ': ', error_msg

q = VKQueue('1', 'apisecuresecret', 5, 1)
#async request
q.add(secure.saveAppStatus(uid='1', status='Hi, Pavel!'), on_success, on_error)

#sync request
event = q.add(secure.saveAppStatus(uid='1', status='Hello world!'))
try:
    response = event.wait()
    print 'response:', response
except VKError, e:
    print 'VKError %s: %s'%(e.code, e.msg)
