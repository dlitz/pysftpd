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

import sys
import os
import paramiko

rsa_bits = 3072
dss_bits = 1024

rsa_key_filename = "server_rsa_key"
dss_key_filename = "server_dss_key"

def show_progress(s):
    sys.stdout.write("... " + s)
    sys.stdout.flush()

def main():
    status = 0

    if os.path.exists(rsa_key_filename):
        print >>sys.stderr, "%s already exists.  Not generating RSA host key." % (rsa_key_filename,)
        status = 2
    elif os.path.exists(rsa_key_filename + ".pub"):
        print >>sys.stderr, "%s already exists.  Not generating RSA host key." % (rsa_key_filename + ".pub",)
        status = 2
    else:
        print "Generating %d-bit RSA host key..." % (rsa_bits,)
        rsa_key = paramiko.RSAKey.generate(bits=rsa_bits, progress_func=show_progress)
        print "... Writing %s" % (rsa_key_filename,)
        rsa_key.write_private_key_file(rsa_key_filename)
        print "... Writing %s" % (rsa_key_filename + ".pub",)
        open(rsa_key_filename + ".pub", "w").write("%s %s\n" % (rsa_key.get_name(), rsa_key.get_base64()))
        del rsa_key
        print "... done!"

    if os.path.exists(dss_key_filename):
        print >>sys.stderr, "%s already exists.  Not generating DSS host key." % (dss_key_filename,)
        status = 2
    elif os.path.exists(dss_key_filename + ".pub"):
        print >>sys.stderr, "%s already exists.  Not generating DSS host key." % (dss_key_filename + ".pub",)
        status = 2
    else:
        print "Generating %d-bit RSA host key..." % (dss_bits,)
        dss_key = paramiko.DSSKey.generate(bits=dss_bits, progress_func=show_progress)
        print "... Writing %s" % (dss_key_filename,)
        dss_key.write_private_key_file(dss_key_filename)
        print "... Writing %s" % (dss_key_filename + ".pub",)
        open(dss_key_filename + ".pub", "w").write("%s %s\n" % (dss_key.get_name(), dss_key.get_base64()))
        del dss_key
        print "... done!"

    sys.exit(status)

if __name__ == '__main__':
    main()

# vim:set ts=4 sw=4 sts=4 expandtab:
