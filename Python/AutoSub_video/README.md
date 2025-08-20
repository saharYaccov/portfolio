<img width="567" height="30" alt="image" src="https://github.com/user-attachments/assets/24613c4b-0f50-4f56-8a4b-6ebbfe66fbf5" />

---

<img width="257" height="26" alt="image" src="https://github.com/user-attachments/assets/409dfe8e-5356-479c-bb44-d87951023915" />

---

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

```

---


| Language | Code | Language | Code | Language | Code | Language | Code |
|----------|------|----------|------|----------|------|----------|------|
| Afrikaans | af | Albanian | sq | Amharic | am | Arabic | ar |
| Armenian | hy | Assamese | as | Aymara | ay | Azerbaijani | az |
| Bambara | bm | Basque | eu | Belarusian | be | Bengali | bn |
| Bhojpuri | bho | Bosnian | bs | Bulgarian | bg | Catalan | ca |
| Cebuano | ceb | Chichewa | ny | Chinese (Simplified) | zh-CN | Chinese (Traditional) | zh-TW |
| Corsican | co | Croatian | hr | Czech | cs | Danish | da |
| Dhivehi | dv | Dogri | doi | Dutch | nl | English | en |
| Esperanto | eo | Estonian | et | Ewe | ee | Filipino | tl |
| Finnish | fi | French | fr | Frisian | fy | Galician | gl |
| Georgian | ka | German | de | Greek | el | Guarani | gn |
| Gujarati | gu | Haitian Creole | ht | Hausa | ha | Hawaiian | haw |
| Hebrew | iw | Hindi | hi | Hmong | hmn | Hungarian | hu |
| Icelandic | is | Igbo | ig | Ilocano | ilo | Indonesian | id |
| Irish | ga | Italian | it | Japanese | ja | Javanese | jw |
| Kannada | kn | Kazakh | kk | Khmer | km | Kinyarwanda | rw |
| Konkani | gom | Korean | ko | Krio | kri | Kurdish (Kurmanji) | ku |
| Kurdish (Sorani) | ckb | Kyrgyz | ky | Lao | lo | Latin | la |
| Latvian | lv | Lingala | ln | Lithuanian | lt | Luganda | lg |
| Luxembourgish | lb | Macedonian | mk | Maithili | mai | Malagasy | mg |
| Malay | ms | Malayalam | ml | Maltese | mt | Maori | mi |
| Marathi | mr | Meiteilon (Manipuri) | mni-Mtei | Mizo | lus | Mongolian | mn |
| Myanmar | my | Nepali | ne | Norwegian | no | Odia (Oriya) | or |
| Oromo | om | Pashto | ps | Persian | fa | Polish | pl |
| Portuguese | pt | Punjabi | pa | Quechua | qu | Romanian | ro |
| Russian | ru | Samoan | sm | Sanskrit | sa | Scots Gaelic | gd |
| Sepedi | nso | Serbian | sr | Sesotho | st | Shona | sn |
| Sindhi | sd | Sinhala | si | Slovak | sk | Slovenian | sl |
| Somali | so | Spanish | es | Sundanese | su | Swahili | sw |
| Swedish | sv | Tajik | tg | Tamil | ta | Tatar | tt |
| Telugu | te | Thai | th | Tigrinya | ti | Tsonga | ts |
| Turkish | tr | Turkmen | tk | Twi | ak | Ukrainian | uk |
| Urdu | ur | Uyghur | ug | Uzbek | uz | Vietnamese | vi |
| Welsh | cy | Xhosa | xh | Yiddish | yi | Yoruba | yo |
| Zulu | zu | - | - | - | - | - | - |


---

<img width="324" height="578" alt="image" src="https://github.com/user-attachments/assets/34e6f9a7-05a5-4170-b03f-c71f553e0bee" />

⮑

<img width="314" height="578" alt="image" src="https://github.com/user-attachments/assets/8b27a06d-f28e-4c77-9ecf-0609bb46f893" />

⮑

<img width="330" height="572" alt="image" src="https://github.com/user-attachments/assets/eac5eb02-04bc-412c-afa4-92f2b946215d" />

<img width="307" height="564" alt="image" src="https://github.com/user-attachments/assets/63431645-92d6-4f6e-9440-de941af45950" />

<img width="333" height="581" alt="image" src="https://github.com/user-attachments/assets/24ff7809-0ac3-4382-a549-dbb467101e88" />

<img width="332" height="582" alt="image" src="https://github.com/user-attachments/assets/4ceab78e-1582-4050-8c0f-eab675cd423b" />

<img width="304" height="540" alt="image" src="https://github.com/user-attachments/assets/567e7864-0ddd-4b2e-8763-b331109acce7" />

<img width="337" height="555" alt="image" src="https://github.com/user-attachments/assets/0a906e54-840c-4ded-ba2e-6ab4cbc7e91f" />

<img width="334" height="549" alt="image" src="https://github.com/user-attachments/assets/02b31cb1-63ef-458c-a87c-fe1b4655b10c" />

<img width="345" height="614" alt="image" src="https://github.com/user-attachments/assets/87401260-52fb-463d-b538-225919f97f96" />

<img width="341" height="564" alt="image" src="https://github.com/user-attachments/assets/dee7b1a8-5119-4cfe-bd08-0251021b5bec" />



