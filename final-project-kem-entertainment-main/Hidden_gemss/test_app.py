import unittest 
import hidden  # Replace with the name of your Streamlit app file

class TestInitialAppState(unittest.TestCase):
    def test_default_prompt(self):
        # Simulate initial app load (Exact method may vary)
        hidden.run()  

        # Access the text input element (Adjust how you retrieve it)
        prompt_input = st._get_widget_state("text_input_key") 
        self.assertEqual(prompt_input, "")

    def test_slider_value(self):
        # Similar concept as above, access the slider
        slider_value = st._get_widget_state("slider_key")  
        self.assertEqual(slider_value, 50)

    def test_session_state(self):
        self.assertFalse(st.session_state.get('generate_query', False)) 

if __name__ == '__main__':
    unittest.main()
