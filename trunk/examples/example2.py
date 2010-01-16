import apivk.secure as secure
from apivk.vkqueue import VKQueue

def on_success(obj):
    print 'on_success ', obj

def on_error(error_code, error_msg, request_params):
    print 'error  ', error_code, ': ', error_msg

api_id = '1788474'
api_secret = 'apisecuresecret'
uid = '1857932'

q = VKQueue(api_id, api_secret, 5)

for x in xrange(100):
    print x
    q.put(secure.saveAppStatus(uid, x), on_success, on_error)

