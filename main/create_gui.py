from tkinter import *

import prepocessor as pp
import chatbot as cb


class create_gui:

    words_dictionary = None
    class_names = None
    responses = []
    model = None
    window = Tk()
    messages = None

    def __init__(self):
        print("create gui started.")
        self.words_dictionary = pp.Preprocessor.get_the_words_dictionary()
        self.class_names = pp.Preprocessor.get_the_class_names()
        self.responses = pp.Preprocessor.get_the_responses()
        self.model = cb.ChatBot.get_the_model()
        self.__create()

    def __add_message_to_messages_field(self, m_type, message):
        print("add message started")
        tag_name = ''

        if m_type == 'You':
            tag_name = 'YOU'
            message = message + "\n"
        elif m_type == 'Amigo':
            tag_name = 'BOT'
            message = message + "\n\n"

        self.messages.insert(INSERT, m_type + " : ", tag_name, message)
        self.messages.see("end")  # scroll to the end of text field

    def __enter_pressed(self, user_input_field):

        if user_input_field.compare("end-1c", "==", "1.0"):
            print("empty text field")
            user_input_field.delete('1.0', END)
            return 'break'

        print("enter pressed")
        input_get = user_input_field.get('1.0', END)
        self.__add_message_to_messages_field('You', input_get)

        bot_response = self.__get_the_bot_response(input_get)

        self.__add_message_to_messages_field('Amigo', bot_response)

        # label = Label(window, text=input_get)
        user_input_field.delete('1.0', END)
        # label.pack()
        return 'break'

    def __get_the_bot_response(self, user_sentence):
        processed_result = pp.Preprocessor.processing(self.words_dictionary, user_sentence)
        return cb.ChatBot.get_the_response(self.class_names, self.responses, self.model, processed_result)

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

        # frame = Frame(self.window)
        # frame.pack_propagate(False)
        # frame.pack()
        self.window.mainloop()


create_gui()
