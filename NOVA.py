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


import json
import PyPDF2

class ResumeParserBot:
    def __init__(self):
        self.genai_api_key = None

    def set_api_key(self, api_key):
        self.genai_api_key = api_key
        genai.configure(api_key=self.genai_api_key)

    def get_gemini_answer(self, question):
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(question)
        return json.loads(response.text)

    def input_pdf_text(self, uploaded_file):
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ''
        for page in range(len(reader.pages)):
            text += str(reader.pages[page].extract_text())
        return text

    def run(self):
        input_prompt = '''
        Hey Act like a skilled or very experienced ATS (Application Tracking System) with a deep understanding of the tech field, software engineering, data science, data analyst, and machine learning engineer. Your task is to evaluate the resume based on the given description. You must consider the job market is very competitive and you should provide the best assistance to improve the resume. Assign the percentage Matching based on the JD and the missing keywords with high accuracy
        resume:{text}
        description:{jd}

        I want the response in one single string having the structure 
        {{"JD Match":"%",'"missing keywords":[],"Profile Summary":""}}'
        '''

        st.title("Resume Parsing App")
        st.write("Improve your Resume")

        uploaded_file = st.file_uploader("Choose a Resume", type="pdf", help='Please upload a valid PDF file')
        jd = st.text_area("Enter Job Description")

        submit = st.button("Submit")

        def get_data():
            if submit and uploaded_file is not None:
                text = self.input_pdf_text(uploaded_file)
                prompt = input_prompt.format(text=text, jd=jd)
                response = self.get_gemini_answer(prompt)
                return response

        if submit:
            if uploaded_file is None:
                st.warning("Please upload a valid PDF file")
            else:
                with st.spinner('Wait for it...'):
                    response = get_data()
                st.json(response)




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

class RecipeBot:
    def __init__(self):
        self.genai_api_key = None

    def set_api_key(self, api_key):
        self.genai_api_key = api_key
        genai.configure(api_key=self.genai_api_key)

    def generate_response(self):
        st.header("Recipe Bot")
        st.write('Recipe Bot, Designed for any recipe related questions you may have')
        model = genai.GenerativeModel('gemini-pro')  
        chat = model.start_chat(history=[])
        user_input = st.text_input("Enter your query: ")
        prompt = """
            Hey act like a professional chef with the knowledge of food and all the ingredients used.
            Based on the user query give the best response. Add the right and best amount of ingredients to be used.
            The user query is:
            {}
            Use the following format to answer the query: not in the exact way append the details you generate in the brackets of the format
            The format should be:
            <Name of the dish>\n
            <Country of origin>\n
            <Cuisine>\n
            <Ingredients>\n
            <Instructions>\n
            <Cooking time>\n
            <FAQ>\n
            And do not answer anything else other than food questions.
            If asked just reply ''I am currently built on only food data so please ask questions regarding that only.''
            """.format(user_input)

        if user_input:
            with st.spinner('Please wait while we generate your response...'):
                response = chat.send_message(prompt)
                first_gen_text = response.text

                refined_response = ""
                if first_gen_text.strip() == 'I am currently built on only food data so please ask questions regarding that only.':
                    refined_response = "I am currently built on only food data so please ask questions regarding that only."
                else:
                    if first_gen_text.strip(): 
                        refined_response = first_gen_text

                st.write(refined_response)

class WeightLossAssistantBot:
    def __init__(self):
        self.genai_api_key = None

    def set_api_key(self, api_key):
        self.genai_api_key = api_key
        genai.configure(api_key=self.genai_api_key)

    def get_user_info(self):
        col1, col2 = st.columns(2)

        with col1:
            gender = st.selectbox('Your Gender', ('Male', 'Female'))
            weight = st.number_input('Your Weight (Kg)', min_value=30, max_value=200, value=58)
            veg_or_non_veg = st.selectbox('Diet Preference', ('Veg', 'Non-Veg'))
            
        with col2:
            age = st.number_input('Your Age', min_value=10, max_value=100, step=1, value=21)
            height = st.number_input('Your Height (Cm)', min_value=100, max_value=250, value=174)
            aim = st.selectbox('Your Goal', ('Weight Loss', 'Weight Gain', 'Maintain Weight'))
        
        user_info = f'''
            Gender: {gender}\n
            Weight: {weight} Kg\n
            Age: {age}\n
            Height: {height} cm\n
            Goal: {aim}\n,
            Diet Preference: {veg_or_non_veg}
            '''
        return user_info

    def generate_analysis(self, user_info):
        output_format = '''
            "Range": <Ideal Weight Range for your age and height>\n,
            "Target": <Target Weight you should aim for>\n,
            "Difference": <Weight you need to lose or gain (specify if gain or lose)>\n,
            "BMI": <Your BMI according to your height>\n,
            "Aim": <Your Aim>\n,
            If the aim of user is to gain weight or lose weight then specify the deight based on the target weight set by the user. If the aim is to maintain weight, do not specify the target weight.\n,
            "Meal Plan For the next seven days": <Meal plan for breakfast, lunch, and dinner for the next 7 days
            according to your goal. Remember to consider your diet preference. If you are vegetarian, do not recommend non-veg options. If you are non-vegetarian, recommend both.
            Provide this information as a markdown format>\n,
            "Total Days": <Total days to reach your target for optimal performance>\n,
            "Weight per week": <Weight you need to lose or gain per week according to your BMI>\n
            Make the whole output in markdown format
            '''
        prompt = user_info + ("\nYou are a expert health advisor.\n" + "Your response should be in the following format:\n") + output_format

        st.title("Weight Loss Assistant")
        st.write('Weight Loss Bot, Designed for any weight loss related questions you may have')
        model = genai.GenerativeModel('gemini-pro')  
        chat = model.start_chat(history=[])
        if st.button('Get Analysis'):
            with st.spinner():
                response = chat.send_message(prompt)
                st.write(response.text)
# Create instances of all bot classes
recipe_bot = RecipeBot()
weight_loss_bot = WeightLossAssistantBot()
qa_bot = QABot()
health_bot = HealthBot()
# fun_bot = FunBot()
resume_parser_bot = ResumeParserBot()
vision_bot = VisionBot()
# chat_bot = ChatBot()  # Create an instance of the ChatBot class
ask_image_bot = AskImageBot()
# Function to hide/show bot sections based on selection
def show_hide_bots(selected_bot):
    if selected_bot == 'Home':
        st.title("Welcome to our integrated AI system N.O.V.A!")
        st.write("Our AI system aims to provide various functionalities while adhering to ethical guidelines.")
        st.write("As part of our commitment to ethical AI, we prioritize transparency, fairness, and privacy.")
        st.write("We encourage users to use AI responsibly and respect privacy concerns.")
        st.markdown("---")
        st.write('First enter your API key in the sidebar.')
        st.write("Now choose a bot to get started.")
        st.write("Select a bot to get started:")
    elif selected_bot == "Recipe Bot":
        recipe_bot.generate_response()
    elif selected_bot == "Weight Loss Assistant Bot":
        user_info = weight_loss_bot.get_user_info()
        weight_loss_bot.generate_analysis(user_info=user_info)
    elif selected_bot == "QA Bot":
        qa_bot.run()
    elif selected_bot == "Health Bot":
        health_bot.run()
    # elif selected_bot == "Fun Bot":
    #     fun_bot.run()
    elif selected_bot == "Resume Parser Bot":
        resume_parser_bot.run()
    elif selected_bot == "Vision Bot":
        vision_bot.run()
    elif selected_bot == "Ask About Image":
        ask_image_bot.run()
    # elif selected_bot == "Chat Bot":  # Add this block for Chat Bot
    #     chat_bot.run('model.h5', 'tokenizer.pkl')

# Sidebar with API key input
api_key = st.sidebar.text_input("Enter the API Key")

# Radio button to choose the bot
selected_bot = st.sidebar.radio("Choose a Bot", ('Home',"Recipe Bot", "Weight Loss Assistant Bot", "QA Bot", "Health Bot",'Ask About Image' ,"Resume Parser Bot", "Vision Bot"))  # Add "Chat Bot" option

# Set API key for all bot instances if provided
if not api_key:
    st.sidebar.warning("Please enter your API key in the sidebar before using any bot.")
if api_key:
    recipe_bot.set_api_key(api_key)
    weight_loss_bot.set_api_key(api_key)
    qa_bot.set_api_key(api_key)
    health_bot.set_api_key(api_key)
    # fun_bot.set_api_key(api_key)
    resume_parser_bot.set_api_key(api_key)
    vision_bot.set_api_key(api_key)
    ask_image_bot.set_api_key(api_key)


# Call function to show/hide bot sections based on selection
show_hide_bots(selected_bot)
