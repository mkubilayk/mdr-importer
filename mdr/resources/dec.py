from middlewares import consume
from mdr import config


def save(options, oc):
    '''
        Create a new data element concept.
    '''
    _path = config.apihost + '/oc/%(id)s/dec'

    err, res = consume('post', _path % oc, {
            'propertyName': options['name'],
            'propertyDefinition': options.get('definition', options['name'].lower()),
            'objectClassID': oc['id'],
            'mappings': options.get('mappings', []),
            'definition': oc['name'] + ':' + options['name'],
            'contextID': options['context'],
            'conceptualDomainID': options['cd']['id']
        })

    if err:
        raise Exception(err)

    return res
