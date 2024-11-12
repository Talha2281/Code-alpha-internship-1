# app.py

import streamlit as st
from googletrans import Translator

# Initialize the Translator
translator = Translator()

# Inject custom CSS for Urdu font
def apply_custom_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu&display=swap');

        .urdu-text {
            font-family: 'Noto Nastaliq Urdu', sans-serif;
            font-size: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Call the function to apply the custom CSS
apply_custom_css()

# List of language options
language_codes = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese (Simplified)": "zh-cn",
    "Chinese (Traditional)": "zh-tw",
    "Hindi": "hi",
    "Urdu": "ur",
    "Arabic": "ar",
    "Russian": "ru",
    "Japanese": "ja",
    "Korean": "ko"
}

# Streamlit app title
st.title("Language Translator")
st.write("This translator is created by TALHA KHAN")

# User input for text to translate
text = st.text_area("Enter text to translate")

# Dropdown for source and target languages
source_language = st.selectbox("Select source language", options=language_codes.keys())
target_language = st.selectbox("Select target language", options=language_codes.keys())

# Translate button
if st.button("Translate"):
    if text:
        # Translate the text
        try:
            translated_text = translator.translate(
                text, 
                src=language_codes[source_language], 
                dest=language_codes[target_language]
            ).text
            # Display the translated text with Urdu font if target is Urdu
            if target_language == "Urdu":
                st.markdown(f"<p class='urdu-text'>{translated_text}</p>", unsafe_allow_html=True)
            else:
                st.write("Translated Text:", translated_text)
        except Exception as e:
            st.error(f"Translation failed: {str(e)}")
    else:
        st.warning("Please enter text to translate.")

 
      
