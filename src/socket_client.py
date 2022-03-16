import socket
import sys
import json
import time

from chatbot import Chat
from NER_func import find_NER

chat = Chat()

print("Ready to Chat")
with open("../intents.json") as file:
    intents = json.loads(file.read())

# connect to server
cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cli_sock.connect((sys.argv[1], int(sys.argv[2])))

response = input("Conversation starter: ")
cli_sock.sendall(response.encode('utf-8'))

while True:
    message = cli_sock.recv(1024).decode('utf-8')
    print('ChatBot: ' + message)

    ints = chat.predict_class(message)
    ents = find_NER(message)
    response = chat.get_response(ints, intents, ents)
    print("YouBot: " + response)

    cli_sock.sendall(response.encode('utf-8'))
    time.sleep(4)
