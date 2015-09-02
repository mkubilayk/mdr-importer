import json
import requests

from mdr import config
from mdr.utils import storage


def consume(method, path, payload=None, cookies=None, params=None):
    _method = method.lower()
    if _method == 'get':
        _method = requests.get
    elif _method == 'post':
        _method = requests.post
    elif _method == 'put':
        _method = requests.put
    elif _method == 'delete' or _method == 'del':
        _method = requests.delete

    _headers = {
        'content-type': 'application/json'
    }

    _payload = json.dumps(payload)
    _cookies = cookies if cookies else storage.memcache('cookie')

    r = _method(path, data=_payload, headers=_headers, cookies=_cookies, params=params)

    if r.status_code == requests.codes.ok:
        return (None, r.json()) if r.content else (None, {})
    else:
        return (r.status_code, r.reason)
