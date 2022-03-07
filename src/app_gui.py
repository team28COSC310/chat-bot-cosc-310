"""
Graphical User Interface for COSC 310 Chat Bot

Created by:
Nicholas Brown, Jonathan Chou, Omar Ishtaiwi, Niklas Tecklenburg and Elizaveta Zhukova

Acknowledgments:
The gui is mostly based on a tutorial from Youtube: https://youtu.be/RNEcewpVZUQ
"""
from tkinter import *
from tkinter import scrolledtext  # scrolledtext widget only works if implemented explicitly
from chatbot import get_response, predict_class  # the functions needed to generate bot's response
from PIL import Image, ImageTk
import json

# all colors used in the gui
BLACK = "#151515"
WHITE = "#FFFFFF"
DARK_BLUE = "#002145"
LIGHT_BLUE = "#A4C3E4"
LIGHT_GRAY = "#EEEEEE"

# All fonts used in the gui
FONT_HIGHLIGHT = ("Roboto", 14, "bold")
FONT_MAIN = ("Roboto", 14)

# Intents file, for bot to retrieve answers from it
INTENTS = json.loads(open("../intents.json").read())


class ChatApplication:
    '''
    Create GUI interface for chatbot
    '''

    def __init__(self):
        '''
        Build and setup the interface window
        '''
        self.window = Tk()
        self._setup_main_window()

    def run(self):
        '''
        Run the bot in a separate window with gui
        '''
        self.window.mainloop()

    def _setup_main_window(self):
        '''
        Setup the graphical elements of gui, such as:
        The head label with the name of chatbot, UBCO logo, and a separator
        The area for a chat with a bot with a scrollbar
        The area for entering the questions to a bot, with the "send" button
        '''
        self.window.title("Chatbot UBCO")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=470, height=550, bg=WHITE)

        # head content
        self.head_label = Label(self.window, bg=WHITE, fg=DARK_BLUE,
                                text="UBCO chatbot", font=FONT_HIGHLIGHT, pady=10)
        self.head_label.place(relwidth=1)

        # ubco logo
        ubco_logo = ImageTk.PhotoImage(Image.open("images/UBC-logo-transparent.png").resize((26, 35)))
        logo_label = Label(self.head_label, bg=WHITE, image=ubco_logo)
        logo_label.image = ubco_logo
        logo_label.place(relwidth=0.07, relheight=0.9)

        # separator line
        separator = Label(self.window, width=450, bg=DARK_BLUE)
        separator.place(relwidth=1, rely=0.07, relheight=0.01)

        # text widget for a chat with the bot
        self.chat_area = scrolledtext.ScrolledText(self.window, width=20, height=2, bg=WHITE, fg=BLACK,
                                                   font=FONT_MAIN, padx=5, pady=8, wrap=WORD)
        self.chat_area.place(relheight=0.745, relwidth=1, rely=0.08)
        self.chat_area.configure(cursor="arrow", state=DISABLED)

        # bottom label
        bottom_label = Label(self.window, bg=DARK_BLUE, height=80)
        bottom_label.place(relwidth=1, rely=0.825)

        # input box for the user
        self.input_entry = Entry(bottom_label, bg=LIGHT_GRAY, fg=BLACK, font=FONT_MAIN)
        self.input_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.input_entry.focus()
        self.input_entry.bind("<Return>", self._on_enter_pressed)

        # send button
        send_button = Button(bottom_label, text="Send", font=FONT_HIGHLIGHT, width=20, bg=LIGHT_BLUE,
                             command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.77, rely=0.018, relheight=0.04, relwidth=0.22)

    def _on_enter_pressed(self, event):
        '''
        Then the user enters the message, get their message and display the question and answer in the chat area
        '''
        msg = self.input_entry.get()
        self._insert_message(msg)

    def _insert_message(self, msg):
        '''
        Adds 2 new messages to the chat area:
        1 for the question the user sent and the second is for the answer the bot gave
        '''
        if not msg:
            return

        self.input_entry.delete(0, END)

        msg1 = f"You: {msg}\n\n"
        self.chat_area.configure(state=NORMAL)
        self.chat_area.insert(END, msg1)
        self.chat_area.configure(state=DISABLED)

        msg2 = f"UBCO: {get_response(predict_class(msg), INTENTS)}\n\n"
        self.chat_area.configure(state=NORMAL)
        self.chat_area.insert(END, msg2)
        self.chat_area.configure(state=DISABLED)

        self.chat_area.see(END)


if __name__ == "__main__":
    app_gui = ChatApplication()
    app_gui.run()
