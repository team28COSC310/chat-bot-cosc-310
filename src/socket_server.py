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
intents = json.loads(open("../intents.json").read())

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
    response = chat.get_response(ints, intents)
    print("YouBot: " + response)
    
    cli_sock.sendall(response.encode('utf-8'))
    time.sleep(4)
    
print(out)
cli_sock.close()
