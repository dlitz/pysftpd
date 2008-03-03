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
import os
import stat
import posixpath
import sys

class SFTPServerInterface(paramiko.SFTPServerInterface):
    
    def __init__(self, server, getUserFunc):
        self._base_dir = getUserFunc().root_path

    def _local_path(self, sftp_path):
        """Return the local path given an SFTP path.  Raise an exception if the path is illegal."""
        if sys.platform == 'win32':
            # We would need to check for illegal characters, special filenames like 
            # PRN.txt and AUX, and then convert to unicode (for NTFS).
            # See "Naming a File" <http://msdn2.microsoft.com/en-us/library/aa365247.aspx>
            raise NotImplementedError("Win32 path sanitization not implemented")
        absBasePath = os.path.abspath(self._base_dir)
        if not sftp_path.startswith("/"):
            raise ValueError("Invalid SFTP path %r" % sftp_path)
        sp = posixpath.normpath(sftp_path)
        sp = sp.lstrip("/")
        assert('..' not in posixpath.split(sp))
        lp = os.path.abspath(os.path.join(self._base_dir, sp))
        assert(os.path.commonprefix((absBasePath, lp)) == absBasePath)
        return lp

    def list_folder(self, sftp_path):
        local_path = self._local_path(sftp_path)
        retval = []
        for filename in os.listdir(local_path):
            lpf = os.path.join(local_path, filename)
            retval.append(paramiko.SFTPAttributes.from_stat(os.lstat(lpf), filename))
        return retval

    def stat(self, sftp_path):
        local_path = self._local_path(sftp_path)
        filename = os.path.basename(local_path)
        return paramiko.SFTPAttributes.from_stat(os.stat(local_path), filename)

    def lstat(self, sftp_path):
        local_path = self._local_path(sftp_path)
        filename = os.path.basename(local_path)
        return paramiko.SFTPAttributes.from_stat(os.lstat(local_path), filename)

    def open(self, sftp_path, flags, attr):
        local_path = self._local_path(sftp_path)
        if (flags & os.O_WRONLY) or (flags & os.O_RDWR):
            return paramiko.SFTP_PERMISSION_DENIED
        h = paramiko.SFTPHandle()
        h.readfile = open(local_path, "rb")
        return h

# vim:set ts=4 sw=4 sts=4 expandtab:
