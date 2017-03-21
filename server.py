#!/usr/bin/python

import os
import socket

FILEPATH = 'nots.txt'
if not os.path.exists(FILEPATH):
    open(FILEPATH, 'w').close()

CONFIG_FILE = os.getenv('NOTIFY_CONFIG')

if not CONFIG_FILE:
    print('There is no NOTIFY_CONFIG env variable')
    exit()

with open(CONFIG_FILE, 'r') as f:
    for line in f.readlines():
        rec = line.strip().split('=')
        if rec[0] == 'PORT':
            PORT = int(rec[1])
        if rec[0] == 'HOST':
            HOST = rec[1]


def handle_input(binary_data):
    text = binary_data.decode('utf-8').strip().replace('\r', '').replace('\n', '')
    if text.startswith('GET'):
        print('getting tasks from file')
        with open(FILEPATH, 'r') as f:
            ret = f.read().encode('utf-8')
    elif text.startswith('CLEAR'):
        print('Erasing file contents')
        open(FILEPATH, 'w').close()
        ret = b''
    elif text.startswith('DEL'):
        text = text.split(' ')
        ident = text[1]
        print('Deleting tasks from ' + ident)
        with open(FILEPATH, 'r') as f:
            lines = f.readlines()
            lines = [l for l in lines if not l.startswith(ident)]
        open(FILEPATH, 'w').close()
        with open(FILEPATH, 'w') as f:
            for l in lines:
                f.write(l)
        ret = b''
    else:
        print('appending task ' + binary_data.decode('utf-8') + 'to file')
        with open(FILEPATH, 'a') as f:
                f.write(text + '\n')
                ret = b''
    return ret

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
while True:
    conn, addr = server_socket.accept()
    print('{} connected!'.format(addr))
    data = conn.recv(1024)
    if not data:
        print('something wrong with data from ' + str(conn))
    response = handle_input(data)
    try:
        conn.sendall(response)
    except:
        pass
    conn.close()
