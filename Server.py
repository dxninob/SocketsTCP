# Import libraries for networking communication and concurrency...
import socket
import threading
import re
import os
import datetime


# Server address and port
address, port = '127.0.0.1', 80
# Encoding format and buffer size to recive
encoding_format = "utf-8"
recv_buffer_size = 2048
# Methods where the file must exist in the server
methods_file_in_server = ['GET', 'HEAD', 'DELETE']
# Methods where the file must exist in the client
methods_file_in_client = ['POST']
# Defining the server socket object
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


def main():
    print('Server is running...')
    print('Dir IP:', address)
    print('Port:', port, '\n')
    server_execution()


#Function to start server process...
def server_execution():
    # Bind the socket to a public host, and a well-known port
    server_socket.bind((address, port))
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print ('Socket is bind to address and port...')
    # We want to queue no more than 5 connection requests before rejecting external connections
    server_socket.listen(5)
    print('Socket is listening...', '\n')
    while True:
        # The server socket accept a client connection
        client_connection, client_address = server_socket.accept()
        # We will receive multiple clients at the same time
        client_thread = threading.Thread(target=handler_client_connection, args=(client_connection,client_address))
        client_thread.start()
    print('Socket is closed...')
    # Close server socket
    server_socket.close()


# Handler for manage incomming clients conections...
def handler_client_connection(client_connection, client_address):
    print(f'New incomming connection is coming from: {client_address[0]}:{client_address[1]}', '\n')
    is_connected = True
    # Read requests from the client while it is connected
    while is_connected:
        # Read data from the client
        data_recevived = client_connection.recv(recv_buffer_size)
        # Decode the data from bytes to the encodieng format
        remote_string = str(data_recevived.decode(encoding_format))
        remote_string = remote_string.upper()
        print (f'Data received from: {client_address[0]}:{client_address[1]}')
        print(remote_string)
        # Remove newline characters from the string
        remote_string = re.sub('\n|\r', '', remote_string)
        # Separate the string into words
        remote_string = remote_string.split(' ')
        method = remote_string[0]
        
        # Execute if the method is DELETE, GET or HEAD
        if (method in methods_file_in_server):
            # The file must exist in te server to execute this methods
            success, myfile = search_file(remote_string)
            # Execute if the file exists
            if (success == 1):
                method_file_in_server(method, myfile, client_connection)
            # Return message to the client saying that the file does not exist                  
            else:
                send_header(client_connection, '404 Not Found', 0)
        # Execute if the method is POST
        elif (method in methods_file_in_client):
            success, myfile = search_file(remote_string)
            method_file_in_client(method, myfile, client_connection)
        # Stop reading data from the client if the command received is "QUIT"
        elif (method == 'QUIT'):
            send_header(client_connection, '200 BYE', 0)
            is_connected = False
        # Message the client if the command is not valid
        else:
            send_header(client_connection, '400 Bad Request', 0)
        client_connection.send('\n'.encode(encoding_format))
    # Close client connection 
    print(f'Now, client {client_address[0]}:{client_address[1]} is disconnected...')
    client_connection.close()


def search_file(remote_string):
    path = remote_string[1]
    myfile = path.split('?')[0]
    myfile = myfile.lstrip('/')
    # / means index.html
    if(myfile == ''):
        myfile = 'index.html'
    # True if file exists
    exists = os.path.exists(myfile)
    if (exists):
        # If the file exists
        return 1, myfile
    else:
        # if the file does not exist
        return 0, myfile


def method_file_in_server(method, myfile, client_connection):
    header = ''
    if (method == 'GET'):
        try:
            send_header(client_connection, '200 OK', myfile)
            client_connection.sendall('\n'.encode(encoding_format))
            # Open and read file
            f = open(myfile, 'rb')
            l = f.read(1024)
            while (l):
                # Send file bytes to the client
                client_connection.send(l)
                l = f.read(1024)
            # Close file
            f.close()
        except:
            send_header(client_connection, '500 Internal Server Error', 0)
    elif (method == 'HEAD'):
        try:
            send_header(client_connection, '200 OK', myfile)
        except:
            send_header(client_connection, '500 Internal Server Error', 0)
    elif (method == 'DELETE'):
        try:
            # Remove the file
            os.remove(myfile)
            send_header(client_connection, '200 OK', myfile)
        except:
            send_header(client_connection, '500 Internal Server Error', 0)


def method_file_in_client(method, myfile, client_connection):
    if (method == 'POST'):
        try:
            # Create new file where the data will be saved
            f = open(myfile, "w")
            # Send info to the client
            input_str = 'Ingrese END cuando quiera guardar la informacion.\n'
            client_connection.send(input_str.encode(encoding_format))
            while True:
                # Ask a variable name to the client
                input_str = 'Ingresa la variable a enviar:\n'
                client_connection.send(input_str.encode(encoding_format))
                # Read variable name
                variable = client_connection.recv(recv_buffer_size)
                variable_encoded = str(variable.decode(encoding_format))
                # Remove newline characters from the string
                variable_encoded = re.sub('\n|\r', '', variable_encoded)
                # Stop savind data if the variable is called END
                if(variable_encoded == 'END'):
                    break                
                else:
                    # Write variable in the file
                    f.write(variable_encoded + ':')
                    # Ask the value of the variable to the client
                    input_str = 'Ingresa el valor de ' + variable_encoded + ':\n'
                    client_connection.send(input_str.encode(encoding_format))
                    # Read value
                    variable = client_connection.recv(recv_buffer_size)
                    variable_encoded = str(variable.decode(encoding_format))
                    # Remove newline characters from the string
                    variable_encoded = re.sub('\n|\r', '', variable_encoded)
                    # Write newline in the file
                    f.write(variable_encoded + os.linesep)
            # Close file
            f.close()
            send_header(client_connection, '200 OK', 0)
        except:
            send_header(client_connection, '500 Internal Server Error', 0)


def send_header(client_connection, header, myfile):
    final_response = header.encode(encoding_format) + '\n'.encode(encoding_format)
    # Date and ip address and port of he server
    date = 'Date: ' + str(datetime.datetime.now()) + '\n'
    server_http = 'Server: ' + str(address) + '/' + str(port) + '\n'
    final_response += date.encode(encoding_format) + server_http.encode(encoding_format)
    # File information
    if (myfile != 0):
        content_length = 'Content-Length: ' + str(os.stat(myfile).st_size) + '\n'
        content_type = 'Content-Type: ' + file_type(myfile) + '\n'
        final_response += content_length.encode(encoding_format) + content_type.encode(encoding_format)
    client_connection.sendall(final_response)


# Return MIME type of the file
def file_type (myfile):
    if(myfile.endswith('.JPG')):
        return 'image/jpg'
    elif(myfile.endswith('.CSS')):
        return 'text/css'
    elif(myfile.endswith('.CSV')):
        return 'text/csv'
    elif(myfile.endswith('.PDF')):
        return 'application/pdf'
    elif(myfile.endswith('.DOC')):
        return 'application/msword'
    elif(myfile.endswith('.HTML')):
        return 'text/html'
    elif(myfile.endswith('.JSON')):
        return 'application/json'
    elif(myfile.endswith('.TXT')):
        return 'text/plain'
    else:
        return 'application/octet-stream'    


if __name__ == "__main__":
    main()