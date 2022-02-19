"""
COSC 310 Chat Bot

Created by:
Nicholas Brown, Jonathan Chou, Omar Ishtaiwi, Niklas Tecklenburg and Elizaveta Zhukova
"""

import data_importer


intents = data_importer.load_intents("")
print(intents.documents)
