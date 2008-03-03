#!/usr/bin/python -tt
# -*- coding: ascii -*-
# Copyright (c) 2007, 2008  Dwayne C. Litzenberger <dlitz@dlitz.net>
# 
# This file is part of PySFTPd.
#
# PySFTPd is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# PySFTPd is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import SocketServer
from SFTPServerInterface import SFTPServerInterface
from Authorization import Authorization
from errors import ProtocolError
import paramiko

class SFTPServer(SocketServer.TCPServer):
    
    def __init__(self, server_address, config, RequestHandlerClass=None):
        if RequestHandlerClass is None:
            RequestHandlerClass = SFTPConnectionRequestHandler
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)
        
        # These attributes will be accessed by the RequestHandlerClass
        self.users = config.users
        self.host_keys = config.host_keys


class SFTPConnectionRequestHandler(SocketServer.BaseRequestHandler):
    
    auth_timeout = 120  # authentication timeout (in seconds)

    def setup(self):
        self.transport = self.make_transport(self.request)
        self.load_server_moduli()
        self.set_security_options()
        self.add_host_keys()
        self.set_subsystem_handlers()

    def handle(self):
        srvIface = Authorization(self.server.users, self._set_authenticated_user)
        self.transport.start_server(server=srvIface)
        # Get the session channel
        chan = self.transport.accept(self.auth_timeout)
        if chan is None:
            raise ProtocolError("session channel not opened (authentication failure?)")
        self.transport.join()

    def _set_authenticated_user(self, user):
        self._auth_user = user
    
    def _get_authenticated_user(self):
        return self._auth_user

    def make_transport(self, sock):
        return paramiko.Transport(sock)

    def load_server_moduli(self):
        self.transport.load_server_moduli()

    def set_security_options(self):
        so = self.transport.get_security_options()

        # Don't support any of (hmac-sha1-96, hmac-md5, hmac-md5-96, none)
        so.digests = ('hmac-sha1',)
   
        # Support delayed zlib compression, but not 'zlib' compression.
        # 'zlib@openssh.com' does the same thing as 'zlib', but avoids attacks
        # by unauthenticated users.
        so.compression = ('zlib@openssh.com', 'none')
        
    def add_host_keys(self):
        for key in self.server.host_keys:
            self.transport.add_server_key(key)

    def set_subsystem_handlers(self):
        self.transport.set_subsystem_handler('sftp', paramiko.SFTPServer,
            sftp_si=SFTPServerInterface, getUserFunc=self._get_authenticated_user)


# vim:set ts=4 sw=4 sts=4 expandtab:
