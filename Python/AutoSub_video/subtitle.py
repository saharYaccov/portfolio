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

    print("📜 קובץ כתוביות נוצר:", srt_path)

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
    print(f"✅ סרטון עם כתוביות נשמר ב- {output_path}")


if __name__ == "__main__":
    start_time = time.time()

    describe_file = 'final_project_video3_hebrew'
    goal_transcript = 'iw'
    video_voice_language = 'en'
    file_name = f'{describe_file}_{video_voice_language}2{goal_transcript}'
    os.makedirs(file_name, exist_ok=True)
    video_file = '/Users/shryqb/PycharmProjects/Video_tool/videos/WhatsApp Video 2025-08-18 at 19.20.40.mp4'
    unique_main(video_file,f'{file_name}/video_no_watermark.mp4',temp_video_path=f'{file_name}/temp.mp4')
    video_path = f"{file_name}/video_no_watermark.mp4"
    add_subtitles(video_path,video_title=file_name, goal_transcript=goal_transcript, video_voice_language=video_voice_language)

    #goal_transcript :
    #   Hebrew - iw
    #   English - en

    end_time = time.time()

    print(f'Total Timer : {end_time-start_time}')
