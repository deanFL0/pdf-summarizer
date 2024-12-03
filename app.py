import streamlit as st
import os
import json
from utils import *

def main():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    GOOGLE_API_KEY = config.get('GOOGLE_API_KEY')
    os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY

    st.set_page_config(page_title="PDF Summarizer", page_icon="📄", layout="centered", initial_sidebar_state="expanded")
    st.title("PDF Summarizer")
    st.write("Upload a PDF file and get a summary of the text in the document.")
    st.divider()

    pdf = st.file_uploader("Choose a PDF file", type=["pdf"])
    submit_button = st.button("Summarize")
    
    if submit_button:
        with st.spinner("Summarizing the document..."):
            response = summarizer(pdf)
            st.subheader("Summary of the document:")
            st.write(response)

if __name__ == "__main__":
    main()