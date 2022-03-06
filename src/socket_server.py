import socket
import sys

# Create socket
srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Register the socket with the OS (defines IP and port no. of the endpoint)
srv_sock.bind(('', int(sys.argv[1])))

# Create a queue for incoming connection requests
srv_sock.listen(1)

# accept client
cli_sock, cli_addr = srv_sock.accept()

while True:
    message = cli_sock.recv(1024).decode('utf-8')
    print('Partner: ' + message)
    response = input(">>") 
    cli_sock.sendall(response.encode('utf-8'))
    
print(out)
cli_sock.close()
