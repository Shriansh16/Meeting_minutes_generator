import streamlit as st
from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, start
from openai import OpenAI
from pydub import AudioSegment
from pydub.utils import make_chunks
import os
import glob
from dotenv import load_dotenv
from crews.meeting_minutes_crew.meeting_minutes_crew import MeetingMinutesCrew

import agentops

load_dotenv()
client = OpenAI()

class MeetingMinutesState(BaseModel):
    transcript: str = ""
    meeting_minutes: str = ""

class MeetingMinutesFlow(Flow[MeetingMinutesState]):

    @start()
    def transcribe_meeting(self, audio_path):
        # Load the audio file
        audio = AudioSegment.from_file(audio_path, format="wav")

        # Split into chunks for processing
        chunk_length_ms = 60000
        chunks = make_chunks(audio, chunk_length_ms)

        # Transcribe each chunk
        full_transcription = ""
        chunk_files = []  # Store chunk filenames for cleanup

        for i, chunk in enumerate(chunks):
            chunk_path = f"chunk_{i}.wav"
            chunk.export(chunk_path, format="wav")
            chunk_files.append(chunk_path)  # Track file for cleanup
            
            with open(chunk_path, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file
                )
                full_transcription += transcription.text + " "

        self.state.transcript = full_transcription

        # Cleanup chunk files
        for file in chunk_files:
            os.remove(file)

    @listen(transcribe_meeting)
    def generate_meeting_minutes(self):
        crew = MeetingMinutesCrew()
        inputs = {"transcript": self.state.transcript}
        meeting_minutes = crew.crew().kickoff(inputs)
        self.state.meeting_minutes = str(meeting_minutes)

        return self.state.meeting_minutes

# Streamlit UI
st.title("📜 AI Meeting Minutes Writer")

uploaded_file = st.file_uploader("Upload a WAV file", type=["wav"])

if uploaded_file:
    # Save uploaded file
    file_path = "uploaded_audio.wav"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    # Show loading spinner while processing
    with st.spinner("Processing audio and generating meeting minutes..."):
        meeting_minutes_flow = MeetingMinutesFlow()
        meeting_minutes_flow.transcribe_meeting(file_path)
        meeting_minutes = meeting_minutes_flow.generate_meeting_minutes()

    # Delete uploaded audio file after processing
    if os.path.exists(file_path):
        os.remove(file_path)

    # Display Meeting Minutes
    st.subheader("📝 Meeting Minutes")
    st.markdown(meeting_minutes)
