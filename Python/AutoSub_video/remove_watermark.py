import cv2
import numpy as np
import subprocess
import sys
from tqdm import tqdm  # ספרייה להצגת סרגל התקדמות

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
# פונקציה לבחירת אזור סימן המים
# ---------------------------
def select_watermark_area(frame):
    coords = []
    temp_display = frame.copy()

    def mouse_callback(event, x, y, flags, param):
        nonlocal coords, temp_display
        if event == cv2.EVENT_LBUTTONDOWN:
            coords = [(x, y)]
        elif event == cv2.EVENT_LBUTTONUP:
            coords.append((x, y))
            temp_frame = temp_display.copy()
            cv2.rectangle(temp_frame, coords[0], coords[1], (0, 255, 0), 2)
            cv2.imshow("Select Watermark Area", temp_frame)

    cv2.namedWindow("Select Watermark Area")
    cv2.setMouseCallback("Select Watermark Area", mouse_callback)
    cv2.imshow("Select Watermark Area", temp_display)
    print("גרור עם העכבר כדי לסמן את אזור סימן המים. לאחר מכן לחץ על מקש Enter או סגור את החלון.")

    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == 13:  # מקש Enter
            break

    cv2.destroyAllWindows()
    if len(coords) == 2:
        return coords
    return None

# ---------------------------
# קריאת סרטון וחלוקה לפריימים
# ---------------------------
def extract_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"שגיאה: לא ניתן לפתוח את הסרטון בנתיב {video_path}")
        return [], 0, (0, 0)

    frames = []
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"מספר פריימים בסרטון: {frame_count}, FPS: {fps}, גודל: {width}x{height}")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)

    cap.release()
    return frames, fps, (width, height)

# ---------------------------
# הסרת סימן מים מפריים
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
        h, w = frame.shape[:2]
        mask[0:50, 0:w] = 255

    inpainted_frame = cv2.inpaint(frame, mask, 10, cv2.INPAINT_NS)
    return inpainted_frame

# ---------------------------
# שמירת סרטון (ללא אודיו)
# ---------------------------
def frames_to_video(frames, output_path, fps, frame_size):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, frame_size)
    if not out.isOpened():
        print(f"שגיאה: לא ניתן ליצור את קובץ הווידאו {output_path}")
        return False
    for frame in frames:
        out.write(frame)
    out.release()
    print(f"סרטון ביניים נשמר ב-{output_path}")
    return True

# ---------------------------
# Main כולל שמירת אודיו והתקדמות
# ---------------------------
def main(video_path, output_path,temp_video_path):
    if not is_ffmpeg_available():
        print("שגיאה: ffmpeg לא מותקן או לא זמין במערכת.")
        sys.exit(1)


    frames, fps, frame_size = extract_frames(video_path)
    if not frames:
        print("שגיאה: לא ניתן לקרוא פריימים מהסרטון.")
        return

    coords = select_watermark_area(frames[0])
    if not coords:
        print("לא נבחר אזור לסימן המים. משתמש בברירת מחדל.")
        coords = None

    print("בדיקה: הצגת פריים לאחר הסרת סימן מים...")
    show_frame = remove_watermark_from_frame(frames[0], coords)
    cv2.imshow("Preview Processed Frame", show_frame)
    cv2.waitKey(1000)  # הצגה שניה אחת בלבד
    cv2.destroyAllWindows()

    print("מתחיל עיבוד פריימים והסרת סימן מים...")
    processed_frames = []
    for frame in tqdm(frames, desc="Processing frames", unit="frame"):
        clean_frame = remove_watermark_from_frame(frame, coords)
        processed_frames.append(clean_frame)

    if not frames_to_video(processed_frames, temp_video_path, fps, frame_size):
        print("שגיאה בשמירת הסרטון הביניים.")
        return

    print("מוסיפים אודיו מהסרטון המקורי...")
    cmd = [
        "ffmpeg",
        "-y",
        "-i", temp_video_path,
        "-i", video_path,
        "-c:v", "libx264",
        "-c:a", "aac",
        "-map", "0:v:0",
        "-map", "1:a:0",
        output_path
    ]
    try:
        subprocess.run(cmd, check=True)
        print(f"סרטון סופי עם אודיו נשמר ב-{output_path}")
        print("✅ כל התהליך הסתיים בהצלחה. Python עובד כראוי 👍")
    except subprocess.CalledProcessError as e:
        print("שגיאה בשמירת הסרטון עם אודיו:", e)
        sys.exit(1)

# ---------------------------
def unique_main(video_path,output_path,temp_video_path):
    main(video_path, output_path,temp_video_path)
