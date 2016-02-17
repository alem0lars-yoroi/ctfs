# IMPORTS ----------------------------------------------------------------------

import sys
from collections   import OrderedDict
from ast           import literal_eval
from argparse      import ArgumentParser
from shared.output import print_error, enable_verbose

# ------------------------------------------------------------------------------
# MODULE INFORMATIONS ----------------------------------------------------------

__all__ = ['main_with_cmds', 'arg_autoint', 'arg_literal']

# ------------------------------------------------------------------------------
# CUSTOM ARGUMENTS -------------------------------------------------------------

def arg_autoint(x):
    return int(x, 0)

def arg_literal(x):
    return literal_eval(x)

# ------------------------------------------------------------------------------
# MAIN POLICIES ----------------------------------------------------------------

def main_with_cmds(prog, desc, cmds, testfn=None):
    parser = ArgumentParser(prog=prog, description=desc)
    parser.add_argument('--verbose', '-v', action='store_true',
            help='Enable verbose output')
    subparsers = parser.add_subparsers(title='subcommands', dest='parser_name')

    # Parser for the test command.
    if testfn:
        parser_test = subparsers.add_parser('test', help='Run tests')

    # Parser for the sub-commands.
    for cmd_name, cmd_info in cmds.items():
        cmd_parser = subparsers.add_parser(cmd_name,
                help='Execute the command: {}'.format(cmd_name))
        if isinstance(cmd_info, dict) and 'args' in cmd_info:
            args = OrderedDict()
            for arg_info in cmd_info['args']:
                name = arg_info.pop('name')
                args[name] = arg_info
            for arg_name, arg_params in args.items():
                cmd_parser.add_argument(arg_name, **arg_params)

    # Parse arguments.
    args = parser.parse_args(sys.argv[1:])

    if args.verbose:
        enable_verbose()

    # Call the right sub-command handler.
    status = None
    if args.parser_name is None:
        print_error('You need to specify the command (see --help)')
    elif args.parser_name == 'test':
        status = testfn()
    else:
        for cmd_name, cmd_info in cmds.items():
            if args.parser_name == cmd_name:
                if isinstance(cmd_info, dict) and 'handler' in cmd_info:
                    status = cmd_info['handler'](args)
                elif hasattr(cmd_info, '__call__'):
                    status = cmd_info(args)
                else:
                    print_error('Invalid informations for command: {}'.format(
                        cmd_name))
                    status = -999

    # Exit from the program with the status-code relative to the command exit
    # status.
    if status is None:
        exit(0)
    else:
        exit(status)

# ------------------------------------------------------------------------------
# vim: set filetype=python :
