import socket

HOST = ''
PORT = 8757

def handle_input(binary_data):
    text = binary_data.decode('utf-8')
    print('I got ' + text)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
while True:
    conn, addr = server_socket.accept()
    print('{} connected!'.format(addr))
    data = conn.recv(1024)
    if not data:
        print('something wrong with data from ' + conn)
    handle_input(data)
    response = data + " is being processed".encode('utf-8')
    conn.sendall(response)
    conn.close()
