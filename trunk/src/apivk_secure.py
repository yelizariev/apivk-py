def withdrawVotes(uid, votes):
    return {
        'uid': uid,
        'votes': votes,
        'method': 'secure.withdrawVotes'}

def saveAppStatus(uid, status):
    return {
        'uid': uid,
        'status': status,
        'method': 'secure.saveAppStatus'}

def getProfiles(uids, fields):
    """uids - list string id"""
    return {
        'uids': ','.join(uids),
        'fields': ','.join(fields),
        'method': 'secure.getProfiles'}

def setCounter(uid, counter):
    return {
        'uid':uid,
        'method':'secure.setCounter'}
