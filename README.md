# AI Meeting Minutes Writer

## Overview
This project is an AI-powered **Meeting Minutes Writer** that transcribes audio meetings, extracts key points, generates structured summaries, and performs sentiment analysis. It utilizes **Streamlit**, **OpenAI's Whisper model**, and **CrewAI agents** to automate the meeting documentation process.

## Features
- **Audio Transcription**: Uses OpenAI's Whisper model to convert meeting recordings into text.
- **Automated Meeting Minutes Generation**: Extracts key discussions, decisions, action items, and sentiment analysis.
- **Structured Output**: Saves summaries, action items, and sentiment analysis in separate files.
- **Streamlit UI**: Simple web interface to upload audio and generate meeting minutes.

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- pip

### Clone the Repository
```bash
git clone <repository-url>
cd <project-folder>
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Set Up Environment Variables
Create a `.env` file and add your OpenAI API key:
```env
OPENAI_API_KEY=your_openai_api_key
```

## Usage
### Run the Streamlit App
```bash
streamlit run src\meeting_minutes\app.py
```

### Upload a Meeting Audio File
1. Open the web interface.
2. Upload a `.wav` audio file.
3. The AI will transcribe and generate meeting minutes.

## Project Structure
```
.
├── meeting_minutes_crew/
│   ├── meeting_minutes_crew.py
│   ├── config/
│   │   ├── agents.yaml
│   │   ├── tasks.yaml
├── app.py
├── requirements.txt
├── .env (not included in repo)
└── README.md
```

## Configuration
### Agent Configuration (`config/agents.yaml`)
Defines AI agent roles, responsibilities, and tools.
```yaml
meeting_minutes_summarizer:
  role: "CrewAI Meeting Minutes Summarizer"
  goal: "Summarize meetings, extract action items, analyze sentiment."
meeting_minutes_writer:
  role: "CrewAI Meeting Minutes Writer"
  goal: "Compile professional meeting minutes."
```

### Task Configuration (`config/tasks.yaml`)
Defines specific tasks assigned to each agent.
```yaml
meeting_minutes_summary_task:
  description: "Summarize the meeting transcript."
meeting_minutes_writing_task:
  description: "Generate a structured meeting minutes document."
```

## Future Enhancements
- Support for multiple audio formats (MP3, M4A, etc.)
- Speaker diarization to identify different speakers
- Integration with calendar and email systems for automated reporting



