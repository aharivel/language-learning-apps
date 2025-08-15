import asyncio
import edge_tts
import os

# Create output folder
OUTPUT_DIR = "korean_audio_assets"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Data from your React app
basicVowels = [
    'ㅏ','ㅑ','ㅓ','ㅕ','ㅗ','ㅛ','ㅜ','ㅠ','ㅡ','ㅣ'
]
basicConsonants = [
    'ㄱ','ㄴ','ㄷ','ㄹ','ㅁ','ㅂ','ㅅ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ'
]
syllableExamples = [
    '가','나','다','마','바','사','아','자'
]
complexVowels = [
    'ㅐ','ㅒ','ㅔ','ㅖ','ㅘ','ㅙ','ㅚ','ㅝ','ㅞ','ㅟ','ㅢ'
]
doubleConsonants = [
    'ㄲ','ㄸ','ㅃ','ㅆ','ㅉ'
]

# Merge all into one set (to avoid duplicates)
all_chars = sorted(set(
    basicVowels + basicConsonants +
    syllableExamples + complexVowels + doubleConsonants
))

# Voice settings
VOICE = "ko-KR-SunHiNeural"

async def main():
    for char in all_chars:
        output_path = os.path.join(OUTPUT_DIR, f"{char}.mp3")
        communicate = edge_tts.Communicate(char, VOICE)
        await communicate.save(output_path)
        print(f"✅ Saved {char} → {output_path}")

if __name__ == "__main__":
    asyncio.run(main())

