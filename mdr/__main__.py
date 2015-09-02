import sys
from os import path
from mdr import importer
from mdr.utils import storage, args


# store module directory path for the future
storage.memcache('module-root', path.dirname(path.abspath(__file__)))

# parse cmd line args
options = args.parse()

# launch
if options.drop:
    importer.drop(options.drops)
elif options.force:
    importer.drop()
    importer.context(options.ctxs)
    importer.extractionSpecification(options.xss)
else:
    importer.context(options.ctxs)
    importer.extractionSpecification(options.xss)
