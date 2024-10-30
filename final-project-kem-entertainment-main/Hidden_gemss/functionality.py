import streamlit as st
import google.generativeai as genai

def generate_content(model, prompt):
    return model.generate_content(prompt)

def create_slider(text, min_value, max_value, value):
    return st.slider(text, min_value, max_value, value)

def create_text_model():
    return genai.GenerativeModel('gemini-pro')