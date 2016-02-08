# IMPORTS ----------------------------------------------------------------------

import argparse, ast, collections, sys
from shared.output import *

# ------------------------------------------------------------------------------
# MODULE INFORMATIONS ----------------------------------------------------------

__all__ = [
    'cmdmain', 'autoint'
]

# ------------------------------------------------------------------------------
# CUSTOM ARGUMENTS -------------------------------------------------------------

def literal(x):
    return ast.literal_eval(x)

def autoint(x):
    return int(x, 0)

# ------------------------------------------------------------------------------
# MAIN POLICIES ----------------------------------------------------------------

def cmdmain(prog, desc, cmds, testfn=None, automaticindent=True):
    parser = argparse.ArgumentParser(prog=prog, description=desc)
    parser.add_argument('--verbose', '-v', action='store_true',
            help='Enable verbose output')
    subparsers = parser.add_subparsers(title='subcommands', dest='parsername')

    # Parser for the test command.
    if testfn:
        parser_test = subparsers.add_parser('test', help='Run tests')

    # Parser for the sub-commands.
    for cmdname, cmdinfo in cmds.items():
        cmdparser = subparsers.add_parser(cmdname,
                help='Execute the command: {}'.format(cmdname))
        if isinstance(cmdinfo, dict) and 'args' in cmdinfo:
            args = collections.OrderedDict()
            for arginfo in cmdinfo['args']:
                name = arginfo.pop('name')
                args[name] = arginfo
            for argname, argparams in args.items():
                cmdparser.add_argument(argname, **argparams)

    # Parse arguments.
    args = parser.parse_args(sys.argv[1:])

    setupoutput(verbose=args.verbose, automaticindent=automaticindent)

    # Call the right sub-command handler.
    status = None
    if args.parsername is None:
        printerror('You need to specify the command (see --help)')
    elif args.parsername == 'test':
        status = testfn()
    else:
        for cmdname, cmdinfo in cmds.items():
            if args.parsername == cmdname:
                if isinstance(cmdinfo, dict) and 'handler' in cmdinfo:
                    status = cmdinfo['handler'](args)
                elif hasattr(cmdinfo, '__call__'):
                    status = cmdinfo(args)
                else:
                    printerror('Invalid info for command: {}'.format(cmdname))
                    status = -999

    # Exit from the program with the status-code relative to the command exit
    # status.
    if status is None:
        exit(0)
    else:
        exit(status)

# ------------------------------------------------------------------------------
# vim: set filetype=python :
