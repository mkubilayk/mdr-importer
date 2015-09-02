from middlewares import consume
from mdr import config


def get(context):
    '''
        Get context with the given name.
    '''
    _path = config.apihost = '/repository'

    err, res = consume('get', _path)

    if err:
        raise Exception(err)

    for ctx in res:
        if ctx['name'] == context:
            return ctx


def save(name, definition):
    '''
        Create a new context.
    '''
    _path = config.apihost + '/repository'

    err, res = consume('post', _path, {
            'name': name,
            'definition': definition
        })

    if err:
        raise Exception(err)

    return res


def delete(options):
    '''
        Delete the existing context with the given id.
    '''
    _path = config.apihost + '/repository/%(id)s'

    err, res = consume('del', _path % options)

    # on success, api returns 204 no content. wtf?
    # if err:
    #     raise Exception(err, res)
