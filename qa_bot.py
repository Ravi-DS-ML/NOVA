import streamlit as st
import google.generativeai as genai

class QABot:
    def __init__(self):
        self.genai_api_key = None
        self.chat = None

    def set_api_key(self, api_key):
        self.genai_api_key = api_key
        genai.configure(api_key=self.genai_api_key)
        # Initialize chat instance after setting API key
        self.chat = genai.GenerativeModel("gemini-pro").start_chat(history=[])

    def get_gemini_response(self, question):
        response = self.chat.send_message(question, stream=True)
        return response

    def run(self):
        st.header("QA Application")
        st.write('Q&A Bot, Designed for any questions you may have')
        # Initialize session state for chat history if it doesn't exist
        if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = []

        input_text = st.text_input("Input: ", key="qa_input")
        submit_button = st.button("Ask the question")

        if submit_button and input_text:
            response = self.get_gemini_response(input_text)
            if response is None:
                st.error("Check the question and try again")
            # Add user query and response to session state chat history
            st.session_state['chat_history'].append(("You", input_text))
            st.subheader("The Response is")
            for chunk in response:
                st.write(chunk.text)
                st.session_state['chat_history'].append(("Bot", chunk.text))

# Instantiate and run the bot
# qa_bot = QABot()
# qa_bot.set_api_key("your_api_key_here")
# qa_bot.run()
