# 🎬 YouTube Video Downloader

A modern YouTube Video Downloader built with **Kivy** and **KivyMD**. Enjoy real-time progress updates and seamless MP4 conversion with intuitive UI feedback.

---

## ✨ Features

- **Download YouTube videos** in various qualities (Best, Medium, Low)
- **Choose destination folder** via file manager
- **Automatic `.mp4` conversion** with live UI feedback
- **Real-time download & conversion progress bars**
- **Pop-up notifications** for all important actions
- **Modular and crash-resistant codebase**

---

## 🧰 Requirements

- Python 3.8+
- [Kivy](https://kivy.org/)
- [KivyMD](https://kivymd.readthedocs.io/)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [ffmpeg-python](https://github.com/kkroening/ffmpeg-python)
- [FFMPEG](https://ffmpeg.org/)

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Sarwarhridoy4/Youtube_Video_Downloader
cd Youtube_Video_Downloader
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv .venv
# For Linux/macOS:
source .venv/bin/activate
# For Windows:
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install FFmpeg

- **On Linux:**
    ```bash
    sudo apt install ffmpeg
    ```
- **On Windows 10/11:**
    ```bash
    winget install Gyan.FFmpeg
    ```
> ⚠️ Ensure ffmpeg is in your system's PATH.

---

## 🖥️ Usage

```bash
python main.py
```

**Steps:**
1. Paste a valid YouTube URL.
2. Select video quality from the dropdown.
3. Choose a folder to save the video.
4. Click **Download**.

> **Watch download + conversion progress in real-time!**

---

## 📁 Project Structure

```
Youtube_Video_Downloader/
│
├── components/
│   └── popup.py               # Reusable popup dialogs
│
├── services/
│   ├── download_service.py    # Download logic using yt-dlp
│   └── conversion_service.py  # MP4 conversion using ffmpeg
│
├── utils/
│   └── validators.py          # URL and info validation helpers
│
├── assets/
│   └── screen.png             # UI screenshot
│
├── main.py                    # App entry point
├── mainscreen.py              # UI logic and real-time control
├── requirements.txt
└── README.md
```

---

## 🔒 .gitignore

```
# Byte-compiled files
__pycache__/
**/__pycache__/
*.py[cod]

# Virtual environments
.venv/
env/

# System
.DS_Store
Thumbs.db
```

---

## 🧑‍💻 Contributing

Pull requests are welcome! If you'd like to add features or fix bugs, please fork and submit a PR.

---

## 📄 License

Licensed under the MIT License.

---

## 📸 Screenshot

![App_Screenshot](./assets/screen.png)

---

## 🙏 Acknowledgments

- [Kivy](https://kivy.org/)
- [KivyMD](https://kivymd.readthedocs.io/)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [ffmpeg-python](https://github.com/kkroening/ffmpeg-python)
- [FFmpeg](https://ffmpeg.org/)







