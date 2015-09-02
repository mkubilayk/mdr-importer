from middlewares import consume
from mdr import config


def query(cd):
    '''
        Get all value meanings attached to the given conceptual domain.
    '''
    _path = config.apihost + '/repository/cd/%(domain)s/vm'

    err, res = consume('get', _path % {'domain': cd})

    if err:
        raise Exception(err)

    return res


def save(cd, id, description):
    '''
        Create a value meaning for the given conceptual domain.
    '''
    _path = config.apihost + '/cd/%(domain)s/vm'

    err, res = consume('post', _path % {'domain': cd}, {
            'id': id,
            'description': description,
            'conceptualDomainID': cd
        })

    if err:
        raise Exception(err)

    return res


def delete(vm, cd):
    '''
        Delete the value meaning with the given id and conceptual domain.
    '''
    _path = config.apihost + '/cd/%(domain)s/vm'

    err, res = consume('del', _path % {'domain': cd}, {
            'id': vm
        })

    if err:
        raise Exception(err)

    return res


def drop(cd):
    '''
        Delete all value meanings attached to the given conceptual domain.
    '''
    vms = query(cd)

    for valmean in vms:
        delete(valmean['id'], cd)
