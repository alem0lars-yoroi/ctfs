# ------------------------------------------------------------------------------
# MODULE INFORMATIONS ----------------------------------------------------------

__all__ = [
    'BLACK', 'RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN', 'WHITE',
    'indent', 'de_indent', 'enable_verbose', 'disable_verbose',
    'colorize', 'print_colored',
    'print_title', 'print_success', 'print_error', 'print_info', 'print_debug',
]

# ------------------------------------------------------------------------------
# COLORS -----------------------------------------------------------------------

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

def colorize(text, color):
    return "\x1b[1;%dm" % (30 + color) + text + "\x1b[0m"

# ------------------------------------------------------------------------------
# MANAGE INDENTATION -----------------------------------------------------------

_INDENT = 0

def indent(amount=1):
    global _INDENT
    _INDENT += amount

def de_indent(amount=1):
    global _INDENT
    _INDENT -= amount

# ------------------------------------------------------------------------------
# MANAGE VERBOSITY -------------------------------------------------------------

_VERBOSE = False

def enable_verbose():
    global _VERBOSE
    _VERBOSE = True

def disable_verbose():
    global _VERBOSE
    _VERBOSE = False

# ------------------------------------------------------------------------------
# PRINT FUNCTIONS --------------------------------------------------------------

def print_colored(text, color=WHITE, prefix=u'\u2022', indent=None):
    indent = indent or _INDENT
    indent_str='  ' * indent
    msg = u'{prefix} {text}'.format(prefix=prefix, text=text)
    msg = filter(None, msg.split('\n'))
    msg = indent_str + '\n{}'.format(indent_str).join(msg)
    print(colorize(msg, color))

def print_title(msg, indent=None):
    print_colored(msg, color=MAGENTA, indent=indent)

def print_success(msg, indent=None):
    print_colored(msg, color=GREEN, indent=indent)

def print_error(msg, indent=None):
    print_colored(msg, color=RED, indent=indent)

def print_info(msg, indent=None):
    print_colored(msg, color=BLUE, indent=indent)

def print_debug(msg, indent=None):
    if _VERBOSE:
        print_colored(msg, color=YELLOW, indent=indent)

# ------------------------------------------------------------------------------
# vim: set filetype=python :
