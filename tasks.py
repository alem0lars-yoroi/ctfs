# ------------------------------------------------------------------------------
# IMPORTS ----------------------------------------------------------------------

import os, sys

import invoke

# ------------------------------------------------------------------------------
# CONFIGURATION ----------------------------------------------------------------

ROOTDIR   = os.path.dirname(os.path.realpath(__file__))
SHAREDDIR = os.path.join(ROOTDIR, 'shared')

# ------------------------------------------------------------------------------
# TASKS ------------------------------------------------------------------------

@invoke.task(help={'ctfname': 'CTF name', 'challengename': 'Challenge name'})
def createchallenge(ctfname, challengename):
    """Prepare the storage for a CTF challenge."""
    chaldir=os.path.join(ROOTDIR, ctfname, challengename)
    sharedlink=os.path.relpath(SHAREDDIR, chaldir)

    print('Preparing {storage} for challenge {challenge} of CTF {ctf}'.format(
        storage=chaldir, challenge=challengename, ctf=ctfname))

    os.makedirs(chaldir)
    os.symlink(sharedlink, os.path.join(chaldir, 'shared'))

# ------------------------------------------------------------------------------
# vim: set filetype=python :
