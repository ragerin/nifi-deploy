""" 
This file is used for the CLI tool.
By default setup.py links `nifi-deploy` as an executable
to this file.
"""

import argparse

from nifi import NifiInstance


def export_function(args):
    nifi_host       = args.nifi_host
    username        = args.username
    password        = args.password
    uuid            = args.uuid    
    name            = args.name
    description     = args.description
    filename        = args.filename
    stdout          = args.stdout
    keep_template   = args.keep_template

    n = NifiInstance(nifi_host, username=username, password=password)
    template_id = None

    try:
        template_id = n.create_template(
            pg_id=uuid,
            name=name,
            desc=description
            ).template.id
        
        r = n.export_template(template_id, filename)
        if args.stdout and args.filename:
            print(r.content.decode())
        
    finally:
        if not args.keep_template:
            n.delete_template(template_id)


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
    subparsers = parser.add_subparsers(title='Actions', help='Append `--help` to view action specific help')


    ### export subparser
    example_usage = """EXAMPLE USAGE:
    nifi-deploy export -n https://nifihost:9090 -u john -p badpractice 0a7361fd-015f-1000-ffff-ffffd2cbc7a7 my_great_template -d template description -f c:\\temp\\my_great_template_export.xml
    """
    parser_export = subparsers.add_parser('export', epilog=example_usage)
    parser_export.add_argument('uuid', help='UUID of a process group to export as a template XML')
    parser_export.add_argument('name', help='Name of exported template - also the name internally if `--keep_template` is included')
    parser_export.add_argument('-n', '--nifi_host', help='Nifi host (typically http://<nifihost>:8080), else using environment variable `NIFI_HOST`')
    parser_export.add_argument('-u', '--username', help='Nifi username, else using environment variable `NIFI_USERNAME`')
    parser_export.add_argument('-p', '--password', help='Nifi password, else using environment variable `NIFI_PASSWORD`')
    parser_export.add_argument('-d', '--description', help='Description of the template - also used internally if `--keep_template` is included')
    parser_export.add_argument('-f', '--filename', help='Path to save exported XML to')
    parser_export.add_argument('-s', '--stdout', action='store_true', default=False, help='Output exported XML to stdout - default if `--filename` is not supplied')
    parser_export.add_argument('-k', '--keep_template', action='store_true', default=False, help='Keep the template in Nifi after export, else exclusively export XML and delete the temporarily instantiated template')
    parser_export.set_defaults(func=export_function)


    ### import subparser
    example_usage = """EXAMPLE USAGE:
    nifi-deploy import -n https://nifihost:9090 -u john -p badpractice c:\\temp\\my_great_template_export.xml
    """
    parser_import = subparsers.add_parser('import', epilog=example_usage)
    parser_import.add_argument('filename', help='Path to template XML file for uploading to Nifi')
    parser_import.add_argument('-n', '--nifi_host', help='Nifi host (typically http://<nifihost>:8080), else using environment variable `NIFI_HOST`')
    parser_import.add_argument('-u', '--username', help='Nifi username, else using environment variable `NIFI_USERNAME`')
    parser_import.add_argument('-p', '--password', help='Nifi password, else using environment variable `NIFI_PASSWORD`')
    parser_import.set_defaults(func=import_function)


    ### show usage help
    args = parser.parse_args()
    if getattr(args, 'func', None):
        args.func(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    cli()