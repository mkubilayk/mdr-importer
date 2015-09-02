from middlewares import consume
from mdr import config


def save(options):
    '''
        Create a new data element.
    '''
    _path = config.apihost + '/context/%(context)s/de'

    err, res = consume('post', _path % options, {
            'name': options['name'],
            'definition': options.get('definition', options['name'].lower()),
            'dataElementConceptID': options['dec'],
            'valueDomainID': options['vd']['id'],
            'valueDomainName': options['vd']['name'],
            'contextID': options['context'],
            'extractionSpecs': options.get('xspec', [])
        })

    if err:
        raise Exception(err, res)

    return res
