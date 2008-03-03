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

import ConfigParser
import paramiko
import base64

class ConfigurationError(Exception):
    pass

class User(object):
    def __init__(self):
        self.anonymous = False
        self.password_hash = None
        self.root_path = None
        self.authorized_keys = []

class Configuration(object):

    def __init__(self, conffile_path):
        self.conffile_path = conffile_path
        self.load()

    def load(self):
        cfgSection = 'pysftpd'
        
        # Read the main configuration file
        config = ConfigParser.RawConfigParser()
        if not config.read(self.conffile_path):
            raise ConfigurationError("Unable to load configuration file %r" % (self.conffile_path,))

        # Read bind address
        listen_host = config.get(cfgSection, 'listen_host')
        listen_port = config.getint(cfgSection, 'listen_port')
        self.bind_address = (listen_host, listen_port)

        # Load host keys
        host_keys = []
        for optname in config.options(cfgSection):
            if optname != "host_key" and not optname.startswith("host_key."):
                continue
            filename = config.get(cfgSection, optname)
            try:
                host_key = paramiko.RSAKey.from_private_key_file(filename=filename)
            except paramiko.SSHException:
                host_key = paramiko.DSSKey.from_private_key_file(filename=filename)
            host_keys.append(host_key)
            host_key = None # erase reference to host key
        if not host_keys:
            raise ConfigurationError("config file %r does not specify any host key" % (self.conffile_path,))
        self.host_keys = host_keys

        # Load the user auth file (authconfig.ini)
        auth_config = ConfigParser.RawConfigParser()
        auth_config.read(config.get(cfgSection, 'auth_config'))
        users = {}
        for username in auth_config.sections():
            u = User()
            if auth_config.has_option(username, 'anonymous'):
                u.anonymous = auth_config.getboolean(username, 'anonymous')
            if not u.anonymous:
                u.password_hash = auth_config.get(username, 'password')
            u.root_path = auth_config.get(username, 'root_path')
            
            # TODO: Move authorized_keys parsing into a separate function
            u.authorized_keys = []
            if auth_config.has_option(username, 'authorized_keys_file'):
                filename = auth_config.get(username, 'authorized_keys_file')
                for rawline in open(filename, 'r'):
                    line = rawline.strip()
                    if not line or line.startswith("#"):
                        continue
                    if line.startswith("ssh-rsa ") or line.startswith("ssh-dss "):
                        # Get the key field
                        try:
                            d = " ".join(line.split(" ")[1:]).lstrip().split(" ")[0]
                        except:
                            # Parse error
                            continue
                        if line.startswith("ssh-rsa"):
                            k = paramiko.RSAKey(data=base64.decodestring(d))
                        else:
                            k = paramiko.DSSKey(data=base64.decodestring(d))
                        del d
                        u.authorized_keys.append(k)
            users[username] = u
        self.users = users

# vim:set ts=4 sw=4 sts=4 expandtab:
