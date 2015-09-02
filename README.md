# mdr-importer

```bash
$ python -m mdr [-h] [--force] [--drop] [-files [foo]] [-ctx [foo]] [-xs [foo]]
```

- `-h, --help`      show this help message and exit
- `--force`         Force reload. Drop current contex, conceptual domains and data elements. Import provided context and extraction specification.
- `--drop`          Drop existing context and models. Import nothing. Do not combine this argument with others. If you want to drop and import with a single command, use `--force` instead.
- `-files [foo]`    Used for specifying files to `--drop` option.
- `-ctx [foo]`      Import a context with its conceptual domains, data types, and data elements provided in the file. Make sure that `<foo.ctx>` exists in `/data` folder.
- `-xs [foo]`       Import provided extraction specifications. Make sure that related data elements are already available in the registry and `<foo.xs>` exists in `/data` folder.
