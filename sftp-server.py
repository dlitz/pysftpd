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
from sftpd.CLI import CLI

if __name__ == '__main__':
    CLI().main()

# vim:set ts=4 sw=4 sts=4 expandtab:
