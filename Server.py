# ********************************************************************************************
    # Lab: Introduction to sockets
    # Course: ST0255 - Telemática
    # MultiThread TCP-SocketServer
# ********************************************************************************************

# Import libraries for networking communication and concurrency...

import socket
import threading
import re
import os


# Server address and port
address, port = '127.0.0.1', 80
encoding_format = "utf-8"
recv_buffer_size = 2048
methods = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']

# Defining a socket object...
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


def main():
    print('Server is running...')
    print('Dir IP:', address)
    print('Port:', port, '\n')
    server_execution()


#Function to start server process...
def server_execution():
    server_socket.bind((address, port))
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print ('Socket is bind to address and port...')
    server_socket.listen(5)
    print('Socket is listening...', '\n')
    while True:
        client_connection, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handler_client_connection, args=(client_connection,client_address))
        client_thread.start()
    print('Socket is closed...')
    server_socket.close()


# Handler for manage incomming clients conections...
def handler_client_connection(client_connection,client_address):
    print(f'New incomming connection is coming from: {client_address[0]}:{client_address[1]}', '\n')
    is_connected = True
    while is_connected:
        data_recevived = client_connection.recv(recv_buffer_size)
        remote_string = str(data_recevived.decode(encoding_format))
        print (f'Data received from: {client_address[0]}:{client_address[1]}')
        print(remote_string)
        remote_string = re.sub('\n|\r', '', remote_string)
        remote_string = remote_string.split(' ')
        method = remote_string[0]
        
        if (method in methods):
            success, myfile = search_file(remote_string)
            if (success == 1):
                select_method(method, myfile, client_connection)                    
            else:
                header = 'HTTP/1.1 404 Not Found\n'
                response = '<html><body>Error 404: File not found</body></html>'.encode(encoding_format)
                final_response = header.encode(encoding_format)
                final_response += response + '\n'.encode(encoding_format)
                client_connection.sendall(final_response)
            
        elif (method == 'QUIT'):
            response = '200 BYE\n'
            client_connection.sendall(response.encode(encoding_format))
            is_connected = False

        else:
            response = '400 Bad Request\n'
            client_connection.sendall(response.encode(encoding_format))

        client_connection.send('\n'.encode(encoding_format))

    print(f'Now, client {client_address[0]}:{client_address[1]} is disconnected...')
    client_connection.close()


def search_file(remote_string):
    path = remote_string[1]
    myfile = path.split('?')[0]
    myfile = myfile.lstrip('/')
    if(myfile == ''):
        myfile = 'index.html'
    exists = os.path.exists(myfile)
    if (exists):
        return 1, myfile
    else:
        return 0, 0


def select_method(method, myfile, client_connection):
    header = ''
    if (method == 'GET'):
        try:
            header = '200 OK\n'
            final_response = header.encode(encoding_format) + '\n'.encode(encoding_format)
            client_connection.sendall(final_response)
            f = open(myfile, 'rb')
            l = f.read(1024)
            while (l):
                client_connection.send(l)
                l = f.read(1024)
            f.close()
        except:
            header = '500 Internal Server Error\n'
    elif (method == 'HEAD'):
        pass
    elif (method == 'POST'):
        pass
    elif (method == 'PUT'):
        pass
    elif (method == 'DELETE'):
        try:
            os.remove(myfile)
            header = '200 OK\n'
        except ValueError:
            header = '500 Internal Server Error\n'
    elif (method == 'CONNECT'):
        pass
    elif (method == 'OPTIONS'):
        pass
    elif (method == 'TRACE'):
        pass
    elif (method == 'PATCH'):
        pass
    return header


if __name__ == "__main__":
    main()