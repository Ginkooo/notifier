#!/usr/bin/python

import os
import socket

HOST = ''
PORT = 8755

FILEPATH = '/home/ginko/.nots'

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
