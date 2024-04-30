import streamlit as st
import google.generativeai as genai
from PIL import Image

class VisionBot:
    def __init__(self):
        self.genai_api_key = None

    def set_api_key(self, api_key):
        self.genai_api_key = api_key
        genai.configure(api_key=self.genai_api_key)

    def run(self):
        st.header("Vision Application")
        st.write('Ask any invoice related question and get answer with ease')
        input_prompt = """
            You are a professional invoice recognizer.
            Means you can extract all the necessary information from the invoice and tell the user.
            You are solely trained for the invoices of the products nothing else.
            """

        input_text = st.text_input("Input Prompt: ", key="vision_input")
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image.", use_column_width=True)
        else:
            image = ""

        submit_button = st.button("Tell me about the image")

        def get_gemini_response(input_text, image, prompt):
            model = genai.GenerativeModel('gemini-pro-vision')
            response = model.generate_content([input_text, image[0], prompt])
            return response.text

        def input_image_setup(uploaded_file):
            if uploaded_file is not None:
                bytes_data = uploaded_file.getvalue()

                image_parts = [
                    {
                        "mime_type": uploaded_file.type,
                        "data": bytes_data
                    }
                ]
                return image_parts
            else:
                raise FileNotFoundError("No file uploaded")

        if submit_button:
            if uploaded_file is None:
                st.warning("Please upload an image.")
            else:
                image_data = input_image_setup(uploaded_file)
                response = get_gemini_response(input_text, image_data, input_prompt)
                st.subheader("The Response is")
                st.write(response)

# Instantiate and run the bot
# vision_bot = VisionBot()
# vision_bot.set_api_key("your_api_key_here")
# vision_bot.run()
