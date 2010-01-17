import threading, time, Queue
from . import connector

class VKThread(threading.Thread):
    def __init__(self, aqueue, squeue, conn):
        """send api request from queue with interval 1 second

        queue - queue of objects (params, on_success, on_error)
            params - see apivk.secure.*
            fok(obj)
            ferror
            (error_code, error_message, request_params)
                request_params = [{"key": "xxx", "value": "yyy"}, ...]
        conn - instance of apivk.connector.Connector"""
        self.aq = aqueue
        self.sq = squeue
        self.c = conn
        threading.Thread.__init__(self)

    def run(self):
        while True:
            if self.aq.empty() or not self.sq.empty():
                try:
                    item = self.sq.get(True, 1)
                except Queue.Empty:
                    continue
            else:
                try:
                    item = self.aq.get(False)
                except Queue.Empty:
                    continue

            while True:
                t = time.time()
                sleep = 1.0
                if send(item, self.c):
                    break
                else:
                    sleep += 0.2
                    #print self.name,' sleep = ', sleep
                    time.sleep(sleep)
            t = 1 + t - time.time()
            #print self.name,' t = ', t
            if t>0 :
                time.sleep(t)

def send(item, conn):
    """ return True if no error 6 'many requests per second'"""
    p, fok, ferror = item
    r = connector.req(p, conn) # r = response
    if r.has_key('response'):
        r = r['response']
        if fok:
            fok(r)
    else:
        r = r['error']
        error_code = int(r['error_code'])
        if (error_code == 6):
            return False
        elif ferror:
            ferror(error_code,
                   r['error_msg'],
                   r['request_params'])
    return True
