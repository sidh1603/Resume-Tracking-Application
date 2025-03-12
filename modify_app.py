import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
from PIL import Image
import pdf2image
import io
import base64

#  Load API Key
load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=api_key)

#  Function to Process PDF and Convert First Page to Image
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_bytes_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_bytes_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No File Uploaded")

#  Function to Get Gemini Response
def get_gemini_response(query, pdf_content, job_description):
    """Generates an AI response based on the resume and job description."""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([query, pdf_content[0], job_description])
        return response.text
    except Exception as e:
        return f"❌ Error: {str(e)}"

#  Streamlit App with Background Color
def main():
    st.set_page_config(page_title="ATS Resume Expert", page_icon="🦜", layout="wide")

    #  Apply Background Color Using HTML & CSS
    st.markdown(
        """
        <style>
            body {
                background-color: #f4f4f4;
            }
            .stApp {
                background-color: #f4f4f4;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            }
            .stTextArea, .stFileUploader {
                border: 2px solid #4CAF50;
                border-radius: 10px;
                padding: 10px;
            }
            .stButton>button {
                border-radius: 8px;
                padding: 10px 15px;
                font-size: 16px;
                font-weight: bold;
            }
            .stButton>button:hover {
                background-color: #007BFF !important;
                color: white !important;
            }
        </style>
        """, 
        unsafe_allow_html=True
    )

    #  Stylish Header
    st.markdown(
        """
        <h1 style='text-align: center; color: #4CAF50;'>📄 ATS Resume Expert</h1>
        <p style='text-align: center; font-size: 18px; color: #555;'>Analyze your resume and get insights on how well you match the job description!</p>
        <hr style='border: 2px solid #4CAF50;'>
        """, 
        unsafe_allow_html=True
    )

    #  Job Description Input with Stylish Box
    st.markdown("<h3 style='color: #008CBA;'>📝 Job Description</h3>", unsafe_allow_html=True)
    input_text = st.text_area("Paste the Job Description Here:", key="input", height=150)

    #  Resume Upload with Custom Style
    st.markdown("<h3 style='color: #008CBA;'>📤 Upload Your Resume (PDF)</h3>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload your Resume", type=["pdf"])

    if uploaded_file is not None:
        st.success(f"✅ **{uploaded_file.name}** uploaded successfully!")

    #  Buttons with Custom Colors
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        submit1 = st.button("🔍 Evaluate Resume", key="eval", help="Get professional evaluation")
    with col2:
        submit2 = st.button("📈 Improve Skills", key="skills", help="Get skill improvement suggestions")
    with col3:
        submit3 = st.button("🔑 Identify Missing Keywords", key="keywords", help="Find missing keywords in your resume")
    with col4:
        submit4 = st.button("📊 Percentage Match Analysis", key="match", help="Check how well your resume matches")

    #  Prompts for AI Analysis
    input_prompt1 = """ 
    You are an experienced HR with technical expertise in evaluating resumes for Data Science, 
    Full Stack Developer, Data Engineer, DevOps, or Data Analyst roles. Your task is to **review the resume** 
    against the provided job description and provide a **detailed evaluation**.
    """

    input_prompt2 = """
    You are a **Technical Human Resource Manager** with expertise in various job roles.
    Your role is to **analyze the resume** and suggest **specific skill improvements** to make the candidate
    a better fit for the job.
    """

    input_prompt3 = """  
    You are an **ATS (Applicant Tracking System) expert** with a deep understanding of resume scanning.
    Analyze the resume against the job description and **list the missing keywords** that could improve the match.
    """

    input_prompt4 = """  
    You are an **Advanced ATS System** that calculates the **match percentage** between a resume and a job description.
    
    - **Provide a match percentage (0-100%)**
    - **List missing skills and keywords**
    - **Highlight strengths and weaknesses of the candidate**
    """

    #  Process User Action
    if submit1 or submit2 or submit3 or submit4:
        if uploaded_file is not None:
            pdf_content = input_pdf_setup(uploaded_file)

            if submit1:
                response = get_gemini_response(input_prompt1, pdf_content, input_text)
                st.markdown("<h3 style='color: #4CAF50;'>📄 Resume Evaluation</h3>", unsafe_allow_html=True)
                st.write(response)

            elif submit2:
                response = get_gemini_response(input_prompt2, pdf_content, input_text)
                st.markdown("<h3 style='color: #4CAF50;'>📈 Skill Improvement Suggestions</h3>", unsafe_allow_html=True)
                st.write(response)

            elif submit3:
                response = get_gemini_response(input_prompt3, pdf_content, input_text)
                st.markdown("<h3 style='color: #4CAF50;'>🔑 Missing Keywords Analysis</h3>", unsafe_allow_html=True)
                st.write(response)

            elif submit4:
                response = get_gemini_response(input_prompt4, pdf_content, input_text)
                st.markdown("<h3 style='color: #4CAF50;'>📊 Percentage Match & Resume Analysis</h3>", unsafe_allow_html=True)
                st.write(response)

        else:
            st.error("⚠️ Please upload your resume before proceeding.")

#  Run the Streamlit App
if __name__ == "__main__":
    main()
