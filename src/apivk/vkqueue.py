import Queue
from . import connector, vkthread

class VKQueue(Queue.Queue):
    def __init__(self,
                 api_id,
                 api_secret,
                 req_per_second = 5,
                 max_queue_size = 1000):
        """requests queue"""
        Queue.Queue.__init__(self, max_queue_size)
        conn = connector.Connector(api_id, api_secret)
        for x in xrange(req_per_second):
            t = vkthread.VKThread(self, conn)
            t.start()

    def put(self, params, fok = None, ferror = None):
        """add request in queue

        fok(obj) - call on success response

        ferror(error_code, error_message, request_params) - call on
        error in response

        request_params = [{"key": "xxx", "value": "yyy"}, ...]
        """
        Queue.Queue.put(self, (params, fok, ferror))
