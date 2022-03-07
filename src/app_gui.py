"""
Graphical User Interface for COSC 310 Chat Bot

Created by:
Nicholas Brown, Jonathan Chou, Omar Ishtaiwi, Niklas Tecklenburg and Elizaveta Zhukova

Acknowledgments:
The gui is mostly based on a tutorial from Youtube: https://youtu.be/RNEcewpVZUQ
"""
from tkinter import *
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

# an array to guarantee proper alignment of responses
DIAL_TAG = []


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

        # chat area (with a scrollbar) for a chat with the bot
        self.chat_area = Canvas(self.window, width=20, height=2, bg=WHITE, takefocus=1)
        self.chat_area.place(relheight=0.745, relwidth=1, rely=0.08)
        scrollbar = Scrollbar(self.chat_area)
        scrollbar.place(relheight=1, relx=0.96)
        scrollbar.configure(command=self.chat_area.yview)
        self.chat_area.configure(yscrollcommand=scrollbar.set)
        self.chat_area.bind_all("<MouseWheel>", self._on_mousewheel) #ensures what the scrollbar can be moved with a mouse wheel

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

    def _on_mousewheel(self, event):
        '''
        Sets the Canvas yview_scroll parameter such that the Scrollbar attached to Canvas can be moved by the mouse wheel.
        This solution is retrieved from: https://stackoverflow.com/questions/17355902/tkinter-binding-mousewheel-to-scrollbar
        The solution works for Windows machines and is not guaranteed to work for other machines
        '''
        self.chat_area.yview_scroll(int(-1 * (event.delta / 120)), "units")

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

        msg1 = f"{msg}"
        msg2 = f"{get_response(predict_class(msg), INTENTS)}"
        if not DIAL_TAG:
            y_coord_1 = 0
        else:
            y_coord_1 = self.chat_area.bbox(DIAL_TAG[0])[3]
        user_text = self.chat_area.create_text(430, y_coord_1+34, text=msg1, anchor='ne', fill=BLACK, font=FONT_MAIN,
                                               justify=RIGHT, width=280)
        X01, Y01, X11, Y11 = self.chat_area.bbox(user_text)
        self._round_rectangle(X01 - 14, Y01-4, X11+14, Y11+4, radius=20, fill=LIGHT_BLUE, outline=LIGHT_BLUE)
        self.chat_area.tag_raise(user_text)
        y_coord_2 = self.chat_area.bbox(user_text)[3]
        bot_text = self.chat_area.create_text(25, y_coord_2+34, text=msg2, anchor='nw', fill=WHITE, font=FONT_MAIN,
                                               width=280)
        X02, Y02, X12, Y12 = self.chat_area.bbox(bot_text)
        self._round_rectangle(X02-14, Y02-4, X12 + 14, Y12+4, radius=20, fill=DARK_BLUE, outline=DARK_BLUE)
        self.chat_area.tag_raise(bot_text)
        if not DIAL_TAG:
            DIAL_TAG.append(bot_text)
        else:
            DIAL_TAG[0]=bot_text
        self.chat_area.configure(scrollregion=self.chat_area.bbox("all")) #ensures the context of our chat area is actually scrollable
        self.chat_area.yview_moveto('1.0') #always show the end of the dialogue

    def _round_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        '''
        Creates a rectangle with rounded borders inside chat area.
        The solution is retrieved from: https://stackoverflow.com/questions/44099594/how-to-make-a-tkinter-canvas-rectangle-with-rounded-corners
        '''

        points = [x1 + radius, y1,
                  x1 + radius, y1,
                  x2 - radius, y1,
                  x2 - radius, y1,
                  x2, y1,
                  x2, y1 + radius,
                  x2, y1 + radius,
                  x2, y2 - radius,
                  x2, y2 - radius,
                  x2, y2,
                  x2 - radius, y2,
                  x2 - radius, y2,
                  x1 + radius, y2,
                  x1 + radius, y2,
                  x1, y2,
                  x1, y2 - radius,
                  x1, y2 - radius,
                  x1, y1 + radius,
                  x1, y1 + radius,
                  x1, y1]

        self.chat_area.create_polygon(points, **kwargs, smooth=True)

if __name__ == "__main__":
    app_gui = ChatApplication()
    app_gui.run()
