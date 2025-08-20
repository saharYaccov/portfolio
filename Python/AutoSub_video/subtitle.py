import os
import subprocess
import whisper
from deep_translator import GoogleTranslator
from remove_watermark import unique_main
import time

def add_subtitles(video_path,
                  video_title,
                  output_path="video_with_subs",
                  goal_transcript='he',
                  video_voice_language='en'):
    os.makedirs(video_title,exist_ok=True)
    model = whisper.load_model("small")
    print("🎙️ מבצע תמלול של האודיו...")
    result = model.transcribe(video_path, language=video_voice_language)
    segments = result["segments"]






    max_words_per_segment = 6  # הגבל כל קטע ל-4 מילים
    new_segments = []

    for seg in segments:
        start = seg["start"]
        end = seg["end"]
        text = seg["text"].strip()
        words = text.split()

        # חישוב משך הזמן של הקטע המקורי
        duration = end - start

        # מספר הקטעים לאחר החלוקה
        num_splits = (len(words) + max_words_per_segment - 1) // max_words_per_segment
        # משך הזמן לכל קטע
        split_duration = duration / num_splits if num_splits > 0 else duration

        for i in range(num_splits):
            split_text = " ".join(words[i * max_words_per_segment:(i + 1) * max_words_per_segment])
            new_segments.append({
                "start": start + i * split_duration,
                "end": start + (i + 1) * split_duration,
                "text": split_text
            })

    segments = new_segments






    translator = GoogleTranslator(source=video_voice_language, target=goal_transcript)

    srt_path = f"{video_title}/subtitles.srt"
    with open(srt_path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, start=1):
            start = seg["start"]
            end = seg["end"]
            text = seg["text"].strip()

            if goal_transcript != video_voice_language:
                try:
                    text = translator.translate(text)
                except Exception as e:
                    print("⚠️ שגיאה בתרגום:", e)

            def format_timestamp(t):
                hours = int(t // 3600)
                minutes = int((t % 3600) // 60)
                seconds = int(t % 60)
                millis = int((t % 1) * 1000)
                return f"{hours:02}:{minutes:02}:{seconds:02},{millis:03}"

            f.write(f"{i}\n")
            f.write(f"{format_timestamp(start)} --> {format_timestamp(end)}\n")
            f.write(f"{text}\n\n")

    print("📜 Subtitles file created:", srt_path)

    if goal_transcript=='iw':
        goal_transcript='he'
    final_output = f'{video_title}/{output_path}_{goal_transcript}.mp4'
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vf", f"subtitles={srt_path}:force_style='FontName=Arial,FontSize=20'",
        "-c:a", "copy",
        f'{final_output}'
    ]
    subprocess.run(cmd, check=True)
    print(f"✅ Video with subtitles saved at {output_path}")


def start(File,describe_file ,goal_lang , video_lang):
    start_time = time.time()

    describe_file = describe_file
        #'final_project_video3_hebrew'
    goal_transcript = goal_lang
    video_voice_language = video_lang
    file_name = f'{describe_file}_{video_voice_language}2{goal_transcript}'
    os.makedirs(file_name, exist_ok=True)
    video_file = File
        #'/Users/shryqb/PycharmProjects/Video_tool/videos/WhatsApp Video 2025-08-18 at 19.20.40.mp4'
    unique_main(video_file,f'{file_name}/video_no_watermark.mp4',temp_video_path=f'{file_name}/temp.mp4')
    video_path = f"{file_name}/video_no_watermark.mp4"
    add_subtitles(video_path,video_title=file_name, goal_transcript=goal_transcript, video_voice_language=video_voice_language)

    # goal_transcript options:
#   Hebrew        - iw
#   English       - en
#   Hindi         - hi
#   Spanish       - es
#   French        - fr
#   German        - de
#   Arabic        - ar
#   Japanese      - ja
#   Chinese (Simplified) - zh-CN
#   Russian       - ru
 

    end_time = time.time()

    print(f'Total Timer : {end_time-start_time}')






# File        : Path to the video file you want to process
# dfile       : Description/name for the video, used for creating folders and output files
# goal_lang   : Target language for transcription/translation of subtitles (here 'iw' = Hebrew)
# video_lang  : Original language of the video's audio (here 'en' = English)
# start(...)  : Function call that removes watermark, performs transcription, translation, and generates subtitles

File = 'videos/Learn English Conversation with Friends Series.mp4'
dfile = 'Example_video'
goal_lang='iw' # goal language
video_lang='en' # video language
start(File=File , describe_file=dfile , goal_lang='iw' ,video_lang='en')
