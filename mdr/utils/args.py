from argparse import ArgumentParser

_argparser = ArgumentParser()

_argparser.add_argument('--force', action='store_true', dest='force',
                        default=False,
                        help='Force reload. Drop current contex, conceptual domains \
                              and data elements. Import provided context and extraction \
                              specification.')

_argparser.add_argument('--drop', action='store_true', dest='drop',
                        default=False,
                        help='Drop existing context and models. Import nothing. Do \
                              not combine this argument with others. If you want to \
                              drop and import with a single command, use --force instead.')

_argparser.add_argument('-files', action='append', dest='drops', nargs='?', metavar='foo',
                        default=[],
                        help='Used for specifying files to --drop option.')

_argparser.add_argument('-ctx', action='append', dest='ctxs', nargs='?', metavar='foo',
                        default=[],
                        help='Import a context with its conceptual domains, data types, \
                              and data elements provided in the file. Make sure \
                              that <foo.ctx> exists in /data folder.')

_argparser.add_argument('-xs', action='append', dest='xss', nargs='?', metavar='foo',
                        default=[],
                        help='Import provided extraction specifications. Make sure \
                              that related data elements are already available in \
                              the registry and <foo.xs> exists in /data folder.')

def parse():
    global _argparser
    return _argparser.parse_args()
