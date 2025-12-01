import streamlit as st
import whisper

# App title
st.title("Pronunciation Feedback Tool")

# Upload audio file
audio_file = st.file_uploader("Upload your recording (WAV/MP3)", type=["wav", "mp3"])

# Load Whisper model
model = whisper.load_model("tiny")  # lightweight, fast

if audio_file is not None:
    # Play audio
    st.audio(audio_file, format='audio/wav')
    st.success("Audio uploaded successfully!")

    # Save temporarily
    with open("temp_audio.wav", "wb") as f:
        f.write(audio_file.getbuffer())

    # Transcribe audio
    result = model.transcribe("temp_audio.wav")
    spoken_text = result["text"].lower()
    st.text_area("Transcribed Text", value=spoken_text)

    # Input target sentence
    target_text = st.text_input("Enter the target sentence:").lower()

    if target_text:
        # Split into words
        words_spoken = set(spoken_text.split())
        words_target = set(target_text.split())

        # Compare
        correct = words_spoken & words_target
        missing = words_target - words_spoken
        extra = words_spoken - words_target

        # Show results
        st.write(f"✅ Correct words: {', '.join(correct)}")
        st.write(f"❌ Missing words: {', '.join(missing)}")
        st.write(f"⚠️ Extra words: {', '.join(extra)}")

        # Accuracy
        if words_target:
            accuracy = len(correct) / len(words_target) * 100
            st.metric("Pronunciation Accuracy", f"{accuracy:.1f}%")
