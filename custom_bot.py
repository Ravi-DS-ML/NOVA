import streamlit as st
from tensorflow.keras.models import load_model
import pickle
import models

class ChatBot:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        if 'conversation_history' not in st.session_state:
            st.session_state.conversation_history = []

    def load_model_and_tokenizer(self, model_path, tokenizer_path):
        self.model = load_model(model_path)
        self.tokenizer = pickle.load(open(tokenizer_path, 'rb'))

    def get_user_input(self):
        return st.text_input('User')

    def get_bot_response(self, user_input):
        bot_data = models.get_data(user_input)
        st.session_state.conversation_history.append({'user': user_input, 'bot': bot_data})

    def display_conversation_history(self):
        for item in reversed(st.session_state.conversation_history):
            col1, col2 = st.columns(2)
            with col2:
                st.markdown(f"**User:** {item['user']}")
            with col1:
                st.divider()
                st.markdown(f"**Bot:** {item['bot']}")

    def run(self, model_path, tokenizer_path):
        st.title('Custom ChatBot')
        self.load_model_and_tokenizer(model_path, tokenizer_path)
        user_input = self.get_user_input()
        submit = st.button('Submit')
        if submit and user_input:
            self.get_bot_response(user_input)
        self.display_conversation_history()

# Instantiate and run the bot
# chat_bot = ChatBot()
# chat_bot.run('model.h5', 'tokenizer.pkl')
