# Video Audio Transcription and Translation

This script extracts audio from video files, transcribes the audio into text, and translates the text into a specified language. It uses several libraries, including `whisper` for transcription, `ffmpeg` for audio extraction, and `GoogleTranslator` for translation.



## ✅  Required libraries for the transcript translation script:
pip install moviepy
pip install googletrans==4.0.0-rc1
pip install SpeechRecognition
pip install pydub
pip install pytube


## 📦 Explanation of Each Library:
Library	Purpose
moviepy	To extract audio from video files
googletrans	To translate text (must use version 4.0.0-rc1)
SpeechRecognition	To transcribe speech from audio to text
pydub	To convert and handle audio formats (like MP3 to WAV)
pytube	To download YouTube videos (if needed)


## Features

- Extracts audio from video files using `ffmpeg`.
- Transcribes audio into text using `whisper`.
- Translates text into a specified language using `GoogleTranslator`.
- Splits text into a specified number of lines for better readability.
- Saves the results into a CSV and an Excel file with formatted columns.

## Dependencies

- `re`
- `pandas`
- `whisper`
- `ffmpeg`
- `googletrans`
- `deep_translator`
- `xlsxwriter`

## Installation

Ensure you have Python installed on your system. You can install the required libraries using pip:

```bash
pip install pandas whisper ffmpeg-python googletrans==4.0.0-rc1 deep-translator xlsxwriter
Additionally, you need to have ffmpeg installed on your system. You can download it from ffmpeg.org.
Usage


Define Video Paths: Specify the paths to your video files and the target language for transcription.


Run the Script: Execute the script in a Python environment where the required dependencies are installed.


View the Results: The script will generate a CSV file and an Excel file with the transcribed and translated text.


Example
 Copyimport re
import pandas as pd
import whisper
import ffmpeg
import os
from googletrans import Translator
import warnings
from deep_translator import GoogleTranslator

warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

param_line = 10

def get_deep_translation(text, language_goal):
    return GoogleTranslator(source='auto', target=language_goal).translate(text)

def extract_audio_with_ffmpeg(video_path, audio_path="temp_audio.wav"):
    try:
        (
            ffmpeg
            .input(video_path)
            .output(audio_path, format='wav', acodec='pcm_s16le', ac=1, ar='16000')
            .overwrite_output()
            .run(quiet=True)
        )
        return audio_path
    except ffmpeg.Error as e:
        print("FFmpeg error:", e)
        return None

def get_translation(text, language_goal):
    translator = Translator()
    translated = translator.translate(text, dest=language_goal)
    return translated.text

def transcribe_audio(audio_path, language="ar"):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, language=language)
    return result["text"]

def extract_text_from_video(video_path, language="ar"):
    print("[+] Extracting audio...")
    audio_path = extract_audio_with_ffmpeg(video_path)
    if not audio_path:
        print("[-] Failed to extract audio.")
        return ""
    print("[+] Transcribing audio...")
    text = transcribe_audio(audio_path, language=language)
    os.remove(audio_path)
    return text

def split_text_by_lines(text, num_lines):
    lines = text.splitlines()
    if len(lines) < num_lines:
        words = ' '.join(lines).split()
        avg_words_per_line = max(1, len(words) // num_lines)
        lines = [' '.join(words[i\:i + avg_words_per_line]) for i in range(0, len(words), avg_words_per_line)]
    return '\n'.join(lines)

# Usage
p1 = {'path': '/Users/shryqb/PycharmProjects/PythonProject/some_running/תכניות בפייתון/trans_video/videos/videoplayback.mp4', 'lang': 'en'}
p2 = {'path': '/Users/shryqb/PycharmProjects/PythonProject/some_running/תכניות בפייתון/trans_video/videos/VID_20250408_022041_725.mp4', 'lang': 'en'}

video_file = []
try:
    for i in range(1, 200):
        var_name = 'p' + str(i)
        if var_name in globals():
            video_file.append(globals()[var_name])
except Exception as e:
    pass

df = []
for video in video_file:
    print(video)
    text_output = extract_text_from_video(video_path=video['path'], language=video['lang'])
    text_output = split_text_by_lines(text_output, param_line)
    Real_text = text_output
    if video['lang'] != 'en':
        text_output = get_deep_translation(text_output, 'en')
    translate_video = get_translation(text_output, 'he')
    translate_video = split_text_by_lines(translate_video, param_line)
    df.append({
        'Language': video['lang'],
        'Real_text_video': Real_text,
        'English_translated': text_output,
        'Translate_video': translate_video
    })

df = pd.DataFrame(df)
df.to_csv('texts of all video.csv')

import xlsxwriter

# Create an ExcelWriter object
writer = pd.ExcelWriter('texts of all video.xlsx', engine='xlsxwriter')

# Write the DataFrame to a sheet without the index
df.to_excel(writer, index=False, sheet_name='Videos')

# Get the workbook and worksheet objects
workbook = writer.book
worksheet = writer.sheets['Videos']

# Create a new format for wrapping text in cells
wrap_format = workbook.add_format({'text_wrap': True})

# Set the column width and apply the wrap format
for i, col in enumerate(df.columns):
    worksheet.set_column(i, i, 70, wrap_format)

# Close the writer and save the final file with formatting
writer.close()
Output
The script generates two files:

texts of all video.csv: A CSV file containing the transcribed and translated text.
texts of all video.xlsx: An Excel file containing the transcribed and translated text with formatted columns for better readability.

Notes

Ensure all dependencies are installed before running the script.
The script can be extended to include additional video files or custom criteria for analysis.
The script uses whisper for transcription, which requires a significant amount of computational resources.

 CopyThis `README.md` provides an overview of the script, its main functions, usage instructions, and an example of how to run the script. You can copy this content into a `README.md` file in your project directory.
