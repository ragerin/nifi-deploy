""" 
This file is used for the CLI tool.
By default setup.py links `nifi-deploy` as an executable
to this file.
"""

import argparse


def export_function(args):
    nifi_host       = args.nifi_host
    username        = args.username
    password        = args.password
    uuid            = args.uuid    
    name            = args.name
    description     = args.description
    filename        = args.filename
    quiet           = args.quiet
    keep_template   = args.keep_template

    n = NifiInstance(nifi_host, username=username, password=password)
    template_id = None

    template = n.create_template(
        pg_id=uuid,
        name=name,
        desc=description
        )
    
    if not template:
        return
    
    content = n.export_template(template.id, filename)

    if not args.quiet:
        print(content)
    
    if not args.keep_template and template:
        n.delete_template(template.id)


def import_function(args):
    nifi_host       = args.nifi_host
    username        = args.username
    password        = args.password
    filename        = args.filename

    n = NifiInstance(nifi_host, username=username, password=password)

    n.import_template(args.filename)


def cli():
    ### argparse setup
    parser = argparse.ArgumentParser(prog='nifi-deploy')
    parser.add_argument('-v', '--version', action='store_true', default=False) 
    subparsers = parser.add_subparsers(title='Actions', help='Append `--help` to view action specific help')


    ### export subparser
    example_usage = """EXAMPLE USAGE:
    nifi-deploy export -n https://nifihost:9090 0a7361fd-015f-1000-ffff-ffffd2cbc7a7 my_great_template -u john -p badpractice -d template description -f c:\\temp\\my_great_template_export.xml --keep_template
    """
    parser_export = subparsers.add_parser('export', epilog=example_usage)
    parser_export.add_argument('uuid', help='UUID of a process group to export as a template XML')
    parser_export.add_argument('name', help='Name of exported template - also the name internally if `--keep_template` is included')
    parser_export.add_argument('-n', '--nifi_host', help='Nifi host (typically http://<nifihost>:8080), else using environment variable `NIFI_HOST`')
    parser_export.add_argument('-u', '--username', help='Nifi username, else using environment variable `NIFI_USERNAME`')
    parser_export.add_argument('-p', '--password', help='Nifi password, else using environment variable `NIFI_PASSWORD`')
    parser_export.add_argument('-d', '--description', help='Description of the template - also used internally if `--keep_template` is included')
    parser_export.add_argument('-f', '--filename', help='Path to save exported XML to')
    parser_export.add_argument('-q', '--quiet', action='store_true', default=False, help='Do not output exported XML to stdout')
    parser_export.add_argument('-k', '--keep_template', action='store_true', default=False, help='Keep the template in Nifi after export, else exclusively export XML and delete the temporarily instantiated template')
    parser_export.set_defaults(func=export_function)


    ### import subparser
    example_usage = """EXAMPLE USAGE:
    nifi-deploy import -n https://nifihost:9090 c:\\temp\\my_great_template_export.xml -u john -p badpractice
    """
    parser_import = subparsers.add_parser('import', epilog=example_usage)
    parser_import.add_argument('filename', help='Path to template XML file for uploading to Nifi')
    parser_import.add_argument('-n', '--nifi_host', help='Nifi host (typically http://<nifihost>:8080), else using environment variable `NIFI_HOST`')
    parser_import.add_argument('-u', '--username', help='Nifi username, else using environment variable `NIFI_USERNAME`')
    parser_import.add_argument('-p', '--password', help='Nifi password, else using environment variable `NIFI_PASSWORD`')
    parser_import.set_defaults(func=import_function)


    ### show usage help
    args = parser.parse_args()
    if getattr(args, 'version', None):
        print(__version__)
        return
    if getattr(args, 'func', None):
        args.func(args)
    else:
        parser.print_help()


if not __name__ == '__main__':
    from . import __version__
    from .nifi import NifiInstance

else:
    # HACK: Extract version with regex from __init__.py when run as a script
    import os
    from re import compile
    pattern = compile('__version__\s+=\s+\'(.*)\'')
    path = os.path.join( os.path.dirname(os.path.realpath(__file__)), '__init__.py' )
    with open(path) as fd:
        __version__ = pattern.search(fd.read()).group(1)
    #
    from nifi import NifiInstance
    cli()