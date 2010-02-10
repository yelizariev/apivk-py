import Queue, threading
from . import connector, vkthread

class VKQueue():
    def __init__(self,
                 api_id,
                 api_secret,
                 req_per_second = 5,
                 async_queue_max_size = 1000):
        """requests queue

        sync request have priority over async request """
        self.aq = Queue.Queue(async_queue_max_size) #async
        self.sq = Queue.Queue(1)                    #sync
        conn = connector.Connector(api_id, api_secret)
        for x in xrange(req_per_second):
            t = vkthread.VKThread(self.aq, self.sq, conn) #thread
            t.start()

    def async(self, params, fok = None, ferror = None):
        """add request in queue

        fok(obj) - call on success response

        ferror(error_code, error_message, request_params) - call on
        error in response

        request_params = [{"key": "xxx", "value": "yyy"}, ...]
        """
        self.aq.put((params, fok, ferror))

    def sync(self, params, timeout = None):
        """add request in queue

        return obj on success response
        on error in response raise apivk.connector.VKError exception
        on timeout raise VKQueueTimeout exception"""
        lock = VKLock(self.sq, params, timeout)
        return lock.obj

class VKLock():
    def __init__(self, sq, params, timeout):
        self.lock = threading.Lock()
        try:
            sq.put((params, self.fok, self.ferror), True, timeout)
        except Queue.Full:
            raise VKQueueTimeout()
        self.lock.acquire()
        self.lock.acquire()#block
        if not self.ok:
            raise self.e

    def fok(self, obj):
        self.ok = True
        self.obj = obj
        self.lock.release()

    def ferror(self, code, msg, rp):
        self.ok = False
        self.e = VKError(code, msg, rp)
        self.lock.release()

class VKError(Exception):
    def __init__(self, code, msg, rp):
        self.code = code
        self.msg = msg
        self.rp = rp
    def __str__(self):
        return 'VKError %s "%s"'%(self.code, self.msg)

class VKQueueTimeout(Exception):
    def __str__(self):
        return 'VKQueueTimeout'
