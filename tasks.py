# ------------------------------------------------------------------------------
# IMPORTS ----------------------------------------------------------------------

from os      import system
from os      import listdir  as list_dir
from os.path import basename as base_name
from os.path import dirname  as dir_name
from os.path import realpath as real_path
from os.path import relpath  as rel_path
from os.path import isfile   as is_file
from os.path import join     as join_path
from invoke  import task

# ------------------------------------------------------------------------------
# CONFIGURATION ----------------------------------------------------------------

ROOT_DIR   = dir_name(real_path(__file__))
SHARED_DIR = join_path(ROOT_DIR, 'shared')
TEST_DIR   = join_path(ROOT_DIR, 'test')

# ------------------------------------------------------------------------------
# TASKS ------------------------------------------------------------------------

@task(help={'ctf_name': 'CTF name', 'challenge_name': 'Challenge name'})
def create_challenge(ctf_name, challenge_name):
    """Prepare the storage for a CTF challenge."""
    challenge_dir = join_path(ROOT_DIR, ctf_name, challenge_name)
    shared_link   = rel_path(SHARED_DIR, challenge_dir)

    print('Preparing {storage} for challenge {challenge} of CTF {ctf}'.format(
        storage=challenge_dir, challenge=challenge_name, ctf=ctf_name))

    os.makedirs(challenge_dir)
    os.symlink(shared_link, join_path(challenge_dir, 'shared'))

@task
def test():
    for file_rel_path in list_dir(TEST_DIR):
        file_path = join_path(TEST_DIR, file_rel_path)
        file_name = base_name(file_path)
        if (is_file(file_path)
            and file_name.startswith('test_')
            and file_name.endswith('.py')):
            system('python {}'.format(file_path))

@task
def cleanup():
    system('find . -name "*.pyc" -exec rm {} \;')

# ------------------------------------------------------------------------------
# vim: set filetype=python :
