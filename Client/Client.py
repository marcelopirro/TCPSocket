import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 1234))

op = -1

while (op != '0'):
    print('Escolha uma das opcoes do menu:\n')
    print('1- requisitar o armazenamento de um arquivo.\n')
    print('2- requisitar a lista de arquivos disponiveis.\n')
    print('3- requisitar um dos arquivos armazenados.\n')
    print('0- sair\n')

    op = input('Digite a opcao desejada: ')
    # envia p/ o servidor a opcao desejada
    client.send(op.encode())

    # cliente manda arquivo para o servidor
    if(op == '1'):
        # nome do arquivo que o cliente deseja enviar
        namefile = str(input('Arquivo:'))

        # envia para o servidor o nome do arquivo
        client.send(namefile.encode())

        # cliente mandando p/ servidor
        with open(namefile, 'rb') as file:
            for data in file.readlines():
                client.send(data)

        print('Arquivo enviado para o servidor')

        client.close()
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 1234))

    # requisitar lista de arquivos no repositorio
    elif(op == '2'):
        print('Lista de arquivos disponiveis no servidor:\n')
        while 1:
            arqui = client.recv(1000000).decode()
            if not arqui:
                break
            print(arqui)
        client.close()
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 1234))

    # servidor retorna um arquivo para o cliente
    elif(op == '3'):
        # nome do arquivo desejado pelo cliente
        namefile = str(input('Arquivo:'))

        # envia o nome do arquivo para o servidor
        client.send(namefile.encode())

        # cliente recebe o arquivo do servidor
        with open(namefile, 'wb') as file:
            while 1:
                data = client.recv(1000000)
                if not data:
                    break
                file.write(data)
        print(f'{namefile} recebido\n')

        client.close()
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 1234))

    elif(op == '0'):
        print('cliente desconectado')
        client.close()
