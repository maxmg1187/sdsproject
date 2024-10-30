from moodmatch import retrieve_recommendations 
from moodmatch import *
import functionality
from functionality import simulate_download_button_click 

# test initial state of recommendations for a default mood
def test_initial_state():
    # Assuming default or initial mood
    default_mood = 'Happy'
    recommendations = retrieve_recommendations(default_mood)
    assert isinstance(recommendations, dict), "Expected recommendations to be a dictionary"
    assert all(k in recommendations for k in ["Movies", "Podcasts", "Music"]), "Missing categories in recommendations"


#test the mood strength slider
def test_slider_value():
    # Test if the slider value falls within the specified range
    min_value = 0
    max_value = 10
    default_value = 5
    slider_value = functionality.create_slider("Test Slider", min_value, max_value, default_value)
    assert min_value <= slider_value <= max_value



#test that the download button for AI generated image is clicked
def test_download_button():
    # Simulate the download button click
    downloaded_content = simulate_download_button_click()
    
    # Define the expected file content
    expected_file_content = open("generated_image.jpg", "rb").read()
    
    # Assert that the downloaded content matches the expected file content
    assert downloaded_content == expected_file_content
