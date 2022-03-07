from tkinter import *
from tkinter import scrolledtext #for some reason it only works if implemented explicitly
from chatbot import get_response, predict_class
from PIL import Image, ImageTk
import json
BLACK = "#151515"
WHITE = "#FFFFFF"
DARK_BLUE = "#002145"
LIGHT_BLUE="#A4C3E4"
LIGHT_GRAY="#EEEEEE"

FONT_BOLD = ("Roboto", 14, "bold")
FONT= ("Roboto", 14)

INTENTS = json.loads(open("../intents.json").read())

class ChatApplication:

    def __init__(self):
        self.window = Tk()
        self._setup_main_window()

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("Chat")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=470, height=550, bg=WHITE)

        # head label
        self.head_label = Label(self.window, bg=WHITE, fg=DARK_BLUE,
                           text="UBCO chatbot", font=FONT_BOLD, pady=10)
        self.head_label.place(relwidth=1)

        #ubco logo image
        ubco_logo = ImageTk.PhotoImage(Image.open("images/UBC-logo-transparent.png").resize((26, 35)))
        logo_label=Label(self.head_label, bg=WHITE, image=ubco_logo)
        logo_label.image=ubco_logo
        logo_label.place(relwidth=0.07, relheight=0.9)

        # tiny divider
        line = Label(self.window, width=450, bg=DARK_BLUE)
        line.place(relwidth=1, rely=0.07, relheight=0.012)


        # text widget
        self.text_widget = scrolledtext.ScrolledText(self.window, width=20, height=2, bg=WHITE, fg=BLACK,
                                font=FONT, padx=5, pady=5, wrap=WORD)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)


        # bottom label
        bottom_label = Label(self.window, bg=DARK_BLUE, height=80)
        bottom_label.place(relwidth=1, rely=0.825)

        # message entry box
        self.msg_entry = Entry(bottom_label, bg=LIGHT_GRAY, fg=BLACK, font=FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)

        # send button
        send_button = Button(bottom_label, text="Send", font=FONT_BOLD, width=20, bg=LIGHT_BLUE,
                             command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.77, rely=0.018, relheight=0.04, relwidth=0.22)

    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        self._insert_message(msg)

    def _insert_message(self, msg):
        if not msg:
            return

        self.msg_entry.delete(0, END)
        msg1 = f"You: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)


        msg2 = f"UBCO: {get_response(predict_class(msg), INTENTS)}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg2)
        self.text_widget.configure(state=DISABLED)

        self.text_widget.see(END)


if __name__ == "__main__":
    app_gui = ChatApplication()
    app_gui.run()