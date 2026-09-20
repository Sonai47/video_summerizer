# AI Video Assistant

An AI-powered project that downloads audio from a YouTube video or reads a local media file, converts it into a processable format, transcribes it using Whisper, summarizes the content, and lets you ask questions about the transcript using a local RAG pipeline.

It is designed for:
- YouTube video analysis
- Meeting or lecture summaries
- Transcript-based Q&A
- Local AI processing without needing a full cloud workflow

## Features

- Download audio from YouTube links
- Convert audio/video files to WAV format
- Split long files into smaller chunks for transcription
- Transcribe using OpenAI Whisper
- Summarize the transcript with an LLM
- Extract action items, decisions, and open questions
- Ask follow-up questions using a vector-based retrieval system
- Run in Streamlit UI or from the terminal

## Project structure

- `app.py` – Streamlit web app
- `main.py` – Command-line pipeline
- `core/` – transcription, summarization, LLM, and RAG logic
- `utils/audio_processer.py` – audio download, conversion, and chunking

## Requirements

Before using the project, make sure you have:

- Python 3.10+
- Git
- FFmpeg installed and available on your system
- An API key for Mistral if you are using the Mistral model
- Optional: Ollama installed if you want to use a local LLM instead

## Download the project

Clone the repository:

```bash
git clone https://github.com/Sonai47/video_summerizer.git
cd VIDEO AGENT
```

If you already have the project folder, open it in VS Code or a terminal.

## Set up a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Whisper for transcription
- yt-dlp for YouTube audio extraction
- Pydub and FFmpeg helpers
- LangChain + Mistral/Ollama support
- ChromaDB for retrieval
- Streamlit for the UI

## Install FFmpeg

This project uses FFmpeg for audio conversion and extraction.

### Windows

You can install FFmpeg with winget:

```powershell
winget install Gyan.Dev.FFmpeg
```

Then confirm:

```powershell
ffmpeg -version
```

If your installation path is different from the one in `utils/audio_processer.py`, update the `FFMPEG_DIR` variable to match your FFmpeg folder.

### macOS

```bash
brew install ffmpeg
```

### Linux

```bash
sudo apt install ffmpeg
```

## Configure environment variables

Create a file named `.env` in the project root and add the following:

```env
LLM_PROVIDER=mistral
MISTRAL_API_KEY=your_mistral_api_key_here
MISTRAL_MODEL=mistral-small-latest
```

If you want to use Ollama instead of Mistral:

```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=qwen2.5:1.5b
```

> The app uses `load_dotenv()`, so the values in `.env` will be loaded automatically.

## Run the app with Streamlit

Start the web interface:

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

Use the UI to:
1. Paste a YouTube URL or choose a local file
2. Select the preferred language
3. Run the pipeline
4. View the transcript, summary, decisions, and questions
5. Ask follow-up questions about the content

## Run from the terminal

You can also use the CLI version:

```bash
python main.py
```

When prompted:

- Enter a YouTube URL or local file path
- Choose the language (for example: `english`). (For now it only support English. Later we add more)
- The script will process the file and print the result
- You can then type questions to chat with the transcript data

Example:

```text
Enter YouTube URL or local file path: https://www.youtube.com/watch?v=example
Language (english/hinglish): english
```

## How it works

The system follows this flow:

1. Audio is downloaded or loaded from the source
2. The file is converted to WAV
3. Audio is split into chunks
4. Whisper transcribes each chunk
5. The transcript is sent to the LLM for summary and extraction
6. The transcript is stored in a vector database
7. You can ask questions and get answers from the stored context

## Common issues

### FFmpeg not found
- Install FFmpeg and confirm it is in your PATH
- Or update `FFMPEG_DIR` in `utils/audio_processer.py`

### Mistral API key error
- Make sure `.env` exists
- Confirm the key is valid
- Check that `LLM_PROVIDER` is set correctly

### Whisper model download is slow
- The first run may take time because Whisper downloads the required model
- This is normal on the first startup

### Streamlit app does not open
- Run from the project folder
- Ensure the virtual environment is activated
- Check if all dependencies were installed successfully

## Notes

This project is best suited for local AI workflows and personal productivity tools. It can be extended with:
- better summarization prompts
- multilingual support
- PDF export
- more file formats
- custom meeting templates

## License

This project is for personal and educational use unless a different license is specified by the repository owner.
