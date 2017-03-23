#!/usr/bin/python

import subprocess
import sys
import os
import socket
from socket import AF_INET, SOCK_STREAM

CONFIG_FILE = os.getenv('NOTIFY_CONFIG')


if not CONFIG_FILE:
    print('You have no NOTIFY_CONFIG env variable set')
    exit()

if len(sys.argv) not in range(2, 4):
    print('Too few arguments')
    exit()

with open(CONFIG_FILE, 'r') as f:
    for line in f.readlines():
        c = line.strip().split('=')
        if c[0] == 'PORT':
            PORT = int(c[1])
        if c[0] == 'HOST':
            HOST = c[1]

print (HOST, PORT)

def send_message(msg, host, port):
    sock = socket.socket(AF_INET, SOCK_STREAM)
    sock.connect((host, port))
    sock.sendall(msg)

def send_and_recv(msg):
    sock = socket.socket(AF_INET, SOCK_STREAM)
    sock.connect((HOST, PORT))
    sock.sendall(msg)
    resp = sock.recv(1024)
    return resp


msg = ' '.join(sys.argv[1:])

print(msg)

sys.stdout.flush()

if msg == b'GET':
    resp = send_and_recv(msg)
    print(resp)
    quit()

send_message(msg, HOST, PORT)
