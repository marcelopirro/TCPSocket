import socket
import os

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# servidor ouvindo a porta 1234
server.bind(('localhost', 1234))
server.listen(1)

while(1):
    # conexao com o cliente
    connection, address = server.accept()
    print('\nCliente conectado')

    # recebe a opcao desejada do cliente
    op = connection.recv(1024).decode()

    # recebe um arquivo enviado pelo cliente
    if(op == '1'):
        # recebe o nome do arquivo que sera enviado pelo cliente
        namefile = connection.recv(1024).decode()

        # servidor recebe o arquivo do cliente
        with open(namefile, 'wb') as file:
            while 1:
                data = connection.recv(1000000)
                if not data:
                    break
                file.write(data)

        print(f'{namefile} recebido\n')

    # lista os arquivos disponiveis
    elif(op == '2'):
        print('Enviando lista de arquivos...')
        for root, dirs, files in os.walk(".", topdown=False):
            for name in files:
                connection.send(os.path.join(root, name).encode())
            for name in dirs:
                connection.send(os.path.join(root, name).encode())

    # envia um arquivo solicitado pelo cliente
    elif(op == '3'):
        # recebe o nome do arquivo requisitado pelo cliente
        namefile = connection.recv(1024).decode()

        # servidor mandando p/ cliente
        with open(namefile, 'rb') as file:
            for data in file.readlines():
                connection.send(data)

        print('Arquivo enviado para o cliente')
    elif(op == '0'):
        print('Cliente desconectado')
    connection.close()
