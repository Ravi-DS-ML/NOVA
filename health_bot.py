import streamlit as st
import google.generativeai as genai
from PIL import Image

class HealthBot:
    def __init__(self):
        self.genai_api_key = None

    def set_api_key(self, api_key):
        self.genai_api_key = api_key
        genai.configure(api_key=self.genai_api_key)

    def get_gemini_response(self, input_text, image, prompt):
        model = genai.GenerativeModel('gemini-pro-vision')
        response = model.generate_content([input_text, image[0], prompt])
        return response.text

    def input_image_setup(self, uploaded_file):
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

    def run(self):
        st.header("Health App")
        st.write('Health Bot, Designed for any health related questions you may have')
        input_prompt = """
        You are an expert in nutritionist where you need to see the food items from the image
        and calculate the total calories, also provide the details of every food items with calories intake
        is below format

        1. Item 1 - no of calories
        2. Item 2 - no of calories
        ----
        ----
        """

        input_text = st.text_input("Input Prompt: ", key="health_input")
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image.", use_column_width=True)
        else:
            image = ""

        submit_button = st.button("Tell me the total calories")

        if submit_button:
            if uploaded_file is None:
                st.warning("Please upload an image.")
            else:
                image_data = self.input_image_setup(uploaded_file)
                response = self.get_gemini_response(input_text, image_data, input_prompt)
                st.subheader("The Response is")
                st.write(response)

# Instantiate and run the bot
# health_bot = HealthBot()
# health_bot.set_api_key("your_api_key_here")
# health_bot.run()
