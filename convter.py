import os
import urllib.request
import zipfile
from pydub import AudioSegment
import streamlit as st

# URL to download FFmpeg zip (official)
FFMPEG_ZIP_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"

def setup_ffmpeg():
    ffmpeg_exe_path = os.path.abspath("ffmpeg/ffmpeg.exe")
    
    if not os.path.exists(ffmpeg_exe_path):
        st.info("Downloading FFmpeg... please wait ⏳")
        
        # Download the zip file
        urllib.request.urlretrieve(FFMPEG_ZIP_URL, "ffmpeg.zip")

        # Extract it
        with zipfile.ZipFile("ffmpeg.zip", 'r') as zip_ref:
            zip_ref.extractall("ffmpeg_dir")

        # Find and move ffmpeg.exe
        for root, dirs, files in os.walk("ffmpeg_dir"):
            for file in files:
                if file == "ffmpeg.exe":
                    found_path = os.path.join(root, file)
                    os.makedirs("ffmpeg", exist_ok=True)
                    os.rename(found_path, ffmpeg_exe_path)
                    break

    # ✅ Set pydub to use this ffmpeg.exe
    AudioSegment.converter = ffmpeg_exe_path
    return ffmpeg_exe_path

# Call setup function
ffmpeg_path = setup_ffmpeg()

st.title("🎵 Audio to MP3 Converter")

uploaded_file = st.file_uploader("Upload audio file", type=["wav", "ogg", "flac", "aac", "m4a", "wma"])

if uploaded_file:
    st.success("✅ File uploaded successfully!")

    try:
        # ✅ Set converter again to be sure
        AudioSegment.converter = ffmpeg_path

        # Convert to MP3
        audio = AudioSegment.from_file(uploaded_file)
        output_path = "converted_output.mp3"
        audio.export(output_path, format="mp3")

        st.success("✅ Conversion completed!")

        # Offer download
        with open(output_path, "rb") as f:
            st.download_button("⬇️ Download MP3", f, file_name="converted.mp3")

    except Exception as e:
        st.error(f"❌ Conversion failed: {e}")
