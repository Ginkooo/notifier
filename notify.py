#!/usr/bin/python

import subprocess
import sys
import os

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
            PORT = c[1]
        if c[0] == 'HOST':
            HOST = c[1]

cmd = ['echo'] + sys.argv[1:]

sys.stdout.flush()

echo = subprocess.Popen(cmd, stdout=subprocess.PIPE)

if echo.wait() != 0:
    print('Something is wrong with echo')
    exit()

nc = subprocess.Popen(['nc', HOST, PORT], stdin=echo.stdout)
