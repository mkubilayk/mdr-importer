from mdr import config
from middlewares import consume


def login(username, password):
    '''
        Authenticate the app with the given username and password.
    '''
    _path = config.apihost + '/auth'

    err, res = consume('put', _path, {
            'username': username,
            'password': password
        })

    if err:
        raise Exception(err, res)

    return res
