import pyvkt.secure as secure
from pyvkt.vkqueue import VKQueue

q = VKQueue(api_id='1', api_secret='apisecuresecret', req_per_second = 5)
q.add_req(secure.saveAppStatus(uid='1', status='Hi, Pavel!'))

def on_success(obj):
    print 'on_success ', obj

def on_error(error_code, error_msg, request_params):
    print 'error  ', error_code, ': ', error_msg
