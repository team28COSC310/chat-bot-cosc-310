import socket
import sys

#connect to server
cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cli_sock.connect((sys.argv[1], int(sys.argv[2])))

while True:
    response = input(">>") 
    cli_sock.sendall(response.encode('utf-8'))
    message = cli_sock.recv(1024).decode('utf-8')
    print('Partner: ' + message)

print(out)
cli_sock.close()


