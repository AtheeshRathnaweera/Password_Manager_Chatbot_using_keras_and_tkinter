import json
from tkinter import *

import prepocessor as pp
import chatbot as cb


class create_gui:
    chatbot_name = "Elvy"
    words_dictionary = None
    window = Tk()
    messages = None

    def __init__(self):
        print("create gui started.")
        self.words_dictionary = pp.Preprocessor.get_the_words_dictionary()  # load the essentials
        self.__create()

    def __add_message_to_messages_field(self, m_type, message):
        tag_name = ''  # tag name for color the responser name

        if m_type == 'You':
            tag_name = 'YOU'
            message = message + "\n"
        elif m_type == self.chatbot_name:
            tag_name = 'BOT'
            message = message + "\n\n"

        self.messages.config(state='normal')  # change the messages textbox state to normal for add the new line
        # insert the new line to the end of the messages textbox
        self.messages.insert(END, m_type + " : ", tag_name, message)
        self.messages.see("end")  # scroll to the end of messages textbox
        self.messages.config(state='disabled')  # disable the messages textbox

    def __enter_pressed(self, user_input_field):

        if user_input_field.compare("end-1c", "==", "1.0"):  # check if the user input is empty
            print("empty text field")
            user_input_field.delete('1.0', END)
            return 'break'

        input_get = user_input_field.get('1.0', END)  # get the user input
        self.__add_message_to_messages_field('You', input_get)  # add user message to the messages textbox

        bot_response = self.__get_the_bot_response(input_get)  # pass the user input to get the model response

        self.__add_message_to_messages_field(self.chatbot_name, bot_response)  # add the model response to the msg txtbo

        user_input_field.delete('1.0', END)  # clear the user input textbox
        return 'break'

    def __get_the_bot_response(self, user_sentence):
        # get the encoded list from the user input
        processed_result = pp.Preprocessor.processing(self.words_dictionary, user_sentence)
        return cb.ChatBot.get_the_response(self.class_names, self.intents, self.model, processed_result)

    def __create(self):
        # window attributes
        self.window.geometry("500x650")
        self.window.title(self.chatbot_name)
        # window attributes

        # messages textbox for display the conversation
        self.messages = Text(self.window, height=38)
        self.messages.pack(fill=X)
        self.messages.config(state='disabled')
        self.messages.tag_config("YOU", foreground="blue")
        self.messages.tag_config("BOT", foreground="green")
        # messages textbox for display the conversation

        # text box for get user input
        user_input_field = Text(self.window, height=1.5)
        user_input_field.insert('0.0', "Type something here!")  # set the placeholder
        user_input_field.pack(side=BOTTOM, fill=X)  # fix to the bottom of the window
        # bind event for remove the placeholder text when focus
        user_input_field.bind("<FocusIn>", lambda args: user_input_field.delete('0.0', 'end'))
        # bind event for enter press in user input text box
        user_input_field.bind("<Return>", lambda event: self.__enter_pressed(user_input_field))
        # text box for get user input

        self.window.mainloop()
