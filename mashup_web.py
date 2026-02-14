from flask import Flask, request, render_template_string, redirect, url_for
import yt_dlp
from pydub import AudioSegment
import glob
import os
import zipfile
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import re
import threading
import time

app = Flask(__name__)

# HTML form template
HTML_FORM = """
<!DOCTYPE html>
<html>
<head><title>Mashup Generator</title></head>
<body>
    <h1>Create Your Audio Mashup</h1>
    <form method="post" action="/generate">
        Singer Name: <input type="text" name="singer" required><br><br>
        Number of Videos (N > 10): <input type="number" name="n" min="11" required><br><br>
        Duration per Video (Y > 20 seconds): <input type="number" name="y" min="21" required><br><br>
        Your Email ID: <input type="email" name="email" required><br><br>
        <input type="submit" value="Generate Mashup">
    </form>
</body>
</html>
"""

# Processing page template
PROCESSING_PAGE = """
<!DOCTYPE html>
<html>
<head><title>Processing...</title></head>
<body>
    <h1>Your mashup is being generated!</h1>
    <p>This may take several minutes. You'll receive an email with the ZIP file when it's ready.</p>
    <p><a href="/">Back to Form</a></p>
</body>
</html>
"""

def generate_mashup(singer, n, y, email):
    """Background function to generate and email the mashup."""
    try:
        # Ensure downloads directory exists
        os.makedirs('downloads', exist_ok=True)
        
        # yt-dlp options
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'noplaylist': True,
            'quiet': True,
            'extractaudio': True,
            'audioformat': 'mp3',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
        }
        
        # Download
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            search_query = f"ytsearch{n}:{singer}"
            ydl.extract_info(search_query, download=True)
        
        # Process
        files = glob.glob('downloads/*.mp3')
        if len(files) < n:
            raise Exception(f"Only {len(files)} files downloaded, but {n} required.")
        
        trimmed_clips = []
        for file in files[:n]:
            audio = AudioSegment.from_mp3(file)
            trimmed = audio[:y * 1000]
            trimmed_clips.append(trimmed)
        
        if not trimmed_clips:
            raise Exception("No valid audio files to process.")
        
        combined = sum(trimmed_clips)
        output_file = "mashup.mp3"
        combined.export(output_file, format="mp3")
        
        # Compress into ZIP
        zip_name = "mashup.zip"
        with zipfile.ZipFile(zip_name, 'w') as zf:
            zf.write(output_file)
        
        # Email the ZIP
        send_email(email, zip_name, success=True)
        
        # Cleanup
        os.remove(output_file)
        os.remove(zip_name)
        for file in files:
            os.remove(file)
    
    except Exception as e:
        # Email failure notification
        send_email(email, None, success=False, error=str(e))

def send_email(recipient, zip_name=None, success=True, error=None):
    """Send email with attachment or error message."""
    try:
        # Email configuration
        sender_email = "ayushisingh.asingh@gmail.com"  
        sender_password = "myapppassword"  
        smtp_server = "smtp.gmail.com"  
        smtp_port = 587
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient
        if success:
            msg['Subject'] = "Your Audio Mashup is Ready!"
            body = "Your mashup has been generated successfully. Find the ZIP file attached."
        else:
            msg['Subject'] = "Mashup Generation Failed"
            body = f"Sorry, there was an error generating your mashup: {error}. Please try again."
        
        msg.attach(MIMEText(body, 'plain'))
        
        if zip_name and success:
            # Attach ZIP
            part = MIMEBase('application', 'octet-stream')
            with open(zip_name, 'rb') as f:
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={zip_name}')
            msg.attach(part)
        
        # Send with retry
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient, msg.as_string())
        server.quit()
    
    except Exception as e:
        print(f"Email sending failed: {e}")  # Log to console (in production, use logging)

@app.route('/')
def index():
    return render_template_string(HTML_FORM)

@app.route('/generate', methods=['POST'])
def generate():
    singer = request.form.get('singer').strip()
    n_str = request.form.get('n').strip()
    y_str = request.form.get('y').strip()
    email = request.form.get('email').strip()
    
    # Validate inputs
    if not all([singer, n_str, y_str, email]):
        return "Error: All fields are required."
    
    try:
        n = int(n_str)
        if n <= 10:
            raise ValueError
    except ValueError:
        return "Error: Number of Videos must be an integer > 10."
    
    try:
        y = int(y_str)
        if y <= 20:
            raise ValueError
    except ValueError:
        return "Error: Duration must be an integer > 20 seconds."
    
    # Validate email format
    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        return "Error: Invalid email format."
    
    # Start background thread for mashup generation
    thread = threading.Thread(target=generate_mashup, args=(singer, n, y, email))
    thread.start()
    
    # Redirect to processing page
    return render_template_string(PROCESSING_PAGE)

if __name__ == '__main__':
    app.run(debug=True, threaded=True)  # Enable threading for Flask