import socket
import os

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 1234))
server.listen(1)
print("waiting for connection...")

while(True):
    # conexao com o cliente
    connection, address = server.accept()
    print('\nConnected client')

    # recebe a opcao desejada do cliente
    option = connection.recv(1024).decode()

    # recebe um arquivo enviado pelo cliente
    if(option == '1'):
        namefile = connection.recv(1024).decode()

        with open(namefile, 'wb') as file:
            while 1:
                data = connection.recv(1000000)
                if not data:
                    break
                file.write(data)

        print(f'{namefile} Received!\n')

    # lista os arquivos disponiveis
    elif(option == '2'):
        for root, dirs, files in os.walk(".", topdown=False):
            for name in files:
                connection.send(os.path.join(root, name).encode())
            for name in dirs:
                connection.send(os.path.join(root, name).encode())

    # envia um arquivo solicitado pelo cliente
    elif(option == '3'):
        namefile = connection.recv(1024).decode()
        with open(namefile, 'rb') as file:
            for data in file.readlines():
                connection.send(data)

        print('File Sent!')
    elif(option == '0'):
        print('Client disconnected')
    connection.close()
