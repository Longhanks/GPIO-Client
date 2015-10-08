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
import argparse

parser = argparse.ArgumentParser(
    description='A client for GPIO-Server.')
parser.add_argument('hostname', type=str, help='The host to connect to.')
parser.add_argument('-p', '--port', type=int, default=12132,
                    help='The port to use. (default: 12132)')
parser.add_argument('-m', '--message', type=str,
                    help='Send this message and exit.')
args = parser.parse_args()

# Create a TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_list = [sys.stdin, server]

# Connect the socket to the port where the server is listening
server_address = (args.hostname, args.port)
sys.stdout.write('Connecting to %s port %s... ' % server_address)
try:
    server.connect(server_address)
except:
    print('Unable to connect.')
    sys.exit()
print('success!')

data = server.recv(4096)

if args.message:
    server.sendall(args.message)
    server.close()
    print('Message successfully sent.')
    sys.exit()

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
                print("Message must contain ASCII characters only.")
                dataStrings = data.split('\n')
                sys.stdout.write(dataStrings[-1])
                sys.stdout.flush()
            elif 'EMPTY_ERROR' in data:
                print('Empty string will be ignored.')
                dataStrings = data.split('\n')
                sys.stdout.write(dataStrings[-1])
                sys.stdout.flush()
            else:
                sys.stdout.write(data)
                sys.stdout.flush()
        else:
            try:
                msg = raw_input()
            except EOFError:
                server.close()
                print("\nConnection closed.")
                sys.exit()
            server.sendall(msg)
