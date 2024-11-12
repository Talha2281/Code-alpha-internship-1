# app.py

import streamlit as st
from googletrans import Translator
from gtts import gTTS
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
st.title("Language Translator")
st.write("This application is created by TALHA KHAN")
# User input for text to translate
text = st.text_area("Enter text to translate")

# Dropdown for source and target languages
source_language = st.selectbox("Select source language", options=language_codes.keys())
target_language = st.selectbox("Select target language", options=language_codes.keys())

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

            # Text-to-Speech for Translated Text
            if st.button("Play Translated Text"):
                tts = gTTS(text=translated_text, lang=language_codes[target_language])
                tts.save("translated_audio.mp3")
                st.audio("translated_audio.mp3", format="audio/mp3")

            # Save as PDF or Text file
            if st.button("Save as PDF"):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.cell(200, 10, txt="Translation", ln=True, align="C")
                pdf.cell(200, 10, txt="Original Text:", ln=True)
                pdf.multi_cell(0, 10, txt=text)
                pdf.cell(200, 10, txt="Translated Text:", ln=True)
                pdf.multi_cell(0, 10, txt=translated_text)
                pdf.output("translation.pdf")
                with open("translation.pdf", "rb") as file:
                    st.download_button("Download PDF", file, file_name="translation.pdf")

            if st.button("Save as Text File"):
                with open("translation.txt", "w") as file:
                    file.write(f"Original Text:\n{text}\n\nTranslated Text:\n{translated_text}")
                with open("translation.txt", "rb") as file:
                    st.download_button("Download Text File", file, file_name="translation.txt")

        except Exception as e:
            st.error(f"Translation failed: {str(e)}")
    else:
        st.warning("Please enter text to translate.")

# Feedback system
st.subheader("Feedback")
feedback = st.radio("Was the translation helpful?", ("👍 Yes", "👎 No"))
if feedback == "👍 Yes":
    st.write("Thank you for your feedback!")
elif feedback == "👎 No":
    st.write("We appreciate your feedback and will work to improve.")

