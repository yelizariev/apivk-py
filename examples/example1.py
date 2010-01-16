import apivk.secure as secure
from apivk.vkqueue import VKQueue

q = VKQueue(api_id='1', api_secret='apisecuresecret', req_per_second = 5)
q.put(secure.saveAppStatus(uid='1', status='Hi, Pavel!'),
          on_success,
          on_error)

def on_success(obj):
    print 'on_success ', obj

def on_error(error_code, error_msg, request_params):
    print 'error  ', error_code, ': ', error_msg