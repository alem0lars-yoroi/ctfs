# ------------------------------------------------------------------------------
# IMPORTS ----------------------------------------------------------------------

import sys
from concurrent.futures import ThreadPoolExecutor
from os.path            import dirname as dir_name, realpath as real_path
from time               import sleep
from unittest           import TestCase, main

try:
    from asyncio import get_event_loop
except ImportError: # Python 2 compatibility
    try:
        from trollius import get_event_loop
    except:
        print('Python 2 is supported through the external package ' +
              '`trollius`: you need to install it (`pip install trollius`)')
        exit(-1)

sys.path.append(dir_name(dir_name(real_path(__file__))))
from shared.irc    import IRCClient
from shared.output import enable_verbose, print_debug

# ------------------------------------------------------------------------------
# UTILITIES --------------------------------------------------------------------

def _delayed_disconnect(client, delay=1):
    def _inner():
        print_debug('Waiting {} second(s) before disconnect'.format(delay))
        sleep(delay)
        print_debug('Sending disconnect')
        client.disconnect()
    return _inner

def _spawn(func, max_workers=1):
    executor = ThreadPoolExecutor(max_workers=max_workers)
    return executor.submit(func).result()

# ------------------------------------------------------------------------------
# UNIT TESTS -------------------------------------------------------------------

class TestIRCClient(TestCase):
    def setUp(self):
        self._irc_host = 'irc.freenode.net'
        self._loop = get_event_loop()

    def test_connect(self):
        try:
            client = IRCClient.connect(host=self._irc_host, wait=False)
        except:
            self.fail('Failed to connect to IRC Server')

        _spawn(_delayed_disconnect(client))

        try:
            self._loop.run_until_complete(client.disconnect_future)
        except:
            self.fail('Failed to wait for disconnection')

# ------------------------------------------------------------------------------
# ENTRY POINT ------------------------------------------------------------------

if __name__ == '__main__':
    enable_verbose()
    main()

# ------------------------------------------------------------------------------
# vim: set filetype=python :
