import streamlit as st
import whisper

st.title("Pronunciation Feedback Tool")

# Upload audio file
audio_file = st.file_uploader("Upload your recording (WAV/MP3)", type=["wav", "mp3"])

# Load Whisper model
model = whisper.load_model("tiny")

if audio_file is not None:
    st.audio(audio_file, format='audio/wav')
    st.success("Audio uploaded successfully!")

    # Save uploaded file temporarily
    with open("temp_audio." + audio_file.name.split(".")[-1], "wb") as f:
        f.write(audio_file.getbuffer())

    # Transcribe audio
    result = model.transcribe("temp_audio." + audio_file.name.split(".")[-1])
    spoken_text = result["text"].lower()
    st.text_area("Transcribed Text", value=spoken_text)

    # Input target sentence
    target_text = st.text_input("Enter the target sentence:").lower()

    if target_text:
        words_spoken = set(spoken_text.split())
        words_target = set(target_text.split())

        correct = words_spoken & words_target
        missing = words_target - words_spoken
        extra = words_spoken - words_target

        st.write(f"✅ Correct words: {', '.join(correct)}")
        st.write(f"❌ Missing words: {', '.join(missing)}")
        st.write(f"⚠️ Extra words: {', '.join(extra)}")

        if words_target:
            accuracy = len(correct) / len(words_target) * 100
            st.metric("Pronunciation Accuracy", f"{accuracy:.1f}%")
