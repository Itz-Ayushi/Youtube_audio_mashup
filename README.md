# 🎵 YouTube Singer Mashup Generator

A command-line Python application that automatically creates a mashup by:

- 🔍 Downloading **N YouTube videos** of a specified singer  
- 🎧 Extracting audio from each video  
- ✂️ Trimming the first **Y seconds** from each audio  
- 🔀 Merging all trimmed clips into a single MP3 output file  

This project demonstrates automation of multimedia processing using Python and third-party libraries.

---

## 🚀 Features

✔ Download multiple YouTube videos automatically  
✔ Extract high-quality audio  
✔ Trim fixed duration from each file  
✔ Merge multiple audio clips into one output file  
✔ Command-line execution  
✔ Input validation  
✔ Exception handling  
✔ Automatic cleanup of temporary files  

---

## 🛠️ Technologies Used

- Python 3.x
- [yt-dlp](https://pypi.org/project/yt-dlp/)
- [moviepy](https://pypi.org/project/moviepy/)
- [pydub](https://pypi.org/project/pydub/)
- FFmpeg

---

## 📦 Installation Guide

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name
```

### 2️⃣ Install Required Python Packages

```bash
pip install yt-dlp moviepy pydub ffmpeg-python
```


### 3️⃣ Install FFmpeg 

Download FFmpeg from:
https://www.gyan.dev/ffmpeg/builds/

After downloading:

Either add ffmpeg to your system PATH

OR copy ffmpeg.exe and ffprobe.exe into the project folder

---

### ▶️ Usage

1. CLI Mode (<RollNumber>.py)

```bash
python <RollNumber>.py "<SingerName>" <NumberOfVideos> <AudioDuration> <OutputFileName>
```
Example
```bash
python 102317237.py "Taylor Swift" 15 30 mashup.mp3
```

2. Web Mode (app.py)
   Launch the Flask server for a graphical interface:
   ```bash
   python app.py
   ```
Open http://127.0.0.1:5000 in your browser.
Fill in the singer name, counts ($>10$), duration ($>20$), and your email.
The mashup will be generated and sent as a .zip attachment to your inbox.
---
## 📌 Parameter Rules

| Parameter      | Description                   | Constraint              |
| -------------- | ----------------------------- | ----------------------- |
| SingerName     | Name of the singer            | Any valid name          |
| NumberOfVideos | Number of videos to download  | Must be greater than 10 |
| AudioDuration  | Duration to trim (in seconds) | Must be greater than 20 |
| OutputFileName | Final mashup file name        | Must end with `.mp3`    |

---

---

## 🔐 Configuration (Email Setup)

To enable the email delivery feature in `app.py`, you must update the sender credentials. For security, do not use your primary account password.

### **Gmail Setup**
1. **Enable 2FA**: Ensure Two-Factor Authentication is active on your Google account.
2. **Generate App Password**: 
   * Go to your **Google Account Settings** > **Security**.
   * Search for **App Passwords**.
   * Select **Mail** and choose **Other** (name it "Mashup Project").
   * Copy the 16-character code provided.

### **Update Credentials**
Update the following variables in your `app.py` file:

```python
# Configuration in app.py
sender_email = "your-email@gmail.com"
sender_password = "xxxx xxxx xxxx xxxx" # Your 16-character app password
```
---

## ⚠️ Troubleshooting

* **Import Errors**: If VS Code displays "Import could not be resolved," ensure you have synced the IDE with your environment. Press `Ctrl+Shift+P`, type **Python: Select Interpreter**, and choose the environment where you installed your packages.
* **FFmpeg Errors**: Audio processing requires FFmpeg. Confirm the binary is correctly installed and accessible via your system's command line by running `ffmpeg -version`.
* **SMTP Failures**: For security, modern email providers block standard passwords for scripts. Ensure you are using a dedicated 16-character **App Password** rather than your standard account password.

---

## 📜 License

This project is developed strictly for educational purposes. Users are responsible for ensuring their use of this tool complies with **YouTube's Terms of Service** and local copyright regulations regarding downloaded content. No warranties are provided.
