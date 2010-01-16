import hashlib

class Auth:
    def __init__(self, api_id, api_secret):
        self.api_id = api_id
        self.api_secret = api_secret

    def check(self, id, auth_key):
        m = hashlib.md5()
        m.update(self.api_id)
        m.update('_')
        m.update(id)
        m.update('_')
        m.update(self.api_secret)
        return m.hexdigest()==auth_key
