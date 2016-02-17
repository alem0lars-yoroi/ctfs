# IMPORTS ----------------------------------------------------------------------

import asyncio
from shared.output import *

# ------------------------------------------------------------------------------
# MODULE INFORMATIONS ----------------------------------------------------------

__all__ = ['IRCClient']

# ------------------------------------------------------------------------------
# CLIENT -----------------------------------------------------------------------

class IRCClient(asyncio.Protocol):

    CMD_NICK = 'NICK {nick}'
    CMD_USER = 'USER {user} {hostname} {servername} :{realname}'

    def __init__(self, loop, nickname, username, realname, hostname,
                 servername):
        self._transport = None
        self._loop = loop
        self._nickname = nick
        self._username = user
        self._realname = realname
        self._hostname = hostname
        self._servername = servername

    @classmethod
    def connect(self, nickname, username, realname, hostname, servername,
                host, port=6667):
        printtitle('Connecting to the IRC server {host}:{port}'.format(
            host=host, port=port))
        loop = asyncio.get_event_loop()
        def handler():
            return cls(loop, nickname, username, realname, hostname,
                       servername)
        connection = loop.create_connection(handler, host, port)
        loop.run_until_complete(connection)
        loop.run_forever()
        loop.close()

    def connection_made(self, transport):
        printtitle('Made a new connection')

        self._transport = transport
        self._send_cmd(CMD_NICK.format(nick=self._nick))
        self._send_cmd(CMD_USER.format(
            user=self._user, hostname=self._hostname,
            servername=self._servername, realname=self._realname))

    def data_received(self, data):
        printtitle('Received new data')
        printdebug('Data received:  {}'.format(data.decode()))

    def connection_lost(self, exc):
        printtitle('The server closed the connection')
        self._loop.stop()

    def _send_cmd(self, msg):
        data = '{}\r\n'.format(msg).encode()
        printdebug('Sending data: {!r}'.format(data.decode()))
        self._transport.write(data)
