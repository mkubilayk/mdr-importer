from middlewares import consume
from mdr import config


def get(options):
    '''
        Get conceptual domain with the given name.
    '''
    _path = config.apihost + '/repository/cd/search'

    err, res = consume('get', _path, params={'q': options['name']})

    if err:
        raise Exception(err, res)

    for cd in res:
        if cd['name'] == options['name']:
            return cd


def save(options):
    '''
        Create a conceptual domain.
    '''
    _path = config.apihost + '/repository/cd'

    err, res = consume('post', _path, {
            'name': options['name'],
            'definition': options['definition'] if 'definition' in options else options['name'].lower(),
            'enumerated': options['enumerated'],
            'id': options['oid'] if options['enumerated'] else None
        })

    if err:
        raise Exception(err, res)

    return res


def update(options):
    '''
        Update the given conceptual domain.
    '''
    _path = config.apihost + '/repository/cd'

    err, res = consume('put', _path, {
            'name': options['name'],
            'definition': options['definition'] if 'definition' in options else options['name'].lower(),
            'enumerated': options['enumerated'],
            'id': options['id']
        })

    if err:
        raise Exception(err, res)

    return res
