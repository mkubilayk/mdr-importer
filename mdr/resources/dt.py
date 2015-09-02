from middlewares import consume
from mdr import config


def get(options):
    '''
        Get data type with the given name.
    '''
    dts = query()

    for dt in dts:
        if dt['datatypeName'] == options['name']:
            return dt


def query():
    '''
        Get all data types available in the repository.
    '''
    _path = config.apihost + '/repository/dt'

    err, res = consume('get', _path)

    if err:
        raise Exception(err, res)

    return res


def save(options):
    '''
        Create a new data type.
    '''
    _path = config.apihost + '/repository/dt'

    err, res = consume('post', _path, {
            'datatypeName': options['name'],
            'schemeReference': options['scheme']
        })

    if err:
        raise Exception(err, res)

    return res


def delete(options):
    '''
        Delete the data type with the given name and scheme reference.
    '''
    _path = config.apihost + '/repository/dt'

    err, res = consume('del', _path, {
            'datatypeName': options['name'],
            'schemeReference': options['scheme']
        })

    if err:
        raise Exception(err, res)
