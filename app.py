import streamlit as st
import subprocess
import sys
from pathlib import Path

# === Setup paths ===
ROOT_DIR = Path(__file__).parent
SRC_DIR = ROOT_DIR / "src"
MUSIC_DIR = ROOT_DIR / "music"
ASSETS_DIR = ROOT_DIR / "assets"
IMAGES_DIR = ROOT_DIR / "images"
VIDEO_DIR = ROOT_DIR / "video"

# === Ensure necessary folders exist ===
for directory in [MUSIC_DIR, ASSETS_DIR, IMAGES_DIR, VIDEO_DIR]:
    directory.mkdir(exist_ok=True)

# === Streamlit Page Config ===
st.set_page_config(page_title="🎶 Beat Frame", layout="centered")

# === Elegant Header ===
st.markdown("""
    <div style='text-align: center;'>
        <h1 style='color: #ff4b4b;'>🎶 Beat Frame</h1>
        <p style='font-size: 18px;'>Turn any MP3 track into a stunning AI-generated music video with visuals synced to lyrics and beats.</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# === File Uploader ===
uploaded_file = st.file_uploader("📤 Upload your MP3 file", type=["mp3"], help="Only .mp3 files are supported")

def run_script(script_path, step_label, step_index, progress_bar, step_status, total_steps):
    step_status.markdown(f"🟡 <b>{step_label}</b> — <i>In progress...</i>", unsafe_allow_html=True)
    result = subprocess.run([sys.executable, str(script_path)])
    if result.returncode != 0:
        step_status.markdown(f"🔴 <b>{step_label}</b> — <i>Failed</i>", unsafe_allow_html=True)
        raise subprocess.CalledProcessError(result.returncode, script_path)
    step_status.markdown(f"🟢 <b>{step_label}</b> — <i>Completed</i>", unsafe_allow_html=True)
    progress_bar.progress((step_index + 1) / total_steps)

if uploaded_file:
    # Save uploaded song
    song_path = MUSIC_DIR / "song.mp3"
    with open(song_path, "wb") as f:
        f.write(uploaded_file.read())
    st.success("✅ Song uploaded successfully!")

    if st.button("🚀 Generate Music Video"):
        try:
            steps = [
                ("🔍 Step 1: Detecting beats", SRC_DIR / "audio_analysis.py"),
                ("📝 Step 2: Transcribing lyrics", SRC_DIR / "transcribe_lyrics.py"),
                ("🎨 Step 3: Generating image prompts", SRC_DIR / "prompt_generation.py"),
                ("🖼️ Step 4: Generating images", SRC_DIR / "generate_images.py"),
                ("🎬 Step 5: Creating final video", SRC_DIR / "create_video.py"),
            ]

            st.markdown("### 🔄 Generation Progress")
            progress_bar = st.progress(0)
            step_status_containers = [st.empty() for _ in steps]

            for idx, (label, script) in enumerate(steps):
                run_script(script, label, idx, progress_bar, step_status_containers[idx], len(steps))

            final_video_path = VIDEO_DIR / "final_music_video.mp4"

            if final_video_path.exists():
                st.balloons()
                st.success("✅ Your music video is ready!")

                # 🎞️ Show video preview
                st.video(str(final_video_path))

                # ⬇️ Provide download option
                with open(final_video_path, "rb") as f:
                    st.download_button(
                        label="⬇️ Download Final Video",
                        data=f,
                        file_name="final_music_video.mp4",
                        mime="video/mp4"
                    )

            else:
                st.error("❌ Final video not found. Please check the logs for errors.")

        except subprocess.CalledProcessError as e:
            st.error(f"🚨 An error occurred during processing:\n\n{e}")
