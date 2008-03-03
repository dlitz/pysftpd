#!/usr/bin/python -tt
# -*- coding: ascii -*-
# Copyright (c) 2008  Dwayne C. Litzenberger <dlitz@dlitz.net>
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

from distutils.core import setup

setup(
    name='PySFTPd',
    version='0.1.0',    # don't forget to update download_url and "Development Status" below
    download_url='https://secure.dlitz.net/pub/dlitz/python/pysftpd/PySFTPd-0.1.0.tar.gz',
    requires=['paramiko (>=1.7.2)'],
    description='SFTP daemon',
    long_description="PySFTPd is an SFTP server implementation that builds upon the paramiko secure shell library.",
    author='Dwayne C. Litzenberger',
    author_email='dlitz@dlitz.net',
    url='http://www.dlitz.net/software/pysftpd/',
    packages=['sftpd'],
    license='GNU General Public License (GPL) >= 3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Internet',
        'Topic :: Security :: Cryptography',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX :: Linux',
    ],
)

# vim:set ts=4 sw=4 sts=4 expandtab:
