import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 1234))

option = -1

while (option != '0'):
    print("Select the option:\n(1) Upload\n(2) List\n(3) Download\n(0) Logout\n")

    option = input("What do you want to do?: ")
    # envia p/ o servidor a opcao desejada
    client.send(option.encode())

    # cliente manda arquivo para o servidor
    if(option == '1'):
        namefile = str(input('File Name:'))
        client.send(namefile.encode())

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

        namefile = str(input('File name:'))
        client.send(namefile.encode())
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
