import streamlit as st
from PIL import Image
from google.cloud import bigquery
import google.generativeai as genai
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
import functionality
import os




# Define the split_rec_content function
def split_rec_content(response):
    # Extract the recommendations string from the response
    recommendations = response.text

    movies = []
    podcasts = []
    music = []

    current_category = None

    # st.title(recommendations)

    for line in recommendations.split("\n"):
        if not line.strip():
            continue
        line = line.replace("'", "")

        if line.startswith("**Movies:**"):
            current_category = "Movies"
        elif line.startswith("**Podcasts:**"):
            current_category = "Podcasts"
        elif line.startswith("**Music:**"):
            current_category = "Music"
        else:
            parts = line.split("https://")
            title = parts[0].strip()
            # link = parts[1].strip()

            if current_category == "Movies":
                movies.append({"title": title})
                # my_query = "INSERT INTO 'citric-lead-411804.moodmatch_01.Recommendations' (title, category, mood) VALUES (@title, @category, @mood)"
                # query_job = client.query(my_query)
                # insert into big query here
            elif current_category == "Podcasts":
                podcasts.append({"title": title})
                # insert into big query here
            elif current_category == "Music":
                music.append({"title": title})
                # insert into big query here

    return {"Movies": movies, "Podcasts": podcasts, "Music": music}



st.set_page_config(page_title="Mood-based Recommendations", page_icon=":heart:", layout="centered")

#write css for mood match into st.markdown
with open('trendingbuzz/moodmatch.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


# Function to generate image using Vertex AI
def generate_image(vertex_prompt, mood_strength):
    vertexai.init(project="citric-lead-411804", location="us-central1")

    vertex_model = ImageGenerationModel.from_pretrained("imagegeneration@005")

    images = vertex_model.generate_images(vertex_prompt)

    if images:
        if len(images.images) == 0:
            return "default_image.jpg"
        else:
            images[0].save("generated_image.jpg")
            return "generated_image.jpg"
    else:
        # Return a default image path if images are not generated
        return "default_image.jpg"


# Function to generate recommendations using Gemini Pro and BigQuery data
api_key = os.environ.get('API_KEY')
def generate_new_mood_recommendation(gemini_prompt, selected_mood):
    genai.configure(api_key=api_key)

    functionality.create_text_model()

    bq_client = bigquery.Client()

    table_id = f"citric-lead-411804.moodmatch_01.{selected_mood.lower()}"
  
    new_recommendations = functionality.generate_content(functionality.create_text_model(), gemini_prompt + "\n")
    new_recommendations = split_rec_content(new_recommendations)
    if len(new_recommendations['Movies']) < 2 or len(new_recommendations['Music']) < 2 or len(new_recommendations['Podcasts']) < 2:
        st.error("Reload for a suitable response. Gen AI call failed at this time! Grateful for your patience 😊")

    else:
        # st.title(new_recommendations)
        my_query = f"INSERT INTO `{table_id}` (movies, music, podcasts) VALUES ('{new_recommendations['Movies'][0]['title']}', '{new_recommendations['Music'][0]['title']}', '{new_recommendations['Podcasts'][0]['title']}'), ('{new_recommendations['Movies'][1]['title']}', '{new_recommendations['Music'][1]['title']}', '{new_recommendations['Podcasts'][1]['title']}')"
        # st.title(my_query)
        query_job = bq_client.query(my_query)
        query_job.result()
    return new_recommendations
#code to clear the table 
def clear_cache(mood):
        table_id = f"citric-lead-411804.moodmatch_01.{mood.lower()}"
        my_query = (f"DELETE FROM `{table_id}` WHERE true")
        bq_client = bigquery.Client()
        query_job = bq_client.query(my_query)
        query_job.result()

def retrieve_recommendations(mood):
    table_id = f"citric-lead-411804.moodmatch_01.{mood.lower()}"
    my_query = (f"SELECT * FROM `{table_id}` LIMIT 2")
    bq_client = bigquery.Client()
    query_job = bq_client.query(my_query)
    rows = query_job.result()
    movies = []
    music = []
    podcasts = []
    for row in rows:
        movies.append({"title":row.movies})
        music.append({"title":row.music})
        podcasts.append({"title":row.podcasts})
    return {"Movies": movies, "Podcasts": podcasts, "Music": music}
# Streamlit app
st.title("KEM Entertainment Home Page")
st.write("Welcome to Mood Match. How are you feeling today?")

mood_options = ['Happy', 'Sad', 'Angry', 'Excited', 'Relaxed']
selected_mood = st.selectbox("Select A Mood below", mood_options)


# Add a slider for mood strength
mood_strength = functionality.create_slider("Rate how strongly you feel about this mood:", min_value=0, max_value=10, value=5)

summary = f"Since you are {selected_mood.lower()} and you rate this mood strength as {mood_strength} out of 10, here are some great entertainment options in forms of movies, music, and podcasts. Also, an image to follow. Check them out:"
st.write(summary)

vertex_prompt = f"A person feeling {selected_mood.lower()} with a strength rating of {mood_strength}/10"
image_path = generate_image(vertex_prompt, mood_strength)

gemini_prompt = f"2 Recommendations each for movies, podcasts, and music based on the {selected_mood.lower()} mood without summary. Use dashes as bullet points"
# recommendations = generate_new_mood_recommendation(gemini_prompt, selected_mood)
recommendations = {}
if selected_mood not in st.session_state:
    st.session_state[selected_mood] = True
    recommendations = generate_new_mood_recommendation(gemini_prompt, selected_mood)
else:
    #call get_recommendations_with_bigquery
    recommendations = retrieve_recommendations(selected_mood)
if image_path:
    st.image(Image.open(image_path), caption=f"Generated Image for {selected_mood} Mood", use_column_width=True)
    st.download_button(
        label="Download Image",
        data=open(image_path, "rb").read(),
        file_name="generated_image.jpg",
        mime="image/jpeg"
    )



with st.expander("Recommendations"):
    for category, content_list in recommendations.items():
        st.subheader(f"{category}:")
        col1, col2 = st.columns(2)
        with col1:
            mood_board1 = ""
            if category == "Movies":
                image_url = "https://as1.ftcdn.net/v2/jpg/02/07/21/78/500_F_207217831_Nt7TLENvPpIfXHo1Lqku8viDKOGLl4iy.jpg"
            elif category == "Podcasts":
                image_url = "https://img.freepik.com/premium-vector/illustration-podcasting-microphone-recording_183875-720.jpg"
            elif category == "Music":
                image_url = "https://3.bp.blogspot.com/-p0ZQ9a-EWo4/T4SOL7e3a3I/AAAAAAAAH9E/-Oc4dg7SmS4/s1600/eighth+notes.jpg"

            mood_board1 += f"""
                <div class='mood-item'>
                    <img src="{image_url}" alt='Image' width="150" height="150">
                    <h3>{content_list[0]["title"]}</h3>
                </div>
            """
            st.markdown(mood_board1, unsafe_allow_html=True)
        with col2:
            mood_board2 = ""
            if category == "Movies":
                image_url = "https://as1.ftcdn.net/v2/jpg/02/07/21/78/500_F_207217831_Nt7TLENvPpIfXHo1Lqku8viDKOGLl4iy.jpg"
            elif category == "Podcasts":
                image_url = "https://img.freepik.com/premium-vector/illustration-podcasting-microphone-recording_183875-720.jpg"
            elif category == "Music":
                image_url = "https://3.bp.blogspot.com/-p0ZQ9a-EWo4/T4SOL7e3a3I/AAAAAAAAH9E/-Oc4dg7SmS4/s1600/eighth+notes.jpg"

            mood_board2 += f"""
                <div class='mood-item'>
                    <img src="{image_url}" alt='Image' width="150" height="150">
                    <h3>{content_list[1]["title"]}</h3>
                </div>
            """
            st.markdown(mood_board2, unsafe_allow_html=True)
clear = st.button("clear cache")
if clear:
    for mood in mood_options:
        clear_cache(mood)




