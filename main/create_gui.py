from tkinter import *


class create_gui:
    window = Tk()
    messages = None

    def __init__(self):
        print("create gui started.")
        self.__create()

    def __add_message_to_messages_field(self, m_type, message):
        print("add message started")
        tag_name = ''

        if m_type == 'You':
            tag_name = 'YOU'
        elif m_type == 'Amigo':
            tag_name = 'BOT'

        self.messages.insert(INSERT, m_type + " : ", tag_name, message + "\n")

    def __enter_pressed(self, user_input_field):

        if user_input_field.compare("end-1c", "==", "1.0"):
            print("empty text field")
            user_input_field.delete('1.0', END)
            return 'break'

        print("enter pressed")
        input_get = user_input_field.get('1.0', END)

        self.__add_message_to_messages_field('You', input_get)
        # label = Label(window, text=input_get)
        user_input_field.delete('1.0', END)
        # label.pack()
        return 'break'

    def __create(self):
        # window attributes
        self.window.geometry("500x650")
        self.window.title("Amigo")
        # window attributes

        self.messages = Text(self.window, height=38)
        self.messages.pack(fill=X)
        self.messages.tag_config("YOU", foreground="blue")
        self.messages.tag_config("BOT", foreground="green")

        user_input_field = Text(self.window, height=1.5)
        user_input_field.pack(side=BOTTOM, fill=X)
        user_input_field.bind("<Return>", (lambda event: self.__enter_pressed(user_input_field)))
        # configuring a tag called BOLD

        self.window.mainloop()


create_gui()
