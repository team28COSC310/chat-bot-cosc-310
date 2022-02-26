from response_model import ChatModel
from prepare_training_data import build_training_data
from data_importer import Intents, load_intents

import numpy as np
#Since we populated the intents file, I am now using the actual file
intents = load_intents("../intents.json")
train_x, train_y = build_training_data(intents)

chat_model = ChatModel(len(train_x[0]), len(train_y[0]))
chat_model.train(train_x, train_y, './newmodel.h5')

print(train_y[5])
print("prediction")
p = np.array(train_x[5])
#Note: originally there was 53 instead of len(p).
# However, the actual intents file has different dimensions than the test file, so I changed it to len(p) for the code to run
p = np.reshape(p, (1, len(p)))
pred = chat_model.predict(p)
print(pred)

print("New Model")
chat_model_1 = ChatModel(len(train_x[0]), len(train_y[0]))
chat_model_1.load_model_weights('./Test.h5')
pred = chat_model_1.predict(p)
print(pred)