# ------------------------------------------------------------------------------
# IMPORTS ----------------------------------------------------------------------

try:
    from asyncio import Protocol, Future, get_event_loop
except ImportError: # Python 2 compatibility
    try:
        from trollius import Protocol, Future, get_event_loop
    except:
        print('Python 2 is supported through the external package ' +
              '`trollius`: you need to install it (`pip install trollius`)')
        exit(-1)

from shared.output     import print_debug
from shared.generators import generate_string

# ------------------------------------------------------------------------------
# MODULE INFORMATIONS ----------------------------------------------------------

__all__ = ['IRCClient']

# ------------------------------------------------------------------------------
# CLIENT -----------------------------------------------------------------------

class IRCClient(Protocol):

    CMD_NICK = 'NICK {nick_name}'
    CMD_USER = 'USER {user_name} {host_name} {server_name} :{real_name}'

    def __init__(self, loop,
                 nick_name=generate_string(),
                 user_name=generate_string(),
                 real_name=generate_string(),
                 host_name=generate_string(),
                 server_name=generate_string(),
                 rcv_handler=None):
        self._transport         = None
        self._loop              = loop
        self._nick_name         = nick_name
        self._user_name         = user_name
        self._real_name         = real_name
        self._host_name         = host_name
        self._server_name       = server_name
        self._rcv_handler       = rcv_handler
        self._disconnect_future = Future()

    @classmethod
    def connect(cls, host='127.0.0.1', port=6667, wait=True, **kwargs):
        print_debug('Connecting to the IRC server {host}:{port}'.format(
            host=host, port=port))
        loop = get_event_loop()
        def handler():
            return cls(loop, **kwargs)
        connection  = loop.create_connection(handler, host, port)
        _, protocol = loop.run_until_complete(connection)
        if wait:
            loop.run_forever()
            loop.close()
        return protocol

    @property
    def disconnect_future(self):
        return self._disconnect_future

    def disconnect(self):
        print_debug('Disconnecting')
        self._transport.close()

    def connection_made(self, transport):
        print_debug('Made a new connection')

        self._transport = transport
        self._send_cmd(self.CMD_NICK.format(nick_name=self._nick_name))
        self._send_cmd(self.CMD_USER.format(
            user_name=self._user_name, real_name=self._real_name,
            server_name=self._server_name, host_name=self._host_name))

    def data_received(self, data):
        print_debug('Received new data:  {}'.format(data.decode()))
        if self._rcv_handler:
            self._rcv_handler(self)

    def connection_lost(self, exc):
        print_debug('Connection closed')
        self._loop.stop()
        self._disconnect_future.set_result(True)

    def _send_cmd(self, msg):
        data = '{}\r\n'.format(msg).encode()
        print_debug('Sending data: {!r}'.format(data.decode()))
        self._transport.write(data)

# ------------------------------------------------------------------------------
# vim: set filetype=python :
