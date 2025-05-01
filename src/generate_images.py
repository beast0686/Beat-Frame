from diffusers import StableDiffusionPipeline
import torch
from pathlib import Path

# Ensure CUDA is available
assert torch.cuda.is_available(), "CUDA (GPU) is not available!"

# Set up paths using pathlib
ROOT_DIR = Path(__file__).parent.parent  # Go up two directories to the root
PROMPTS_FILE = ROOT_DIR / "assets" / "prompts.txt"
IMAGES_DIR = ROOT_DIR / "images"

# Ensure the images directory exists
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# Load the prompts from the prompts.txt file
try:
    with open(PROMPTS_FILE, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
except FileNotFoundError as e:
    print(f"Error: {e}")
    exit(1)

# Load the StableDiffusionPipeline
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16  # You can still keep this if your GPU supports float16
).to("cuda")

# Generate and save an image for each prompt
for i, line in enumerate(lines):
    prompt = f"cinematic scene of: {line}"
    image = pipe(prompt).images[0]
    image.save(IMAGES_DIR / f"frame_{i+1:02d}.png")

print(f"Images saved to {IMAGES_DIR}")
