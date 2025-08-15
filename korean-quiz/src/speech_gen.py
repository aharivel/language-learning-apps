#!/usr/bin/env python3
"""
Korean Audio Generation Script
Generates MP3 files for Korean learning app using Microsoft Edge TTS

Usage:
    python speech_gen.py          # Generate missing audio files
    python speech_gen.py -f       # Force regenerate all audio files

Requirements:
    pip install edge-tts
"""

import asyncio
import edge_tts
import os
import argparse
from pathlib import Path
import sys

# Create output folder
OUTPUT_DIR = "korean_audio_assets"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Voice settings - Using high quality Korean neural voice
VOICE = "ko-KR-SunHiNeural"

# Data from your React app - Complete list
basicVowels = [
    'ㅏ','ㅑ','ㅓ','ㅕ','ㅗ','ㅛ','ㅜ','ㅠ','ㅡ','ㅣ'
]

complexVowels = [
    'ㅐ','ㅒ','ㅔ','ㅖ','ㅘ','ㅙ','ㅚ','ㅝ','ㅞ','ㅟ','ㅢ'
]

basicConsonants = [
    'ㄱ','ㄴ','ㄷ','ㄹ','ㅁ','ㅂ','ㅅ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ'
]

doubleConsonants = [
    'ㄲ','ㄸ','ㅃ','ㅆ','ㅉ'
]

# Extended syllable examples from the app
syllableExamples = [
    '가','나','다','라','마','바','사','아','자','차','카','타','파','하',
    '고','노','도','로','모','보','소','오','조','초','코','토','포','호',
    '구','누','두','루','무','부','수','우','주','추','쿠','투','푸','후',
    '그','느','드','르','므','브','스','으','즈','츠','크','트','프','흐',
    '기','니','디','리','미','비','시','이','지','치','키','티','피','히'
]

# Basic sentences/phrases from the app
basicSentences = [
    '안녕하세요',      # Hello (formal)
    '안녕',           # Hi/Bye (casual)
    '감사합니다',      # Thank you (formal)
    '고마워',         # Thanks (casual)
    '제이름은',       # My name is (simplified for audio)
    '죄송합니다',      # I'm sorry (formal)
    '네',            # Yes
    '아니요',         # No
    '안녕히가세요',    # Goodbye (to person leaving)
    '안녕히계세요',    # Goodbye (when you leave)
]

# Korean numbers (Sino-Korean system)
koreanNumbers = [
    '일',    # 1
    '이',    # 2
    '삼',    # 3
    '사',    # 4
    '오',    # 5
    '육',    # 6
    '칠',    # 7
    '팔',    # 8
    '구',    # 9
    '십',    # 10
]

# Merge all into one list (preserve order, avoid duplicates)
all_items = []
seen = set()

for item_list in [basicVowels, complexVowels, basicConsonants, doubleConsonants, 
                  syllableExamples, basicSentences, koreanNumbers]:
    for item in item_list:
        if item not in seen:
            all_items.append(item)
            seen.add(item)

def file_exists(text):
    """Check if audio file already exists for given text."""
    output_path = os.path.join(OUTPUT_DIR, f"{text}.mp3")
    return Path(output_path).exists()

async def generate_audio(text, force=False):
    """Generate audio file for Korean text using Edge TTS."""
    output_path = os.path.join(OUTPUT_DIR, f"{text}.mp3")
    
    # Skip if file exists and not forcing regeneration
    if file_exists(text) and not force:
        print(f"⏭️  Skipping {text}.mp3 (already exists)")
        return True
    
    try:
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(output_path)
        
        status = "🔄 Regenerated" if file_exists(text) and force else "✅ Generated"
        print(f"{status} {text} → {text}.mp3")
        return True
        
    except Exception as e:
        print(f"❌ Error generating {text}.mp3: {str(e)}")
        return False

async def main():
    """Main function to generate all Korean audio files."""
    parser = argparse.ArgumentParser(description="Generate Korean audio files for learning app")
    parser.add_argument('-f', '--force', action='store_true', 
                       help='Force regeneration of all audio files (even if they exist)')
    
    args = parser.parse_args()
    
    print("🎵 Korean Audio Generator (Edge TTS)")
    print("=" * 45)
    print(f"📁 Output directory: {OUTPUT_DIR}")
    print(f"🎤 Voice: {VOICE}")
    
    # Generate audio files
    total_files = len(all_items)
    generated = 0
    skipped = 0
    errors = 0
    
    print(f"\n🎯 Processing {total_files} Korean audio files...")
    if args.force:
        print("🔄 Force mode: Regenerating ALL files")
    else:
        print("⚡ Smart mode: Skipping existing files")
    
    print("-" * 45)
    
    for i, text in enumerate(all_items, 1):
        print(f"[{i:2d}/{total_files}] ", end="")
        
        if file_exists(text) and not args.force:
            print(f"⏭️  Skipping {text}.mp3 (already exists)")
            skipped += 1
        else:
            if await generate_audio(text, args.force):
                generated += 1
            else:
                errors += 1
    
    # Summary
    print("\n" + "=" * 45)
    print("📊 SUMMARY:")
    print(f"✅ Generated: {generated} files")
    print(f"⏭️  Skipped: {skipped} files")
    print(f"❌ Errors: {errors} files")
    
    # Count actual files in directory
    actual_files = len(list(Path(OUTPUT_DIR).glob('*.mp3')))
    print(f"📁 Total files in {OUTPUT_DIR}: {actual_files}")
    
    if errors == 0:
        print("\n🎉 All audio files ready for Korean learning app!")
    else:
        print(f"\n⚠️  {errors} files failed to generate. Check internet connection.")
    
    print(f"\n💡 Tip: Use 'python {sys.argv[0]} -f' to force regenerate all files")
    
    # Show what's included
    print(f"\n📝 Audio files include:")
    print(f"   • {len(basicVowels)} basic vowels")
    print(f"   • {len(complexVowels)} complex vowels") 
    print(f"   • {len(basicConsonants)} basic consonants")
    print(f"   • {len(doubleConsonants)} double consonants")
    print(f"   • {len(syllableExamples)} syllable examples")
    print(f"   • {len(basicSentences)} basic phrases")
    print(f"   • {len(koreanNumbers)} numbers (1-10)")

if __name__ == "__main__":
    asyncio.run(main())

