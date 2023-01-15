import socket
import os
#define the IP Port:
PORT = 4456

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', PORT))
server.listen(1)
print("waiting for connection...")

while(True):
    #establishing connection with the Client
    connection, address = server.accept()
    print('\nConnected client')

    #receive the selected option
    option = connection.recv(1024).decode()

    #OPTION (1): The Server receives a file from the Client
    if(option == '1'):
        #receive the file name
        namefile = connection.recv(1024).decode()
        #save the file
        with open(namefile, 'wb') as file:
            while 1:
                data = connection.recv(1000000)
                if not data:
                    break
                file.write(data)

        print(f'{namefile} Received!\n')

    #OPTION (2): List the files available on the Server
    elif(option == '2'):
        for root, dirs, files in os.walk(".", topdown=False):
            for name in files:
                connection.send(os.path.join(root, name).encode())
            for name in dirs:
                connection.send(os.path.join(root, name).encode())

    #OPTION (3):The Server sends a file to the Client
    elif(option == '3'):
        print("Listing the Files")
        namefile = connection.recv(1024).decode()
        with open(namefile, 'rb') as file:
            for data in file.readlines():
                connection.send(data)

        print('File Sent!')
    elif(option == '0'):
        print('Client disconnected')
    connection.close()
