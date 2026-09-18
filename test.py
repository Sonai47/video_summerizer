from utils.audio_processer import process_input
from core.transcriber import transcribe_all

source = "https://www.youtube.com/watch?v=qYNweeDHiyU"  # Put your YouTube URL or local file path here

chunks = process_input(source)

print(transcribe_all(chunks))