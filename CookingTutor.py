import streamlit as st
import google.generativeai as genai
from google.genai import types
from PIL import Image
import io

try:
    with open('static/key.txt','r') as file:
        key = file.read()
except:
    st.write('No API key given in ./static/key.txt')
    exit()

# Setting up Gemini API Key
genai.configure(api_key=key)

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

# Set AI Tutor prompt
system_prompt = """
You are a professional AI recipe tutor who specializes in helping users learn cooking and recipe design.
Please provide detailed recipes based on user needs, including ingredients, steps, time estimates and suggestions.
If the user has specific dietary restrictions (e.g. vegetarian, gluten-free, low carb, etc.), please provide those recommendations.
If users make mistakes or are confused about certain steps, be patient and explain and provide helpful tips.
"""

# Welcome Message
st.write("🍽 AI Recipe Tutor: Hello! I'm your AI recipe assistant for any cooking & recipe question you have!")

#Input Box
prompt = st.chat_input(placeholder="👩‍🍳: ")
image = st.file_uploader(label="Upload an Image", type=['.webp', '.jpg', '.png'], accept_multiple_files=True)

images:list[Image.Image] = []
if image != None:
    for uploaded_file in image:
        im = Image.open(io.BytesIO(uploaded_file.read()))
        images.append(im)
        st.image(im)

# Start a conversation loop

if prompt:
    # Let Gemini generate answers
    with st.spinner(text="Cooking a response...", show_time=True):
        response = model.generate_content(
            contents=[f"{system_prompt}\n\nuser: {prompt}\n\nAI Recipe Tutor:"]+images
            )
    with open('static/log.txt', 'a+') as file:
        file.write('\n')
        file.write(response.text)
    
    # Show AI Tutor's answers
    st.write("🍽 AI Recipe Tutor:", response.text, "\n")