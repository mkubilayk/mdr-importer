import json
from os import path, makedirs, remove, listdir
from mdr import config

def memcache(key, value=None):
    '''
    '''
    if 'depot' not in memcache.__dict__:
        memcache.depot = {}     # TODO: use a decorator

    if value is None:
        return memcache.depot.get(key, None)
    else:
        memcache.depot[key] = value


def persistent(filepath, content=None):
    '''
        Deserialize the contents of a file as an object.
        Or serialize an object and persist it in a file.
    '''
    depot = memcache('module-root') + '/.depot'
    if not path.exists(depot):
        makedirs(depot)

    filepath = depot + '/' + filepath
    if content is None:
        if path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
        else:
            return None
    else:
        with open(filepath, 'w') as f:
            f.write(json.dumps(content, indent=2))


def batch():
    '''
        Return a generator to iterate over all files
        in the persistent storage.
    '''
    depot = memcache('module-root') + '/.depot'
    for f in listdir(depot):
        if path.isfile(path.join(depot, f)):
            yield f


def rm(filepath):
    '''
        Remove file from persistent storage.
    '''
    filepath = memcache('module-root') + '/.depot/' + filepath

    if path.exists(filepath):
        remove(filepath)


def abspath(relpath):
    return path.join(memcache('module-root'), relpath)
