import streamlit as st
import pandas as pd
import os  # For environment variables
import pandas as pd
import numpy as np 
from PIL import Image
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
from google.cloud import bigquery
import random
import functionality 

# Import for Google generative AI, ensure you have the correct library installed
import google.generativeai as genai

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Set page config to widen the layout
st.set_page_config(layout="wide")

# Configure the Google AI model with an environment variable for the API key
api_key = os.getenv('GOOGLE_GENAI_KEY', 'AIzaSyAQUH2gMLozHX5chMBIr2WNLDUUSkMWdJs')  # Use a default or throw an error
genai.configure(api_key=api_key)
text_model = genai.GenerativeModel('gemini-pro')
image_model = genai.GenerativeModel('gemini-pro-vision')
image_generator = ImageGenerationModel.from_pretrained("imagegeneration@005")
client = bigquery.Client()
model = functionality.create_text_model()

from google.api_core.exceptions import InvalidArgument

def imagen(prompt):
    try:
        images = image_generator.generate_images(prompt=prompt)
        if images:
            image_path = 'sample.jpg'
            images[0].save(image_path)
            return image_path  # Return the path where the image was saved
        else:
            return None  # Return None if no image was generated, skip displaying anything
    except Exception as e:
        # Log error quietly without showing it to the user
        with open("error_log.txt", "a") as log_file:
            log_file.write(f"Failed prompt: {prompt} - Error: {str(e)}\n")
        return None  # Return None if an error occurred, continue without showing anything



imagen("a picture of a dog")  # Call without the 'rating' argument

# hiddenness_level = functionality.create_slider("How hidden do you want to be? 100 = most hidden", min_value=1, max_value=100, value=50) 

def get_hidden_gems(prompt, hiddenness_level):
    adjustment = ""
    if hiddenness_level <= 25:
        adjustment = " Focus on underground and lesser-known artists."
    elif hiddenness_level <= 50:
        adjustment = " Include a mix of hidden gems and emerging artists."
    else:
        adjustment = " I'm interested in both popular and undiscovered artists."

    response = text_model.generate_content(prompt + adjustment)
    artist_names = response.text.split('\n')

    # Ensure that no more than 10 artists are processed
    artist_names = artist_names[:10]

    for name in artist_names:
        col1, col2 = st.columns([3, 2])
        col1.write(name)
        with col2:
            image_path = imagen(name)  # Generate image for the artist
            if image_path:
                st.image(image_path, caption=f"Artwork inspired by {name}")
            # If no image is generated, nothing is displayed, and it just skips to the next artist

# Interface setup
st.title("Hidden Gems Finder")
user_prompt = st.text_input("Enter a music genre or theme:")
hiddenness_level = st.slider("Select the level of hiddenness", 0, 100, 50)
if st.button("Discover Hidden Gems"):
    get_hidden_gems(user_prompt, hiddenness_level)

# Query BigQuery for movie recommendations
def generate_query():
    QUERY = """
    SELECT title, reviewer_rating
    FROM `bigquery-public-data.imdb.reviews`
    WHERE reviewer_rating >= 6.0
    ORDER BY RAND()
    LIMIT 10
    """
    query_job = client.query(QUERY)
    results = query_job.result()

    st.session_state.movies = [{'title': row.title, 'reviewer_rating': row.reviewer_rating} for row in results]
    st.session_state.query_generated = True

if st.button("Press to generate 10 random movies (6.0+ rating)", on_click=generate_query):
    for movie in st.session_state.movies:
        st.subheader(f"**{movie['title']}** (Rating: {movie['reviewer_rating']})")
        imagen(f"A movie poster for {movie['title']}")  # Generate and display image for each movie

st.markdown("---")
st.markdown("© 2024 CampusMate. All rights reserved.")