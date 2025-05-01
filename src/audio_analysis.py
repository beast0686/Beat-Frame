import librosa
import json
import numpy as np
from pathlib import Path

# Define absolute path to the song
ROOT_DIR = Path(__file__).parent.parent
song_path = ROOT_DIR / "music" / "song.mp3"

# Load the song
y, sr = librosa.load(song_path)
tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
beat_times = librosa.frames_to_time(beats, sr=sr)

# Save beat times to a JSON file
beat_times_path = ROOT_DIR / "assets" / "beat_times.json"
with open(beat_times_path, "w") as f:
    json.dump(beat_times.tolist(), f)

# Determine tempo
if isinstance(tempo, (list, np.ndarray)):
    tempo_val = float(tempo[0])
else:
    tempo_val = float(tempo)

print(f"Tempo: {tempo_val:.2f} BPM")
print(f"Saved {len(beat_times)} beat timestamps.")
