import sys
import os
import yt_dlp
from pydub import AudioSegment
import glob

def main():
    # Validate command-line arguments
    if len(sys.argv) != 5:
        print("Usage: python mashup_cli.py SingerName NumberOfVideos AudioDuration OutputFileName")
        print("Example: python mashup_cli.py 'Taylor Swift' 15 30 mashup.mp3")
        sys.exit(1)
    
    singer = sys.argv[1]
    try:
        n = int(sys.argv[2])
        if n <= 10:
            raise ValueError("NumberOfVideos must be > 10")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    try:
        y = int(sys.argv[3])
        if y <= 20:
            raise ValueError("AudioDuration must be > 20 seconds")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    output_filename = sys.argv[4]
    
    # Ensure downloads directory exists
    os.makedirs('downloads', exist_ok=True)
    
    # yt-dlp options for downloading audio
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
    
    # Download the first N audio streams
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            search_query = f"ytsearch{n}:{singer}"
            ydl.extract_info(search_query, download=True)
    except Exception as e:
        print(f"Network error during download: {e}")
        sys.exit(1)
    
    # Process downloaded files: Trim first Y seconds
    files = glob.glob('downloads/*.mp3')
    if len(files) < n:
        print(f"Error: Only {len(files)} files downloaded, but {n} required.")
        sys.exit(1)
    
    trimmed_clips = []
    for file in files[:n]:  # Use only the first N files
        try:
            audio = AudioSegment.from_mp3(file)
            trimmed = audio[:y * 1000]  # pydub uses milliseconds
            trimmed_clips.append(trimmed)
        except Exception as e:
            print(f"Error processing {file}: {e}")
            continue
    
    if not trimmed_clips:
        print("No valid audio files to process.")
        sys.exit(1)
    
    # Merge all trimmed clips
    combined = sum(trimmed_clips)
    combined.export(output_filename, format="mp3")
    
    print(f"Mashup created successfully: {output_filename}")
    
    # Cleanup: Remove downloaded files (optional)
    for file in files:
        os.remove(file)

if __name__ == "__main__":
    main()