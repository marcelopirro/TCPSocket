import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 1234))

option = -1

while (option != '0'):
    print("Select the option:\n(1) Upload\n(2) Download\n(3) List\n(0)Logout\n")

    option = input("What do you want to do?: ")
    # envia p/ o servidor a opcao desejada
    client.send(option.encode())

    # cliente manda arquivo para o servidor
    if(option == '1'):
        # nome do arquivo que o cliente deseja enviar
        namefile = str(input('File Name:'))

        # envia para o servidor o nome do arquivo
        client.send(namefile.encode())

        # cliente mandando p/ servidor
        with open(namefile, 'rb') as file:
            for data in file.readlines():
                client.send(data)

        print('File Sent!')

        client.close()
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 1234))

    # requisitar lista de arquivos no repositorio
    elif(option == '2'):
        print('Files on the server\n')
        while 1:
            arch = client.recv(1000000).decode()
            if not arch:
                break
            print(arch)
        client.close()
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 1234))

    # servidor retorna um arquivo para o cliente
    elif(option == '3'):
        # nome do arquivo desejado pelo cliente
        namefile = str(input('File name:'))

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

    elif(option == '0'):
        print('Disconnected!!')
        client.close()
