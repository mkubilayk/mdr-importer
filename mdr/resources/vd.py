from middlewares import consume
from mdr import config


def get(options):
    '''
        Get value domain with the given id.
    '''
    _path = config.apihost + '/vd/%(id)s'

    err, res = consume('get', _path % options)

    if err:
        raise Exception(err, res)

    return res


def save(options):
    '''
        Create a new value domain.
    '''
    _path = config.apihost + '/cd/%(cd)s/vd'

    err, res = consume('post', _path % options, {
            'conceptualDomainID': options['cd'],
            'contextID': options['context'],
            'dataType': {
                'schemeReference': options['dt']['scheme'],
                'datatypeName': options['dt']['name']
            },
            'enumerated': options['enumerated'],
            'permissibleValues': options['pvs'],
            'name': options['name'],
            'definition': options['definition'] if 'definition' in options else options['name'].lower()
        })

    if err:
        raise Exception(err, res)

    return res
