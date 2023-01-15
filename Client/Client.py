import socket
#define the IP Port:
PORT = 4456

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', PORT))

option = -1

while (option != '0'):
    print("Select the option (1, 2, 3 or 0):\n(1) Upload\n(2) List\n(3) Download\n(0) Logout\n")

    option = input("What do you want to do?: ")
    #send the selected option
    client.send(option.encode())

    #OPTION (1):The Client sends a file to the Server
    if(option == '1'):
        namefile = str(input('File Name:'))
        client.send(namefile.encode())

        with open(namefile, 'rb') as file:
            for data in file.readlines():
                client.send(data)

        print('File Sent!')

        client.close()
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', PORT))

    #OPTION (2): List the files available on the Server
    elif(option == '2'):
        print('Files on the server:\n')
        while 1:
            arch = client.recv(1000000).decode()
            if not arch:
                break
            print(arch)
        print("\n")
        client.close()
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', PORT))

    #OPTION (3): The Server sends a file from the Client
    elif(option == '3'):

        namefile = str(input('File name:'))
        client.send(namefile.encode())
        with open(namefile, 'wb') as file:
            while 1:
                data = client.recv(1000000)
                if not data:
                    break
                file.write(data)
        print(f'{namefile} Received!\n')

        client.close()
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', PORT))

    elif(option == '0'):
        print('Disconnected!!')
        client.close()
