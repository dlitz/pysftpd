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

import paramiko
import crypt

class Authorization(paramiko.ServerInterface):
    
    users = None

    def __init__(self, users, setAuthUserFunc):
        self.users = users
        self._setAuthUser = setAuthUserFunc

    def get_allowed_auths(self, username):
        return "publickey,password"

    def check_auth_none(self, username):
        if username == 'anonymous' and username in self.users and self.users[username].anonymous:
            self._setAuthUser(self.users[username])
            return paramiko.AUTH_SUCCESSFUL
        else:
            return paramiko.AUTH_FAILED

    def check_auth_password(self, username, password):
        if username == 'anonymous' and username in self.users and self.users[username].anonymous:
            # 'anonymous' user may use any password
            pass
        elif username in self.users:
            pwhash = self.users[username].password_hash
            if crypt.crypt(password, pwhash) != pwhash:
                return paramiko.AUTH_FAILED
        else:
            return paramiko.AUTH_FAILED
        self._setAuthUser(self.users[username])
        return paramiko.AUTH_SUCCESSFUL

    def check_auth_publickey(self, username, key):
        if username == 'anonymous' and username in self.users and self.users[username].anonymous:
            # 'anonymous' user may use any public key
            pass
        elif username in self.users:
            if key not in self.users[username].authorized_keys:
                return paramiko.AUTH_FAILED
        else:
            return paramiko.AUTH_FAILED
        self._setAuthUser(self.users[username])
        return paramiko.AUTH_SUCCESSFUL

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

# vim:set ts=4 sw=4 sts=4 expandtab:
