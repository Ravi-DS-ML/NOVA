import streamlit as st
from PIL import Image
import google.generativeai as genai

class AskImageBot:
    def __init__(self):
        self.genai_api_key = None

    def set_api_key(self, api_key):
        self.genai_api_key = api_key
        genai.configure(api_key=self.genai_api_key)

    def initialize_streamlit_app(self):
        st.header("Ask Image Application")
        self.input_prompt = st.text_input("Input Prompt: ", key="ask_image_input")
        self.uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    def get_gemini_response(self):
        model = genai.GenerativeModel('gemini-pro-vision')
        if self.input_prompt != "":
            response = model.generate_content([self.input_prompt, self.image])
        else:
            response = model.generate_content(self.image)
        return response.text

    def run(self):
        self.initialize_streamlit_app()
        st.write('Image Bot, Designed to answer your question about the image')
        if self.uploaded_file is not None:
            self.image = Image.open(self.uploaded_file)
            st.image(self.image, caption="Uploaded Image.", use_column_width=True)
        else:
            self.image = None

        submit = st.button("Tell me about the image")

        if submit:
            if not self.genai_api_key:
                st.error("Please enter your OpenAI API key in the sidebar.")
            else:
                response = self.get_gemini_response()
                st.subheader("The Response is")
                st.write(response)

# Instantiate and run the bot
# ask_image_bot = AskImageBot()
# ask_image_bot.set_api_key("your_api_key_here")
# ask_image_bot.run()
