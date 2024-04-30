import streamlit as st
import google.generativeai as genai
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

# Instantiate and run the bot
# resume_parser_bot = ResumeParserBot()
# resume_parser_bot.set_api_key("your_api_key_here")
# resume_parser_bot.run()
