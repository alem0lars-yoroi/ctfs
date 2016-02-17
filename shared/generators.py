# ------------------------------------------------------------------------------
# IMPORTS ----------------------------------------------------------------------

from random import SystemRandom
from string import ascii_uppercase, ascii_lowercase, digits

# ------------------------------------------------------------------------------
# MODULE INFORMATIONS ----------------------------------------------------------

__all__ = ['generate_string']

# ------------------------------------------------------------------------------
# GENERATORS -------------------------------------------------------------------

def generate_string(size=8, chars=ascii_uppercase + ascii_lowercase + digits):
    return ''.join(SystemRandom().choice(chars) for _ in range(size))

# ------------------------------------------------------------------------------
# vim: set filetype=python :
