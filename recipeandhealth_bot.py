import streamlit as st
import google.generativeai as genai

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

# Instantiate and run the bots
# recipe_bot = RecipeBot()
# weight_loss_bot = WeightLossAssistantBot()
# api_key = st.sidebar.text_input("Enter the API Key")
# if st.sidebar.button("Set API Key"):
#     if api_key:
#         recipe_bot.set_api_key(api_key)
#         weight_loss_bot.set_api_key(api_key)
#         recipe_bot.generate_response()
#         weight_loss_bot.get_user_info()
#         weight_loss_bot.generate_analysis()
