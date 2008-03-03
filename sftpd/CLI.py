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

import optparse
import sys
import os
import logging
import pwd
import grp
import paramiko
from SFTPServer import SFTPServer
from Configuration import Configuration

class CLI(object):
    
    def parse_args(self):
        # Defaults
        defaults = {}
        defaults['config'] = "/etc/pysftpd/pysftpd.ini"

        # Parse options
        op = optparse.OptionParser(usage="Usage: %s [opts]")
        op.add_option("-c", "--config", metavar="FILE",
            dest="config", default=defaults['config'],
            help="load program configuration from FILE (default: %s)" % (defaults['config'],))
        op.add_option("--user", metavar="NAME",
            dest="user",
            help="setuid to this user before accepting connections")
        op.add_option("--group", metavar="NAME",
            dest="group",
            help="setgid to this group before accepting connections")
        op.add_option("--chroot", metavar="PATH",
            dest="chroot",
            help="[experimental] chroot to PATH before accepting connections (requires --user and --group; don't forget to close open file descriptors!)")
        op.add_option("-v", "--verbose", metavar="FILE",
            dest="verbosity", action="count", default=0,
            help="verbose operation (multiple -v options allowed)")
        
        (options, args) = op.parse_args()
        if len(args) != 0:
            print >>sys.stderr, "%s: error: invalid arguments" % (sys.argv[0],)
            sys.exit(1)

        if options.chroot and (not options.user or not options.group):
            print >>sys.stderr, "%s: error: --chroot requires --user and --group" % (sys.argv[0],)
            sys.exit(1)

        return options

    def main(self):
        options = self.parse_args()
     
        # Log verbosity
        if options.verbosity == 0:
            logging.basicConfig(level=logging.ERROR)
        elif options.verbosity == 1:
            logging.basicConfig(level=logging.INFO)
        elif options.verbosity >= 2:
            logging.basicConfig(level=logging.DEBUG)
        
        config = Configuration(options.config)

        server = SFTPServer(config.bind_address, config=config)
        if options.chroot:
            uid = pwd.getpwnam(options.user)[2]
            gid = grp.getgrnam(options.group)[2]

            # TODO: Audit this
            os.chroot(options.chroot)
            os.setgroups([])    # Drop supplemental group privileges
            os.setgid(gid)
            os.setuid(uid)
        server.serve_forever()


# vim:set ts=4 sw=4 sts=4 expandtab:
