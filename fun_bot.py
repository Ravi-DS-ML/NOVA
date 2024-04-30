import streamlit as st
import google.generativeai as palm

class FunBot:
    def __init__(self):
        self.palm_api_key = None

    def set_api_key(self, api_key):
        self.palm_api_key = api_key
        palm.configure(api_key=self.palm_api_key)

    def get_gemini_response(self, prompt):
        completion = palm.generate_text(
            model='models/text-bison-001',
            prompt=prompt,
            temperature=0,
            max_output_tokens=800,
        )
        return completion

    def run(self):
        st.header("FUN Application")
        st.write('Fun Bot, Designed for any fun questions you may have')
        input_query = st.text_input("Enter your Query ", key='fun_input')
        submit_button = st.button("Tell me something fun")

        input_prompt = '''
        You are a helpful assistant.
        You are a fun bot.
        Tell new jokes each time and do not repeat the joke.
        '''

        if submit_button:
            response = self.get_gemini_response(input_prompt + input_query)
            st.subheader("The Response is")
            st.write(response.result)

# Instantiate and run the bot
# fun_bot = FunBot()
# fun_bot.set_api_key("your_api_key_here")
# fun_bot.run()
