import socket
import threading


def http_response(connection_socket):
    request = connection_socket.recv(buffer_size).decode('ascii')

    # parse http request to get file name
    request = request.split('\n')
    request_line = request[0]
    request_line = request_line.split(' ')
    file_name = request_line[1]

    # now have the file name, can find and send the file
    file_name = 'content' + file_name
    try:
        response = "HTTP/1.1 200 OK\r\n" \
                   "\r\n"

        with open(file_name, 'rb') as f:
            file = f.read()
            response = response.encode() + file
            connection_socket.send(response)

    except FileNotFoundError:
        response = "HTTP/1.1 404 Not Found\r\n"
        response = response.encode()
        connection_socket.send(response)

    connection_socket.close()


server_ip = 'localhost'
server_port = 8907
buffer_size = 1024

welcome_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
welcome_socket.bind((server_ip, server_port))

welcome_socket.listen()

print('The server is ready to receive')

while True:
    connection_socket, addr = welcome_socket.accept()
    threading.Thread(target=http_response, args=(connection_socket,)).start()
