import socket
import sys
import pickle
import json
import time

from chatbot import Chat
from response_model import ChatModel
from prepare_training_data import build_training_data
from data_importer import Intents, load_intents

chat = Chat()

print("Ready to Chat")
intents = json.loads(open("../intents.json").read())

#connect to server
cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cli_sock.connect((sys.argv[1], int(sys.argv[2])))

response = input("Conversation starter: ")
cli_sock.sendall(response.encode('utf-8'))

while True:
    message = cli_sock.recv(1024).decode('utf-8')
    print('ChatBot: ' + message)
    
    ints = chat.predict_class(message)
    response = chat.get_response(ints, intents)
    print("YouBot: " + response)
    
    cli_sock.sendall(response.encode('utf-8'))
    time.sleep(4)

print(out)
cli_sock.close()


