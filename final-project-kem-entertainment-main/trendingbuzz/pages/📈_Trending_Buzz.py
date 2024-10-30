import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from google.cloud import bigquery
import functionality

#write css for Trending Buzz into st.markdown
with open('trendingbuzz/trendingstyle.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#Configuring genai api/bigquery client
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)
model = functionality.create_text_model()
image_model = genai.GenerativeModel('gemini-pro-vision')
client = bigquery.Client()


#Static prompts for page load content
sports_prompt = "Give me a single headline of trending news in sports as a single string"
social_media_prompt = "Give me a single headline of trending news in social media as a single string."
entertainment_prompt = "Give me a single headline of trending news in entertainment as a single string, no quotes."

#Abstracting content generation here, then set 'loaded' to True to prevent refreshing this content.
#It also looks better because everything loads at once
if 'loaded' not in st.session_state:
    st.session_state.loaded = False
if not st.session_state.loaded:
    st.session_state.sports_response = functionality.generate_content(model, sports_prompt)
    st.session_state.social_media_response = functionality.generate_content(model, social_media_prompt)
    st.session_state.entertainment_response = functionality.generate_content(model, entertainment_prompt)
    st.session_state.loaded = True

#Title and description
st.title("Trending Buzz 📈")
st.write("Analyze your favorite trends, recommendations, and the hottest searches!")

#Sports section
st.header("Sports 🏀")
st.write("◼️" + st.session_state.sports_response.text)

#Social Media section
st.header("Social Media 🔔")
st.write("◼️" + st.session_state.social_media_response.text)

#Entertainment section
st.header("Entertainment 📽")
st.write("◼️" + st.session_state.entertainment_response.text)


#####
#Generate new content based off user input
st.markdown('<br><br>', unsafe_allow_html=True)
st.header("What other content would you like to see?")
user_prompt = st.text_input("Type here!")

#Using a button/session state to prevent content from regenerating when using other features
if 'user_response' not in st.session_state:
    st.session_state.user_response = False
if st.button("Generate new trends"):
    if user_prompt:
        st.session_state.user_response = functionality.generate_content(model, "Give me a single headline of trending news in " + user_prompt)
if st.session_state.user_response:
    st.write("◼️" + st.session_state.user_response.text)


#Generate similar/show ideas from a user uploaded image
user_image = st.file_uploader("Upload a show or movie cover to get new recommendations")

#Use a button/session states to prevent content from regenerating when using other features
#Let's use some exception handling in case gemini returns an 'unsafe' response and doesn't want to display.
if 'user_image_response' not in st.session_state:
    st.session_state.user_image_response = False
if st.button("Get a new recommendation"):
    if user_image:
        image_to_text = image_model.generate_content(Image.open(user_image))
        image_to_prompt = "Provide just the name of a new piece of media similar to " + image_to_text.text
        st.session_state.user_image_response = functionality.generate_content(model, image_to_prompt)
if st.session_state.user_image_response:
    try:
        st.write("Check out: " + st.session_state.user_image_response.text + "!")
    except Exception as e:
        st.write("Response was too crazy. Try again!")


#####
#Button to call BigQueryand grab top 10 most searched terms of the day
st.markdown('<br><br>', unsafe_allow_html=True)
st.header("Top 10 Search Terms 🔎")
if 'query_generate' not in st.session_state:
    st.session_state.query_generate = False
def query_generated():
    QUERY = """
    # Find the latest refresh date
    SELECT MAX(refresh_date) AS latest_date
    FROM `bigquery-public-data.google_trends.top_terms`;
    # Subquery for recent terms with highest scores on the latest date
    WITH LatestScores AS (
    SELECT term, MAX(score) AS highest_score
    FROM `bigquery-public-data.google_trends.top_terms`
    WHERE refresh_date = (SELECT MAX(refresh_date) FROM `bigquery-public-data.google_trends.top_terms`)
    GROUP BY term  -- Group by term here
    ORDER BY highest_score DESC
    LIMIT 10
    )
    # Select the desired data
    SELECT term, highest_score
    FROM LatestScores;
    """
    top_ten_query = client.query(QUERY)
    st.session_state.terms = list(top_ten_query.result())
    st.session_state.query_generate = True
st.button("Press to generate top 10 Google Search terms of the day", on_click=query_generated)

#when query is done, display to user
if st.session_state.query_generate:
    download_string = ""
    for term in st.session_state.terms:
        st.write("◼️" + term[0])
        download_string += (term[0] + ", ")
    #give user the option to download the top 10 search terms generated
    st.download_button("Download these search terms", download_string, file_name="top10.txt")
