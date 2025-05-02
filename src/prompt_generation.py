import openai
from pathlib import Path

# Set your OpenAI API key
openai.api_key = "YOUR_API_KEY"

# File paths
ROOT_DIR = Path(__file__).parent.parent  # Go up two directories from the script
LYRICS_FILE = ROOT_DIR / "assets" / "lyrics.txt"  # Set correct path
OUTPUT_FILE = ROOT_DIR / "assets" / "prompts.txt"  # Set correct path

def generate_prompts_from_lyrics(lyrics_text):
    system_prompt = (
        "You are an assistant that transforms song lyrics into visual prompts for an AI image generator. "
        "Given multiple lines of lyrics, return one image prompt for each line in the same order. "
        "Make each prompt visually descriptive and suitable for models like 'runwayml/stablediffusion-v1-5'.\n\n"
        "Return the output in the same number of lines — one prompt per line."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Lyrics:\n{lyrics_text.strip()}\n\nImage Prompts:"}
            ],
            temperature=0.7,
            max_tokens=1500,
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"[ERROR generating prompts: {e}]"

def main():
    if not LYRICS_FILE.exists():
        print(f"Error: {LYRICS_FILE} not found.")
        return

    with open(LYRICS_FILE, 'r', encoding='utf-8') as infile:
        lyrics_text = infile.read()

    print("Generating image prompts from lyrics...")
    prompts = generate_prompts_from_lyrics(lyrics_text)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
        outfile.write(prompts + '\n')

    print(f"\nAll image prompts saved to '{OUTPUT_FILE}'")

if __name__ == '__main__':
    main()
