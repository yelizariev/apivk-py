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
