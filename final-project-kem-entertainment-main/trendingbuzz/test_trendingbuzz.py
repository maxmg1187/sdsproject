from streamlit.testing.v1 import AppTest

#test that initial responses are generated on page load
def test_page_load():
    at = AppTest.from_file("trendingbuzz.py")
    at.run(timeout=15)
    assert at.session_state.loaded
    assert at.session_state.sports_response
    assert at.session_state.social_media_response
    assert at.session_state.entertainment_response


#test that a response is generated when button is clicked
def test_generate_new_trends():
    at = AppTest.from_file("trendingbuzz.py")
    at.run(timeout=10)
    at.user_prompt = "test"
    at.button[0].click().run()
    assert at.session_state.user_response

#test that query is ran and stored into session state
def test_generate_top_terms():
    at = AppTest.from_file("trendingbuzz.py")
    at.run()
    at.button[2].click().run()
    assert at.session_state.terms