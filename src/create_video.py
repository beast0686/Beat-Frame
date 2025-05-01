import json
import os
from pathlib import Path
from moviepy import AudioFileClip, CompositeVideoClip, ImageClip

# Get the absolute path to the root directory and audio file
ROOT_DIR = Path(__file__).parent.parent  # Adjust path to root directory
audio_path = ROOT_DIR / "music" / "song.mp3"

# Check if audio file exists
if not audio_path.exists():
    print(f"Error: Audio file '{audio_path}' not found!")
    exit(1)

# === Load audio ===
try:
    audio_clip = AudioFileClip(str(audio_path))
    audio_duration = audio_clip.duration
except Exception as e:
    print(f"Error loading audio file: {e}")
    exit(1)

# === Load lyrics segments with timestamps ===
segments_path = ROOT_DIR / "assets" / "lyrics_segments.json"
if not segments_path.exists():
    print(f"Error: Segments file '{segments_path}' not found!")
    exit(1)

with open(segments_path) as f:
    segments = json.load(f)

# === Load available image frames ===
image_folder = ROOT_DIR / "images"
image_files = sorted([f for f in os.listdir(image_folder) if f.endswith(".png")])

if not image_files:
    raise RuntimeError("No images found in 'images/' folder.")

# === Create image clips based on segment timings ===
clips = []
num_images = len(image_files)

for i, segment in enumerate(segments):
    start = segment["start"]
    end = segment["end"]
    duration = end - start

    image_path = os.path.join(image_folder, image_files[i % num_images])
    img = ImageClip(image_path).with_start(start).with_duration(duration)
    clips.append(img)

# === Composite video with image overlays ===
video = CompositeVideoClip(clips, size=(512, 512)).with_duration(audio_duration)

# === Add audio and export ===
video = video.with_audio(audio_clip)

# Ensure output folder exists
output_folder = ROOT_DIR / "video"
output_folder.mkdir(exist_ok=True)

# Export video
output_path = output_folder / "final_music_video.mp4"
try:
    video.write_videofile(str(output_path), fps=24)
    print(f"Video successfully created at {output_path}")
except Exception as e:
    print(f"Error during video export: {e}")
