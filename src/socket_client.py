import socket
import sys
import pickle
import json
import time

from chatbot import predict_class, get_response
from response_model import ChatModel
from prepare_training_data import build_training_data
from data_importer import Intents, load_intents

intents = load_intents("../intents.json")
train_x, train_y = build_training_data(intents)

chat_model = ChatModel(len(train_x[0]), len(train_y[0]))

words = pickle.load(open("words.pkl", "rb"))
classes = pickle.load(open("classes.pkl", "rb"))

# Load the Chatbot model, if there are no weights available, train the model
try:
    chat_model.load_model_weights('./model_weights/weights.h5')
except:
    chat_model.train(train_x, train_y, './model_weights/weights.h5')

intents = json.loads(open("../intents.json").read())

print("Ready to Chat")


#connect to server
cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cli_sock.connect((sys.argv[1], int(sys.argv[2])))

response = input("Conversation starter: ")
cli_sock.sendall(response.encode('utf-8'))

while True:
    message = cli_sock.recv(1024).decode('utf-8')
    print('ChatBot: ' + message)
    
    ints = predict_class(message)
    response = get_response(ints, intents)
    print("YouBot: " + response)
    
    cli_sock.sendall(response.encode('utf-8'))
    time.sleep(4)

print(out)
cli_sock.close()


