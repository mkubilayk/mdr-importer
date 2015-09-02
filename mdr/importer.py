import json
import parser

from mdr import config
from mdr.resources import auth, cd, ctx, de, dec, dt, oc, vd, vm, xs
from mdr.utils import storage
from progressbar import ProgressBar


def drop(files=[]):
    _authenticate()
    if not files:
        files = storage.batch()

    for f in files:
        obj = storage.persistent(f)
        if obj['header']['type'] == 'ctx':
            _dropContext(obj)
        elif obj['header']['type'] == 'xs':
            _dropExtractionSpecification(obj)

        storage.rm(f)


def context(files):
    _authenticate()
    for f in files:
        context = parser.run('data/' + f + '.ctx')

        # create context, save context id
        res = ctx.save(context['header']['Context Name'], context['header']['Context Definition'])
        context['id'] = res['id']

        # create object classes, save object class id
        for _, _oc in context['ocs'].iteritems():
            _oc['context'] = context['id']
            res = oc.save(_oc)
            _oc['id'] = res['id']

        # create data types
        for _, _dt in context['dts'].iteritems():
            dt.save(_dt)

        # create conceptual domains, update
        # in the case of name collision
        # then create value domains
        context['vds'] = {}
        for _, _cd in context['cds'].iteritems():
            existing = cd.get({
                'name': _cd['name']
            })

            if existing:
                _cd['id'] = existing['id']
                cd.update(_cd)
            else:
                res = cd.save(_cd)
                _cd['id'] = res['id']

            _vd = {
                'cd': _cd['id'],
                'name': _cd['name'] + ':' + _cd['dt'],
                'context': context['id'],
                'dt': context['dts'][_cd['dt']],
                'enumerated': _cd['enumerated'],
                'pvs': []
            }
            res = vd.save(_vd)
            _vd['id'] = res['id']
            context['vds'][_cd['name']] = _vd

        # create data element concepts
        # and data elements
        context['demap'] = {}
        for _, _oc in context['ocs'].iteritems():
            for _de in _oc['properties']:
                _de['cd'] = context['cds'][_de['cd']]
                _de['context'] = context['id']
                res = dec.save(_de, _oc)
                _de['dec'] = res['id']

                _de['vd'] = context['vds'][_de['cd']['name']]
                res = de.save(_de)
                _de['id']['remote'] = res['id']

                context['demap'][_de['id']['local']] = _de['id']['remote']

        storage.persistent(f + '.ctx', context)


def extractionSpecification(files):
    _authenticate()
    for f in files:
        xspec = parser.run('data/' + f + '.xs')

        # create context, save context id
        cm = xspec['header']['Concept Model']
        oid = xspec['header']['OID']

        ctx = storage.persistent(xspec['header']['Context Name'].lower() + '.ctx')

        for de, xss in xspec['entries'].iteritems():
            for _xs in xss:
                _xs['de'] = ctx['demap'][de]
                _xs['concept'] = cm
                _xs['oid'] = oid

                xs.save(_xs)

        storage.persistent(f + '.xs', xspec)


def _authenticate():
    res = auth.login(config.username, config.password)
    storage.memcache('cookie', {
        'SID': res['sessionID']
    })


def _dropContext(obj):
    ctx.delete(obj)

    for _, _dt in obj['dts'].iteritems():
        dt.delete(_dt)


def _dropExtractionSpecification(obj):
    for _, _de in obj['entries'].iteritems():
        for _xs in _de:
            xs.delete(_xs)
