# app.py

import streamlit as st
from googletrans import Translator
from fpdf import FPDF
import os

# Initialize the Translator
translator = Translator()

# Inject custom CSS for Urdu font (Optional)
def apply_custom_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu&display=swap');
        .urdu-text { font-family: 'Noto Nastaliq Urdu', sans-serif; font-size: 20px; }
        </style>
        """, unsafe_allow_html=True
    )

apply_custom_css()

# List of language options
language_codes = {
    "Auto-Detect": "auto",
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
st.title("Enhanced Language Translator")

# User input for text to translate
text = st.text_area("Enter text to translate")

# Scrollable language selection with proper handling of selected values
source_language = st.multiselect(
    "Select source language", 
    options=language_codes.keys(),
    default=["Auto-Detect"], 
    max_selections=1
)

target_language = st.multiselect(
    "Select target language", 
    options=language_codes.keys(),
    default=["English"], 
    max_selections=1
)

# Ensure that a language is selected
if source_language:
    source_language = source_language[0]  # Get the first selected language
else:
    source_language = "Auto-Detect"

if target_language:
    target_language = target_language[0]  # Get the first selected language
else:
    target_language = "English"

# Translate button
if st.button("Translate"):
    if text:
        try:
            # Detect language if "Auto-Detect" is selected
            if language_codes[source_language] == "auto":
                detected_lang = translator.detect(text).lang
                source_language = next(
                    (lang for lang, code in language_codes.items() if code == detected_lang),
                    "Detected Language"
                )
                st.write(f"Detected Source Language: {source_language}")

            # Translate the text
            translated_text = translator.translate(
                text,
                src=language_codes[source_language] if source_language != "Auto-Detect" else "auto",
                dest=language_codes[target_language]
            ).text

            # Display the translated text
            if target_language == "Urdu":
                st.markdown(f"<p class='urdu-text'>{translated_text}</p>", unsafe_allow_html=True)
            else:
                st.write("Translated Text:", translated_text)

        except Exception as e:
            st.error(f"Translation failed: {str(e)}")
    else:
        st.warning("Please enter text to translate.")
