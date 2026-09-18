import whisper
import os


WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")


_model = None


def normalize_language(language: str | None) -> str | None:
    if language is None:
        return None

    lang = language.strip().lower()
    mapping = {
        "english": "en",
        "spanish": "es",
        "french": "fr",
        "german": "de",
        "italian": "it",
        "portuguese": "pt",
        "russian": "ru",
        "japanese": "ja",
        "korean": "ko",
        "chinese": "zh",
    }
    return mapping.get(lang, lang)


def load_model():

    global _model

    if _model is None:
        print(f"Loading Whisper model: {WHISPER_MODEL} ...")
        _model = whisper.load_model(WHISPER_MODEL)
        print("Whisper model loaded.")
    return _model 


def transcribe_chunk(chunk_path: str, translate: bool = False, language: str | None = None) -> str:
    model = load_model()

    task = "translate" if translate else "transcribe"
    whisper_language = normalize_language(language)

    kwargs = {"task": task}
    if whisper_language:
        kwargs["language"] = whisper_language

    result = model.transcribe(chunk_path, **kwargs)

    return result["text"]


def transcribe_all(chunks: list, translate: bool = False, language: str | None = None) -> str:
    full_transcript = ""

    for i, chunk in enumerate(chunks):
        print(f"Transcribing chunk: {chunk} ...")
        text = transcribe_chunk(chunk, translate=translate, language=language)

        full_transcript += text + " "

    print("Transcription completed.")
    return full_transcript