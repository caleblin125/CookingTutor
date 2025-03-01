import streamlit as st
import google.generativeai as genai
from google.genai import types
from PIL import Image
import io
from serpapi import GoogleSearch

try:
    with open('static/key.txt','r') as file:
        key = file.read()
except:
    st.write('No API key given in ./static/key.txt')
    exit()

try:
    with open('static/searchkey.txt','r') as file:
        SERPAPI_API_KEY = file.read()
except:
    st.write('No API key given in ./static/searchkey.txt')
    exit()

try:
    with open('static/log.txt', 'r') as file:
        st.write(file.read())
except:
    pass

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
Always cite your sources.
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

def search_query(query):
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_API_KEY,
        "num": 3  # Take the first three results
    }
    search = GoogleSearch(params)
    results = search.get_dict()

    if 'organic_results' in results:
        snippets = [item['snippet']+', link: '+item['link'] for item in results['organic_results'][:3]]
        return "\n".join(snippets)
    return "No relevant information found."

# Start a conversation loop
if prompt:
    # if prompt == 'clear':
    #     with open('log.txt', 'w'):
    #         pass
    #     exit()

    # Let Gemini generate answers
    with st.spinner(text="Searching for recipes...", show_time=True):
        # Start searching for additional information
        searchPrompt = prompt
        if len(images) > 0:
            searchPrompt += ' '+model.generate_content(["describe these images briefly for a websearch"]+images).text
        search_results = search_query(searchPrompt)

    with st.spinner(text="Cooking a response...", show_time=True):
        # Let Gemini generate the response and add the search results
        response = model.generate_content(
            [f"{system_prompt}\n"
            f"User: {prompt}\n"
            f"Search Grounding Info:\n{search_results}\n"
            f"AI Recipe Tutor:"] + images
        )

    with open('static/log.txt', 'a+') as file:
        file.write('\n------\n')
        file.write(prompt)
        file.write('\n------\n')
        file.write(response.text)
    
    # Show AI Tutor's answers
    st.write("🍽 AI Recipe Tutor:", response.text, "\n")