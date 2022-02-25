from response_model import ChatModel
from prepare_training_data import build_training_data
from data_importer import Intents, load_intents

import numpy as np

intents = load_intents("./intents_test.json")
train_x, train_y = build_training_data(intents)

chat_model = ChatModel(len(train_x[0]), len(train_y[0]))
chat_model.train(train_x, train_y, './Test.h5')

print(train_y[5])
print("prediction")
p = np.array(train_x[5])
p = np.reshape(p, (1, 53))

pred = chat_model.predict(p)
print(pred)

print("New Model")
chat_model_1 = ChatModel(len(train_x[0]), len(train_y[0]))
chat_model_1.load_model_weights('./Test.h5')
pred = chat_model_1.predict(p)
print(pred)