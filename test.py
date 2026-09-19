from dotenv import load_dotenv
load_dotenv()   # MUST be before any core/ imports

from utils.audio_processer import process_input
from core.transcriber import transcribe_all
from core.summerizer import analyze_transcript

source = "https://www.youtube.com/watch?v=qYNweeDHiyU"  # Put your YouTube URL or local file path here
language = "english"

chunks = process_input(source)

transcript = transcribe_all(chunks, language=language)
print("\n" + "=" * 60)
print("📝 TRANSCRIPT")
print("=" * 60)
print(transcript[:500] + "..." if len(transcript) > 500 else transcript)


analysis = analyze_transcript(transcript)

print("\n" + "=" * 60)
print(f"📌 TITLE: {analysis['title']}")
print("=" * 60)
print("\n📋 SUMMARY")
print("-" * 60)
print("\n".join(f"- {item}" for item in analysis["summary"]))

print("\n" + "=" * 60)
print("✅ ACTION ITEMS")
print("=" * 60)
print("\n".join(f"- {item}" for item in analysis["action_items"]) or "None found.")

print("\n" + "=" * 60)
print("🔑 KEY DECISIONS")
print("=" * 60)
print("\n".join(f"- {item}" for item in analysis["key_decisions"]) or "None found.")

print("\n" + "=" * 60)
print("❓ OPEN QUESTIONS")
print("=" * 60)
print("\n".join(f"- {item}" for item in analysis["open_questions"]) or "None found.")