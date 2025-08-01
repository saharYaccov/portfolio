import re

import pandas as pd
import whisper
import ffmpeg
import os
from googletrans import Translator
import warnings
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

param_line = 10
from deep_translator import GoogleTranslator
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
    # קודם כל מחליפים את הסימנים המיוחדים בירידת שורה
    #text = re.sub(r'[@!#$?]', r'\n', text)

    # מחלקים את הטקסט לפי שורות קיימות
    lines = text.splitlines()

    # אם יש מעט שורות – מבצעים גם חלוקה לפי מילים
    if len(lines) < num_lines:
        words = ' '.join(lines).split()
        avg_words_per_line = max(1, len(words) // num_lines)
        lines = [' '.join(words[i:i + avg_words_per_line]) for i in range(0, len(words), avg_words_per_line)]

    return '\n'.join(lines)

# שימוש:
p1 =     {'path': '/Users/shryqb/PycharmProjects/PythonProject/some_running/תכניות בפייתון/trans_video/videos/videoplayback.mp4', 'lang': 'en'}
p2 =     {'path': '/Users/shryqb/PycharmProjects/PythonProject/some_running/תכניות בפייתון/trans_video/videos/VID_20250408_022041_725.mp4', 'lang': 'en'}


video_file = []
try :
    for i in range (1,200):
        var_name = 'p' + str(i)
        if var_name in globals():
            video_file.append(globals()[var_name])
except Exception as e:
    pass
df = []
for video in video_file:
    print(video)
    text_output = extract_text_from_video(video_path= video['path'] , language= video['lang'])
    text_output = split_text_by_lines(text_output,param_line)
    Real_text = text_output
    if video['lang']!='en':
        text_output = get_deep_translation(text_output, 'en')
    translate_video = get_translation(text_output, 'he')
    translate_video = split_text_by_lines(translate_video,param_line)
    df.append( {
        'Language':video['lang'],
        'Real_text_video':Real_text,
        'English_translated':text_output,
        'Translate_video' : translate_video

    })
df = pd.DataFrame(df)
df.to_csv('texts of all video.csv')
import xlsxwriter





# יוצרים אובייקט ExcelWriter, שמאפשר לכתוב קובץ Excel
# בוחרים מנוע כתיבה בשם 'xlsxwriter' שתומך בעיצוב תאים
writer = pd.ExcelWriter('texts of all video.xlsx', engine='xlsxwriter')

# כותבים את ה-DataFrame לגיליון בשם 'Videos', בלי העמודה של האינדקס
df.to_excel(writer, index=False, sheet_name='Videos')

# מקבלים את אובייקט חוברת העבודה (Workbook) מתוך writer
workbook = writer.book

# מקבלים את אובייקט הגיליון (Worksheet) שאליו נכתב ה-DataFrame
worksheet = writer.sheets['Videos']

# יוצרים פורמט חדש עבור תאים: עוטף את הטקסט בתוך התא (wrap text)
wrap_format = workbook.add_format({'text_wrap': True})

# עוברים על כל העמודות ב-DataFrame לפי אינדקס
for i, col in enumerate(df.columns):
    # קובעים לעמודה הזו רוחב של 70 תווים + מיישמים את פורמט עטיפת הטקסט
    worksheet.set_column(i, i, 70, wrap_format)

# סוגרים את writer ושומרים את הקובץ הסופי עם העיצוב
writer.close()
