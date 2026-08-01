import streamlit as st
import whisper
import os
import tempfile
from datetime import timedelta

st.set_page_config(page_title="Video to SRT Converter", page_icon="🎬")

st.title("🎬 Audio/Video to SRT Converter")
st.write("Video သို့မဟုတ် Audio ဖိုင်တင်ပြီး SRT Subtitle ဖိုင် ရယူပါ။")

@st.cache_resource
def load_model():
    return whisper.load_model("base")

st.info("💡 Whisper Model ကို ခေါ်ယူနေပါသည်...")
model = load_model()

def format_timestamp(seconds: float):
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def generate_srt(transcript):
    srt_content = ""
    for i, segment in enumerate(transcript['segments'], start=1):
        start = format_timestamp(segment['start'])
        end = format_timestamp(segment['end'])
        text = segment['text'].strip()
        srt_content += f"{i}\n{start} --> {end}\n{text}\n\n"
    return srt_content

uploaded_file = st.file_uploader("Upload Video/Audio", type=["mp4", "mp3", "wav", "m4a", "mov"])

if uploaded_file is not None:
    if st.button("Generate SRT 🚀"):
        with st.spinner("Processing... ခဏစောင့်ပါ..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_path = tmp_file.name

            try:
                result = model.transcribe(tmp_path)
                srt_output = generate_srt(result)
                
                st.success("အောင်မြင်စွာ ပြီးဆုံးပါပြီ!")
                st.text_area("SRT Preview", srt_output, height=200)

                st.download_button(
                    label="📥 Download .srt File",
                    data=srt_output,
                    file_name=f"{os.path.splitext(uploaded_file.name)[0]}.srt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
