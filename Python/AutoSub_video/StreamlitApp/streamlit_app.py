import streamlit as st
import cv2
import numpy as np
import os
import time
import torch
import whisper
from deep_translator import GoogleTranslator

import subprocess
import sys


def install_package(package_name):
    try:
        __import__(package_name)
    except ImportError:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        except Exception as e:
            print(f"⚠️ Can't install {package_name}: {e}")

# דוגמה לשימוש:
for pkg in ["streamlit", "opencv-python", "numpy==1.26.0", "torch", "whisper", "deep-translator"]:
    install_package(pkg)

# הערה: יש להניח שכל הפונקציות המקוריות שלך מוגדרות בתוך קובץ זה או מיובאות כראוי.
# למען הפשטות, אני מצרף את רוב הפונקציות הנדרשות ישירות לקוד ה-Streamlit.

# ----------------------------------------------------------------------
# הגדרות Streamlit - חלק מהפונקציות המקוריות מותאמות או מועברות לכאן
# ----------------------------------------------------------------------

# ---------------------------
# פונקציה לבדיקת זמינות ffmpeg
# ---------------------------
def is_ffmpeg_available():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


# ---------------------------
# הסרת סימן מים מפריים - ללא שינוי
# ---------------------------
def remove_watermark_from_frame(frame, mask_coords=None):
    mask = np.zeros(frame.shape[:2], np.uint8)
    if mask_coords:
        x1, y1 = mask_coords[0]
        x2, y2 = mask_coords[1]
        x1, x2 = sorted([x1, x2])
        y1, y2 = sorted([y1, y2])
        mask[y1:y2, x1:x2] = 255
    else:
        # ברירת מחדל אם אין קואורדינטות - השארתי את הלוגיקה המקורית
        h, w = frame.shape[:2]
        mask[0:50, 0:w] = 255

        # שימוש ב-cv2.INPAINT_TELEA במקום cv2.INPAINT_NS כיוון שהוא לרוב מהיר יותר,
    # אך השארתי את המקורי cv2.INPAINT_NS כפי שביקשת.
    inpainted_frame = cv2.inpaint(frame, mask, 10, cv2.INPAINT_NS)
    return inpainted_frame


# ---------------------------
# קריאת סרטון וחלוקה לפריימים
# ---------------------------
@st.cache_data
def extract_frames(video_file_bytes):
    # שמירת הקובץ הזמני
    temp_video_path = "temp_uploaded_video.mp4"
    with open(temp_video_path, "wb") as f:
        f.write(video_file_bytes)

    cap = cv2.VideoCapture(temp_video_path)
    if not cap.isOpened():
        return [], 0, (0, 0), temp_video_path

    frames = []
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # קוראים רק את הפריים הראשון עבור התצוגה המקדימה
    ret, first_frame = cap.read()
    cap.release()

    # מכיוון שאנו רוצים לשמור על קובץ וידאו עבור ה-FFMPEG לאחר מכן, נשאיר אותו
    # והפונקציות הבאות ישתמשו בנתיב הזמני.

    return [first_frame] if ret else [], fps, (width, height), temp_video_path


# ---------------------------
# שמירת סרטון (ללא אודיו) - ללא שינוי
# ---------------------------
def frames_to_video(frames, output_path, fps, frame_size):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, frame_size)
    if not out.isOpened():
        return False
    for frame in frames:
        out.write(frame)
    out.release()
    return True


# ---------------------------
# הסרת סימן מים (Watermark Removal) - הותאם ל-Streamlit
# ---------------------------
def remove_watermark_process(video_path, output_path, temp_video_path, coords_input, progress_bar, status_text):
    if not is_ffmpeg_available():
        st.error("שגיאה: ffmpeg אינו מותקן או אינו זמין במערכת. אנא התקן אותו כדי להמשיך.")
        return False, None

    # קריאת כל הפריימים (פונקציה זו צריכה להיות לא מוטמעת ב-cache_data!)
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        status_text.error(f"שגיאה: לא ניתן לפתוח את הסרטון בנתיב {video_path}")
        return False, None

    frames = []
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    status_text.info(f"מאתחל: {frame_count} פריימים, FPS: {fps}, גודל: {width}x{height}")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()

    # המרת הקואורדינטות למבנה הנדרש
    if coords_input:
        x1, y1, x2, y2 = coords_input
        coords = [(x1, y1), (x2, y2)]
    else:
        coords = None

    status_text.info("מתחיל עיבוד פריימים והסרת סימן מים...")
    processed_frames = []

    for i, frame in enumerate(frames):
        clean_frame = remove_watermark_from_frame(frame, coords)
        processed_frames.append(clean_frame)
        progress = (i + 1) / frame_count
        progress_bar.progress(progress)

    status_text.info("שמירת סרטון ביניים ללא אודיו...")
    if not frames_to_video(processed_frames, temp_video_path, fps, (width, height)):
        status_text.error("שגיאה בשמירת הסרטון הביניים.")
        return False, None

    status_text.info("מוסיפים אודיו מהסרטון המקורי (FFMPEG)...")
    final_video_path = output_path

    cmd = [
        "ffmpeg",
        "-y",
        "-i", temp_video_path,
        "-i", video_path,
        "-c:v", "libx264",
        "-c:a", "aac",
        "-map", "0:v:0",
        "-map", "1:a:0",
        final_video_path
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        status_text.success(f"✅ סרטון סופי ללא סימן מים (ללא כתוביות עדיין) נשמר ב-{final_video_path}")
        return True, final_video_path
    except subprocess.CalledProcessError as e:
        status_text.error(f"שגיאה בהוספת אודיו (FFMPEG): {e.stderr.decode()}")
        return False, None
    except FileNotFoundError:
        status_text.error("שגיאה: ffmpeg לא נמצא. אנא ודא שהוא מותקן וזמין ב-PATH.")
        return False, None


# ---------------------------
# הוספת כתוביות (Subtitles) - מותאם
# ---------------------------
def add_subtitles_process(video_path, video_title, output_path, goal_transcript, video_voice_language, status_text):
    status_text.info("🎙️ מבצע תמלול ותרגום (Whisper & Google Translator)...")

    # הגדרות Whisper
    device = "cuda" if torch.cuda.is_available() else "cpu"
    wisper_lang = 'he' if video_voice_language == 'iw' else video_voice_language

    try:
        model = whisper.load_model("small").to(device=device)
    except Exception as e:
        status_text.error(f"שגיאה בטעינת מודל Whisper: {e}. ודא ש-PyTorch ו-Whisper מותקנים כהלכה.")
        return False, None

    try:
        result = model.transcribe(video_path, language=wisper_lang)
    except Exception as e:
        status_text.error(f"שגיאה בתמלול: {e}")
        return False, None

    segments = result["segments"]
    # ... (המשך הלוגיקה המקורית של חלוקת המקטעים - מקוצר למען הבהירות) ...
    max_words_per_segment = 6
    new_segments = []
    for seg in segments:
        start = seg["start"]
        end = seg["end"]
        text = seg["text"].strip()
        words = text.split()
        duration = end - start
        num_splits = (len(words) + max_words_per_segment - 1) // max_words_per_segment
        split_duration = duration / num_splits if num_splits > 0 else duration
        for i in range(num_splits):
            split_text = " ".join(words[i * max_words_per_segment:(i + 1) * max_words_per_segment])
            new_segments.append(
                {"start": start + i * split_duration, "end": start + (i + 1) * split_duration, "text": split_text})
    segments = new_segments

    # תרגום וכתיבת קובץ SRT
    translator = GoogleTranslator(source=video_voice_language, target=goal_transcript)
    srt_path = f"{video_title}/subtitles.srt"

    def format_timestamp(t):
        hours = int(t // 3600)
        minutes = int((t % 3600) // 60)
        seconds = int(t % 60)
        millis = int((t % 1) * 1000)
        return f"{hours:02}:{minutes:02}:{seconds:02},{millis:03}"

    with open(srt_path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, start=1):
            text = seg["text"].strip()
            if goal_transcript != video_voice_language:
                try:
                    text = translator.translate(text)
                except Exception as e:
                    st.warning(f"⚠️ שגיאה בתרגום קטע: {e}")

            f.write(f"{i}\n")
            f.write(f"{format_timestamp(seg['start'])} --> {format_timestamp(seg['end'])}\n")
            f.write(f"{text}\n\n")

    status_text.info(f"📜 קובץ כתוביות (SRT) נוצר: {srt_path}")

    # הוספת כתוביות לסרטון באמצעות FFMPEG
    final_output_path = f'{video_title}/{output_path}_{goal_transcript}.mp4'
    if goal_transcript == 'iw':
        font_name = 'Arial'  # Arial תומך טוב בעברית
    else:
        font_name = 'Arial'

    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vf",
        f"subtitles={srt_path}:force_style='FontName={font_name},FontSize=20,PrimaryColour=&HFFFFFF&,BackColour=&H000000&,BorderStyle=3,Outline=1,Shadow=0',"
        f"drawtext=text='Created by Python S.Y':fontcolor=black:fontsize=6:x=W-tw-10:y=10",
        "-c:a", "copy",
        final_output_path
    ]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        status_text.success(f"✅ סרטון סופי עם כתוביות נשמר ב-{final_output_path}")
        return True, final_output_path
    except subprocess.CalledProcessError as e:
        status_text.error(f"שגיאה בהוספת כתוביות (FFMPEG): {e.stderr.decode()}")
        return False, None
    except FileNotFoundError:
        status_text.error("שגיאה: ffmpeg לא נמצא. אנא ודא שהוא מותקן וזמין ב-PATH.")
        return False, None


# ----------------------------------------------------------------------
# ממשק Streamlit
# ----------------------------------------------------------------------

st.set_page_config(page_title="כלי עיבוד וידאו - סימן מים וכתוביות", layout="wide")

st.title("🎬 כלי עיבוד וידאו: הסרת סימן מים והוספת כתוביות")

st.markdown("""
כלי זה יאפשר לך להסיר סימן מים מאזור נבחר בווידאו, לתמלל את האודיו, לתרגם אותו ולהוסיף כתוביות.
**שימו לב:** יש לוודא ש-**ffmpeg** מותקן במערכת להפעלת התהליך המלא.
""")

#---

## 1. העלאת קובץ וידאו

uploaded_file = st.file_uploader("בחר קובץ וידאו (מומלץ MP4)", type=['mp4', 'mov', 'avi'])

if uploaded_file is not None:
    file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type}
    st.info(f"קובץ הועלה: **{file_details['FileName']}**")

    # קריאת הפריים הראשון לצורך תצוגה מקדימה והגדרת קואורדינטות
    frames, fps, frame_size, temp_video_path = extract_frames(uploaded_file.read())

    if not frames:
        st.error("שגיאה בקריאת הוידאו. אנא ודא שהקובץ תקין.")
        st.stop()

    first_frame = frames[0]
    frame_rgb = cv2.cvtColor(first_frame, cv2.COLOR_BGR2RGB)

    st.subheader("תצוגה מקדימה של הפריים הראשון")
    st.image(frame_rgb, caption="פריים ראשון (להערכת מיקום סימן המים)", use_column_width=True)

    height, width, _ = first_frame.shape
    st.write(f"גודל הוידאו: {width}x{height}")

    #---

    ## 2. הגדרות הסרת סימן מים

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### קואורדינטות סימן מים (בפיקסלים)")
        x1 = st.number_input('X1 (שמאל עליון)', min_value=0, max_value=width, value=0, step=1)
        y1 = st.number_input('Y1 (שמאל עליון)', min_value=0, max_value=height, value=0, step=1)

    with col2:
        st.markdown("### קואורדינטות סימן מים (בפיקסלים)")
        x2 = st.number_input('X2 (ימין תחתון)', min_value=0, max_value=width, value=100, step=1)
        y2 = st.number_input('Y2 (ימין תחתון)', min_value=0, max_value=height, value=50, step=1)

    # הצגת פריים מעובד מקדים
    if st.button("הצג תצוגה מקדימה לאחר הסרה"):
        coords_preview = [(x1, y1), (x2, y2)]
        preview_frame = remove_watermark_from_frame(first_frame.copy(), coords_preview)
        preview_frame_rgb = cv2.cvtColor(preview_frame, cv2.COLOR_BGR2RGB)
        st.image(preview_frame_rgb, caption="פריים לאחר הסרת סימן מים (תצוגה מקדימה)", use_column_width=True)

    coords_to_use = (x1, y1, x2, y2)

    #---

    ## 3. הגדרות כתוביות ושפה

    st.markdown("### הגדרות שפה")

    # אפשרויות שפה לפי הקוד המקורי
    lang_options = {
        'עברית': 'iw', 'אנגלית': 'en', 'הינדי': 'hi',
        'ספרדית': 'es', 'צרפתית': 'fr', 'גרמנית': 'de',
        'ערבית': 'ar', 'יפנית': 'ja', 'סינית': 'zh-CN', 'רוסית': 'ru'
    }

    video_lang_name = st.selectbox("שפת האודיו המקורית של הוידאו:", list(lang_options.keys()), index=1)
    goal_lang_name = st.selectbox("שפת הכתוביות הרצויה:", list(lang_options.keys()), index=0)

    video_lang_code = lang_options[video_lang_name]
    goal_lang_code = lang_options[goal_lang_name]

    file_description = st.text_input("שם לתיקיית העבודה (למשל: Video_Project_1)", value="Processed_Video_Streamlit")

    # נתיבים זמניים וסופיים
    output_folder = file_description
    os.makedirs(output_folder, exist_ok=True)
    temp_watermark_video_path = f'{output_folder}/temp_no_watermark.mp4'
    final_watermark_video_path = f'{output_folder}/video_no_watermark_audio.mp4'

    #---

    ## 4. הפעלת התהליך

    if st.button("התחל תהליך עיבוד וידאו מלא", type="primary"):
        start_time = time.time()

        # 1. הסרת סימן מים
        st.subheader("שלב 1: הסרת סימן מים והוספת אודיו")
        status_watermark = st.empty()
        progress_bar = st.progress(0)

        # הקובץ המקורי נמצא ב-temp_video_path לאחר קריאתו
        success_wm, wm_output_path = remove_watermark_process(
            temp_video_path,
            final_watermark_video_path,
            temp_watermark_video_path,
            coords_to_use,
            progress_bar,
            status_watermark
        )

        if success_wm:
            st.success("✅ הסרת סימן מים הושלמה בהצלחה!")

            # 2. הוספת כתוביות
            st.subheader("שלב 2: תמלול, תרגום והוספת כתוביות")
            status_subtitles = st.empty()

            success_sub, final_video_path = add_subtitles_process(
                wm_output_path,
                video_title=output_folder,
                output_path="final_with_subs",
                goal_transcript=goal_lang_code,
                video_voice_language=video_lang_code,
                status_text=status_subtitles
            )

            if success_sub:
                st.balloons()
                st.subheader("🎉 התהליך הסתיים בהצלחה!")
                end_time = time.time()
                st.info(f"משך זמן כולל: **{end_time - start_time:.2f} שניות**")

                # מתן אפשרות הורדה
                with open(final_video_path, "rb") as file:
                    st.download_button(
                        label="⬇️ הורד את קובץ הוידאו הסופי",
                        data=file,
                        file_name=os.path.basename(final_video_path),
                        mime="video/mp4"
                    )

                st.video(final_video_path)
            else:
                st.error("❌ שגיאה בשלב הוספת הכתוביות. אנא בדוק את ההודעות למעלה.")

        else:
            st.error("❌ שגיאה בשלב הסרת סימן המים. אנא בדוק את ההודעות למעלה.")

        # ניקוי קבצים זמניים (מומלץ)
        try:
            os.remove(temp_video_path)
            if os.path.exists(temp_watermark_video_path):
                os.remove(temp_watermark_video_path)
        except OSError:
            pass  # התעלם אם הקבצים לא קיימים
















