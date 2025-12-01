import streamlit as st
import whisper
from pydub import AudioSegment
import io

st.title("Pronunciation Feedback Tool")

# Upload audio
audio_file = st.file_uploader("Upload your recording (WAV/MP3)", type=["wav", "mp3"])

# Load Whisper model
model = whisper.load_model("tiny")  # lightweight, fast

def convert_to_wav(file):
    # Convert mp3 to wav in memory
    audio = AudioSegment.from_file(io.BytesIO(file.read()))
    buf = io.BytesIO()
    audio.export(buf, format="wav")
    buf.seek(0)
    return buf

if audio_file is not None:
    st.audio(audio_file, format="audio/wav")
    st.success("Audio uploaded successfully!")

    # Convert uploaded file to WAV
    wav_audio = convert_to_wav(audio_file)

    # Save temporarily for Whisper
    with open("temp_audio.wav", "wb") as f:
        f.write(wav_audio.read())

    # Transcribe audio
    result = model.transcribe("temp_audio.wav")
    spoken_text = result["text"].lower()
    st.text_area("Transcribed Text", value=spoken_text)

    # Enter target sentence
    target_text = st.text_input("Enter the target sentence:").lower()

    if target_text:
        # Word-level comparison
        words_spoken = set(spoken_text.split())
        words_target = set(target_text.split())

        correct = words_spoken & words_target
        missing = words_target - words_spoken
        extra = words_spoken - words_target

        st.write(f"✅ Correct words: {', '.join(correct)}")
        st.write(f"❌ Missing words: {', '.join(missing)}")
        st.write(f"⚠️ Extra words: {', '.join(extra)}")

        # Pronunciation accuracy
        if words_target:
            accuracy = len(correct) / len(words_target) * 100
            st.metric("Pronunciation Accuracy", f"{accuracy:.1f}%")
