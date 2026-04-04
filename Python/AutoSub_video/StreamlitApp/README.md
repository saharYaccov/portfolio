# 🎬 Video Processing Tool (Watermark Removal & Subtitles)

A Streamlit-based application for processing videos by:

* Removing watermarks from a selected region
* Transcribing audio using Whisper
* Translating subtitles
* Embedding subtitles into the final video

---

## 🚀 Features

* 🎯 Manual watermark removal using coordinate selection
* 🧠 Speech-to-text transcription (OpenAI Whisper)
* 🌍 Automatic translation (Google Translator)
* 🎞️ Subtitle generation (SRT format)
* 🔊 Audio preservation using FFmpeg
* 📥 Download final processed video

---

## 🛠️ Requirements

### 1. System Dependencies

Install **FFmpeg**:

#### macOS

```bash
brew install ffmpeg
```

#### Ubuntu

```bash
sudo apt install ffmpeg
```

#### Windows

Download from: https://ffmpeg.org/download.html
Make sure it is added to PATH.

---

### 2. Python Dependencies

Install required packages:

```bash
pip install streamlit opencv-python numpy==1.26.0 torch openai-whisper deep-translator
```

---

## ▶️ How to Run

Run the application:

```bash
streamlit run app.py
```

Then open in browser:

```
http://localhost:8501
```

---

## 📂 Project Structure

```bash
.
├── app.py
├── README.md
└── output/   # auto-created
```

---

## ⚙️ Workflow

1. Upload a video
2. Select watermark coordinates:

   * Top-left: (x₁, y₁)
   * Bottom-right: (x₂, y₂)
3. Preview watermark removal
4. Select source & target language
5. Run processing

---

## 🧠 Processing Pipeline

### Watermark Removal

```python
cv2.inpaint(frame, mask, 10, cv2.INPAINT_NS)
```

---

### Speech Recognition

```python
model.transcribe(video_path)
```

---

### Subtitle Segmentation

```python
max_words_per_segment = 6
```

---

### Translation

```python
translator.translate(text)
```

---

### Subtitle Rendering

```bash
ffmpeg -i input.mp4 -vf subtitles=subtitles.srt output.mp4
```

---

## 📐 Mathematical Representation (LaTeX)

### Frame Complexity

$$
T(n) = O(n)
$$

Where:

* ( n ) = number of frames

---

### Segmentation Formula

$$
\mathrm{S}= \left\lceil \frac{W}{k} \right\rceil
$$

Where:

* ( W ) = number of words
* ( k ) = words per segment

---

### Time Distribution

$$
\Delta t = \frac{t_{end} - t_{start}}{S}
$$

---

## ⚠️ Notes

* Whisper downloads models on first run
* GPU recommended for performance
* Requires internet for translation
* Large videos need more RAM

---

## ❗ Limitations

* Manual watermark selection
* No batch processing
* Sequential execution

---

## 💡 Future Improvements

* Auto watermark detection
* GPU optimization
* Batch processing
* UI improvements

---

## 👨‍💻 Author

Created by **S.Y**

