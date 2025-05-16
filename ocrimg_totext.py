import streamlit as st
from PIL import Image
import numpy as np
import easyocr
from io import BytesIO

# Set page config
st.set_page_config(page_title="Image Text Extractor", page_icon="🔍")

# Footer
st.markdown("""
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    text-align: center;
    padding: 10px;
    background: transparent;
    color: gray;
}
</style>
<div class="footer">Made with love ❤️ Nilesh Mete</div>
""", unsafe_allow_html=True)

# App UI
st.title("🔍 Image Text Extractor")
st.markdown("Upload an image to extract text using OCR.")

# Language selection
language = st.selectbox(
    "Select Language",
    ("English", "French", "Spanish", "German", "Hindi"),
    index=0
)

language_codes = {
    "English": "en",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Hindi": "hi"
}

# File uploader
uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    if st.button("Extract Text"):
        with st.spinner("Extracting text..."):
            reader = easyocr.Reader([language_codes[language]])
            result = reader.readtext(np.array(image))
            extracted_text = "\n".join([text[1] for text in result])
            
            st.success("Done!")
            st.text_area("Extracted Text", extracted_text, height=200)
            
            # Download button
            txt_file = BytesIO()
            txt_file.write(extracted_text.encode("utf-8"))
            txt_file.seek(0)
            st.download_button(
                "Download Text",
                data=txt_file,
                file_name="extracted_text.txt",
                mime="text/plain"
            )