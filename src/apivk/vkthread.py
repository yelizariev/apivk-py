import threading, time
from . import connector

class VKThread(threading.Thread):
    def __init__(self, queue, conn):
        """send api request from queue with interval 1 second

        queue - queue of objects (params, on_success, on_error)
            params - see apivk.secure.*
            fok(obj)
            ferror
            (error_code, error_message, request_params)
                request_params = [{"key": "xxx", "value": "yyy"}, ...]
        conn - instance of apivk.connector.Connector"""
        self.q = queue
        self.c = conn
        threading.Thread.__init__(self)

    def run(self):
        while True:
            self.p, self.fok, self.ferror = self.q.get()
            while True:
                t = time.time()
                sleep = 1.0
                if self.send():
                    break
                else:
                    sleep += 0.2
                    #print self.name,' sleep = ', sleep
                    time.sleep(sleep)
            t = 1 + t - time.time()
            #print self.name,' t = ', t
            if t>0 :
                time.sleep(t)

    def send(self):
        """ return True if no error 6 'many requests per second'"""
        r = connector.req(self.p, self.c) # r = response
        if r.has_key('response'):
            if self.fok:
                self.fok(r['response'])
            else:
                if self.ferror:
                    r = r['error']
                    error_code = int(r['error_code'])
                    if (error_code == 6):
                        return False
                    self.ferror(error_code,
                                r['error_message'],
                                r['request_params'])
        return True
