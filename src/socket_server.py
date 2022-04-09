import socket
import sys
import json
import time

from chatbot import Chat
from NER_func import find_NER

chat = Chat()
with open("../intents.json") as file:
    intents = json.loads(file.read())

print("Ready to Chat")

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
    print('ChatBot: ' + message)
    
    ints = chat.predict_class(message)
    ents = find_NER(message)
    response = chat.get_response(ints, intents, ents, message)
    print("YouBot: " + response)
    
    cli_sock.sendall(response.encode('utf-8'))
    time.sleep(4)
