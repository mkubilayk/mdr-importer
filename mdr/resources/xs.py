from middlewares import consume
from mdr import config


def save(options): #concept, oid, type, value, de):
    '''
        Create a new extraction specification for the given data element.
    '''
    _path = config.apihost + '/de/%(de)s/extractionspecification'

    err, res = consume('post', _path % options, {
        'modelName': options['concept'],
        'modelOID': options['oid'],
        'type': options['type'],
        'value': options['value']
    })

    if err:
        raise Exception(err, res)

    return res

def delete(options):
    '''
        Delete an existing extraction specification.
    '''
    _path = config.apihost + '/de/%(de)s/extractionspecification'

    err, res = consume('del', _path % options, {
        'modelOID': options['oid'],
        'type': options['type'],
        'value': options['value']
    })

    if err:
        raise Exception(err, res)
