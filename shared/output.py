# IMPORTS ----------------------------------------------------------------------

import sys

# ------------------------------------------------------------------------------
# MODULE INFORMATIONS ----------------------------------------------------------

__all__ = [
    'BLACK', 'RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN', 'WHITE',
    'setupoutput',
    'colorize', 'printcolored',
    'printtitle', 'printsuccess', 'printerror', 'printinfo', 'printdebug',
]

# ------------------------------------------------------------------------------
# MODULE SETUP -----------------------------------------------------------------

def setupoutput(verbose=False, automaticindent=True):
    global _VERBOSE
    global _INDENT

    _VERBOSE = verbose
    if automaticindent:
        _INDENT = 0
        sys.settrace(_tracefunc)

# ------------------------------------------------------------------------------
# COLORS -----------------------------------------------------------------------

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

def colorize(text, color):
    return "\x1b[1;%dm" % (30 + color) + text + "\x1b[0m"

# ------------------------------------------------------------------------------
# AUTOMATIC INDENT -------------------------------------------------------------

_INDENT = 0

def _tracefunc(frame, event, arg):
    global _INDENT
    if event == 'call':
        if not frame.f_code.co_name.startswith('_'):
            _INDENT += 1
    elif event == 'return':
        if not frame.f_code.co_name.startswith('_'):
            _INDENT -= 1
    return _tracefunc

# ------------------------------------------------------------------------------
# PRINT FUNCTIONS --------------------------------------------------------------

_VERBOSE = False

def printcolored(text, color=WHITE, prefix=u'\u2022', indent=0):
    indentstr='  ' * indent
    msg = u'{prefix} {text}'.format(prefix= prefix, text=text)
    msg = filter(None, msg.split('\n'))
    msg = indentstr + '\n{}'.format(indentstr).join(msg)
    print(colorize(msg, color))

def printtitle(msg, indent=None):
    printcolored(msg, color=MAGENTA, indent=indent or _INDENT - 1)

def printsuccess(msg, indent=None):
    printcolored(msg, color=GREEN, indent=indent or _INDENT)

def printerror(msg, indent=None):
    printcolored(msg, color=RED, indent=indent or _INDENT)

def printinfo(msg, indent=None):
    printcolored(msg, color=BLUE, indent=indent or _INDENT)

def printdebug(msg, indent=None):
    if _VERBOSE:
        printcolored(msg, color=YELLOW, indent=indent or _INDENT)

# ------------------------------------------------------------------------------
# vim: set filetype=python :
