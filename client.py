#!/usr/bin/env python
# GPIO-Client. Created on 07.10.2015
# Copyright (C) 2014 Andreas Schulz <andreas.schulz@frm2.tum.de>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 US

import socket
import sys
import select

# Create a TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_list = [sys.stdin, server]
if (len(sys.argv) < 3):
    print("Usage: client.py <hostname> <port>")
    sys.exit()

# Connect the socket to the port where the server is listening
server_address = (sys.argv[1], int(sys.argv[2]))
sys.stdout.write('Connecting to %s port %s... ' % server_address)
try:
    server.connect(server_address)
except:
    print('Unable to connect.')
    sys.exit()
print('success!')

data = server.recv(4096)
sys.stdout.write(data)
sys.stdout.flush()

while True:
    # Get the list sockets which are readable
    read_sockets, write_sockets, error_sockets = select.select(
        socket_list, [], [])

    for sock in read_sockets:
        # incoming message from remote server
        if sock == server:
            data = sock.recv(4096)
            if not data:
                print('\nConnection was closed by server.')
                sys.exit()
            elif 'ASCII_ERROR' in data:
                dataStrings = data.split('\n')
                print("Message must contain ASCII characters only.")
                sys.stdout.write(dataStrings[-1])
                sys.stdout.flush()
            else:
                sys.stdout.write(data)
                sys.stdout.flush()
        else:
            msg = sys.stdin.readline()
            server.sendall(msg)
