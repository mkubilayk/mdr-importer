from middlewares import consume
from mdr import config


def save(options):
    '''
        Create a new object class under the given context.
    '''
    _path = config.apihost + '/context/%(context)s/oc'

    err, res = consume('post', _path % {'context': options['context']}, {
            'contextID': options['context'],
            'name': options['name'],
            'definition': options['definition']
        })

    if err:
        raise Exception(err, res)

    return res
