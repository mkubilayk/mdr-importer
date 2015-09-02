from os import path
from mdr import config
from mdr.utils import storage


def run(filepath):
    f = storage.abspath(filepath)
    name, ext = path.splitext(f)

    if ext == '.xs':
        return _xs(f)
    elif ext == '.ctx':
        return _ctx(f)


def _header(fp, typ):
    header = {'type': typ}
    for line in fp:
        if not line.strip():
            break

        k, v = [x.strip() for x in line.strip().split('=')]
        header[k] = v

    return header


def _ctx(filepath):
    ctx = {}
    with open(filepath, 'r') as fp:
        ctx['header'] = _header(fp, 'ctx')

        ctx['ocs'] = {}
        ctx['cds'] = {}
        ctx['dts'] = {}
        for line in fp:
            entry = line.strip().split(config.delimiter)

            if len(entry) < 10:
                # raise error
                print 'err on', line
                continue

            deid, oc, ocdefn, prop, dt, cd, enum, oid, pv, defn = [x if x != '.' else None for x in entry[:10]]
            enum = bool(enum)

            # add object class to ocs with its definition
            if oc not in ctx['ocs']:
                ctx['ocs'][oc] = {
                    'name': oc,
                    'definition': ocdefn,
                    'properties': []
                }

            # add property to the object class
            ctx['ocs'][oc]['properties'].append({
                'id': {
                    'local': deid,
                    'remote': None
                },
                'name': prop,
                'cd': cd,
                'definition': defn
            })

            # add conceptual domain to cds with data type
            # if it is enumarated permissible values and oid is also set
            pvs = {}
            if pv:
                for vm in pv.strip().split('|'):
                    if '=' in vm:
                        vmid, vmdefn = vm.split('=')
                        pvs[vmid] = vmdefn

            ctx['cds'][cd] = {
                'name': cd,
                'enumerated': enum,
                'dt': dt,
                'pvs': pvs,
                'oid': oid
            }

    # add scheme references to data types,
    # if data type is a custom class, it is the scheme reference
    # if it is a primitive type, scheme reference is ISO11404
    for _, cd in ctx['cds'].iteritems():
        dt = cd['dt']
        if dt in ctx['ocs']:
            ctx['dts'][dt] = {
                'name': dt,
                'scheme': dt,
                'type': 'custom'
            }
        else:
            ctx['dts'][dt] = {
                'name': dt,
                'scheme': 'ISO11404',
                'type': 'primitive'
            }

    return ctx


def _xs(filepath):
    xs = {}
    with open(filepath, 'r') as fp:
        xs['header'] = _header(fp, 'xs')

        xs['entries'] = {}
        for line in fp:
            entry = line.strip().split(config.delimiter)

            if len(entry) < 3:
                continue

            de, typ, val = entry[:3]

            if de not in xs['entries']:
                xs['entries'][de] = []

            xs['entries'][de].append({
                'type': typ,
                'value': val
            })

    return xs
