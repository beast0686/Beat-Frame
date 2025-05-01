import whisper
import os
import json
from pathlib import Path

# Define absolute path to the song
ROOT_DIR = Path(__file__).parent.parent  # Go up two directories from the script
audio_path = str(ROOT_DIR / "music" / "song.mp3")  # Convert to string
lyrics_path = ROOT_DIR / "assets" / "lyrics.txt"
segments_path = ROOT_DIR / "assets" / "lyrics_segments.json"

# Load Whisper model
print("Loading Whisper model...")
model = whisper.load_model("base")

# Transcribe the song
print("Transcribing audio...")
result = model.transcribe(audio_path)

# Save raw text (optional)
text = result["text"]

# Save cleaned lines
lines = []
segments = []

for segment in result["segments"]:
    start = segment["start"]
    end = segment["end"]
    line = segment["text"].strip().capitalize()
    if line:
        lines.append(line)
        segments.append({
            "start": start,
            "end": end,
            "text": line
        })

# Save lyrics as plain text
with open(lyrics_path, "w") as f:
    f.write("\n".join(lines))

# Save timestamped segments as JSON
with open(segments_path, "w") as f:
    json.dump(segments, f, indent=2)

print(f"Transcribed {len(lines)} lines")
