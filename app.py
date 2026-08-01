import streamlit as st
from src.transcriber import Transcriber
from src.srt_formatter import generate_srt

# Streamlit Page Configuration
st.set_page_config(page_title="AI Video/Audio to SRT Converter", page_icon="🎙️", layout="centered")

st.title("🎙️ AI Subtitle Generator (Video/Audio → SRT)")
st.write("Upload your media file to automatically generate `.srt` subtitles using OpenAI Whisper.")

# Model Options
model_size = st.sidebar.selectbox("Select Model Size", ["tiny", "base", "small", "medium"], index=1)

# File Uploader
uploaded_file = st.file_uploader("Choose a Video or Audio file", type=["mp3", "wav", "mp4", "mkv", "mov", "m4a"])

if uploaded_file is not None:
    st.info(f"File uploaded: **{uploaded_file.name}** ({round(uploaded_file.size / (1024*1024), 2)} MB)")
    
    if st.button("Generate SRT Subtitles", type="primary"):
        with st.spinner("Transcribing media... This may take a moment."):
            try:
                # Load transcriber
                transcriber = Transcriber(model_size=model_size)
                
                # Get extension
                file_ext = f".{uploaded_file.name.split('.')[-1]}"
                
                # Perform transcription
                segments = transcriber.transcribe(uploaded_file.read(), file_ext)
                
                # Format to SRT
                srt_content = generate_srt(segments)
                
                st.success("Transcription complete!")
                
                # Preview SRT
                with st.expander("Preview SRT Output"):
                    st.text_area("SRT Content", srt_content, height=250)
                
                # Download Button
                srt_filename = f"{uploaded_file.name.rsplit('.', 1)[0]}.srt"
                st.download_button(
                    label="📥 Download SRT File",
                    data=srt_content,
                    file_name=srt_filename,
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                
