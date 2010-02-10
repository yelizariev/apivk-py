import time

delta = 0
def timestamp():
    return int(time.time())+delta

### init
import urllib2, hashlib, re

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
    delta = int(m.group(1)) - int(time.time())
    #print 'delta = ', delta
else:
    raise Exception('unixtime response: '+r)
