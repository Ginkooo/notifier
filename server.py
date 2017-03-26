#!/usr/bin/python

import os
import socket
import re
import datetime

CONFIG_FILE = os.getenv('NOTIFY_CONFIG')

#Set default values
config = {
        'HOST': 'localhost',
        'PORT': 8755,
        'LOG_FILE': 'logs.txt',
        'NOTS_FILE': 'nots.txt',
        }

if not CONFIG_FILE:
    print('There is no NOTIFY_CONFIG env variable')
    exit()

def log(msg : str) -> None:
        msg = re.sub(r'[\n\r]', '', msg)
        date = datetime.datetime.now().strftime('%Y %M %D, %h:%m')
        with open(config['LOG_FILE'], 'a') as f:
            f.write(date + ' | ' + msg + os.linesep)
        print(msg)

with open(CONFIG_FILE, 'r') as f:
    for line in f.readlines():
        if line.startswith('#'):
            continue
        if not line.strip():
            continue

        rec = line.strip().split('=')
        if rec[0] == 'PORT':
            rec[1] = int(rec[1])

        config[rec[0]] = rec[1]

def log(msg : str) -> None:
        msg = re.sub(r'[\n\r]', '', msg)
        date = datetime.datetime.now().strftime('%Y/%m/%d, %H:%M')
        with open(config['LOG_FILE'], 'a') as f:
            f.write(date + ' | ' + msg + os.linesep)
        print(msg)

if not os.path.exists(config['NOTS_FILE']):
    open(config['NOTS_FILE'], 'w').close()



def handle_input(binary_data):
    text = binary_data.decode('utf-8').strip().replace('\r', '').replace('\n', '')
    if text.startswith('GET'):
        log('Getting tasks from file : ' + text)
        with open(config['NOTS_FILE'], 'r') as f:
            ret = f.read().encode('utf-8')
    elif text.startswith('CLEAR'):
        log('Erasing file contents : ' + text)
        open(config['NOTS_FILE'], 'w').close()
        ret = b''
    elif text.startswith('DEL'):
        text = text.split(' ')
        ident = text[1]
        log('Deleting tasks from ' + ident + ' : ' + text)
        with open(config['NOTS_FILE'], 'r') as f:
            lines = f.readlines()
            lines = [l for l in lines if not l.startswith(ident)]
        open(config['NOTS_FILE'], 'w').close()
        with open(config['NOTS_FILE'], 'w') as f:
            for l in lines:
                f.write(l)
        ret = b''
    else:
        log('Appending task ' + text + ' to file : ' + text)
        with open(config['NOTS_FILE'], 'a') as f:
                f.write(text + '\n')
                ret = b''
    return ret

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((config['HOST'], config['PORT']))
server_socket.listen(1)

log('Starting server on {}, port {}'.format(config['HOST'], config['PORT']))

while True:
    conn, addr = server_socket.accept()
    log('{} connected!'.format(addr))
    data = conn.recv(1024)
    if not data:
        log('something wrong with data from ' + str(conn))
    response = handle_input(data)
    try:
        log('sending ' + response)
        conn.sendall(respons)
    except:
        pass
    conn.close()
