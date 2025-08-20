<img width="567" height="30" alt="image" src="https://github.com/user-attachments/assets/24613c4b-0f50-4f56-8a4b-6ebbfe66fbf5" />
# 🎬 Video Processing Tool – Subtitle Generation & Watermark Removal

This **Python-based video processing pipeline** enables you to:
- Remove watermarks from videos using OpenCV’s inpainting.
- Transcribe speech to text with OpenAI Whisper.
- Translate text into another language (e.g., English ↔ Hebrew).
- Generate subtitles (SRT) with accurate timing.
- Burn subtitles directly into the video using FFmpeg.

---

## 🚀 Features

<custom-element data-json="%7B%22type%22%3A%22table-metadata%22%2C%22attributes%22%3A%7B%22title%22%3A%22Features%22%7D%7D" />
   Feature                | Description                                                                 |
 |------------------------|-----------------------------------------------------------------------------|
 | 🔊 **Speech-to-Text**   | Uses Whisper (`small` model) to transcribe audio.                          |
 | 🌍 **Translation**      | Translates text via `deep-translator` (GoogleTranslator).                  |
 | 📝 **Subtitle Generator** | Creates `.srt` subtitle files with proper timestamps.                     |
 | 🎥 **Hardcoded Subtitles** | Burns subtitles directly into the video using FFmpeg.                     |
 | 🧼 **Watermark Removal** | Lets users select the watermark area and removes it from all frames.      |
 | 📦 **Final Output**     | Delivers a clean video with subtitles in `.mp4` format, plus `.srt` file. |

---

## 📂 Project Structure

```bash
├── transcript.py        # Main script to add subtitles
├── remove_watermark.py  # Script to remove watermark
├── videos/              # Input videos
├── outputs/             # Processed videos
└── README.md            # Documentation

⚙️ Installation


Clone the repository and install dependencies:
 Copypip install whisper deep-translator opencv-python tqdm ffmpeg-python


Ensure FFmpeg is installed on your system:

Linux: sudo apt install ffmpeg
macOS: brew install ffmpeg
Windows (Chocolatey): choco install ffmpeg




🛠️ Usage
1️⃣ Remove Watermark from Video
 Copyfrom remove_watermark import unique_main

video_path = "videos/input.mp4"
output_path = "outputs/video_no_watermark.mp4"
temp_video_path = "outputs/temp.mp4"

unique_main(video_path, output_path, temp_video_path)

Note: A window will open—drag your mouse to select the watermark area and press Enter.


2️⃣ Generate Subtitles & Burn into Video
 Copyfrom transcript import add_subtitles

video_path = "outputs/video_no_watermark.mp4"
add_subtitles(
    video_path=video_path,
    video_title="final_project_video",
    goal_transcript="he",      # Target language: "he" (Hebrew), "en" (English)
    video_voice_language="en"  # Original voice language
)
Outputs:

subtitles.srt (subtitle file)
video_with_subs_he.mp4 (final video with burned subtitles)


🔄 Workflow Diagram
 Copyflowchart TD
    A[🎥 Input Video] --> B[🧼 Remove Watermark]
    B --> C[🎙️ Speech-to-Text (Whisper)]
    C --> D[🌍 Translate (GoogleTranslator)]
    D --> E[📝 Generate Subtitles (SRT)]
    E --> F[🔥 Burn Subtitles with FFmpeg]
    F --> G[✅ Final Clean Video with Subtitles]

📊 Performance Tips

Use GPU acceleration for Whisper (if available):
 Copypip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

For faster processing, reduce max_words_per_segment in transcript.py.
To generate only .srt files (without burning subtitles), skip the FFmpeg stage.


🧪 Testing
Test with a short video first:
 Copypython transcript.py
Expected Outputs:

subtitles.srt (with translations, if enabled)
video_with_subs_he.mp4 (final video)


⚡ Notes

Language Options: he (Hebrew), en (English).
Whisper Model: Uses the small model by default (adjustable to tiny, base, medium, or large).
Watermark Removal: Requires manual selection of the watermark area in the first frame.
Processing Time: Depends on video length and hardware (CPU/GPU).


🤝 Contribution
Pull requests are welcome! Suggested improvements:

Support for additional subtitle formats (e.g., .vtt).
Auto-detection for watermark removal.
Batch processing for multiple videos.


<img width="358" height="672" alt="image" src="https://github.com/user-attachments/assets/57606768-7a61-4ceb-a1ed-503b493dc413" />
