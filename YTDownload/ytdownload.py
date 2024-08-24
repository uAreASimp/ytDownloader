import yt_dlp
import argparse
import os
import subprocess
import sys

def download_youtube_video(url, output_path='.'):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'noplaylist': True,
        'quiet': False,
        'progress_hooks': [progress_hook],
    }

    try:
        print("Starting the download...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
        
        print("\nDownload completed. Converting audio to AAC format...")
        convert_to_aac(filename, output_path)
        print("Conversion completed successfully!")
    
    except Exception as e:
        print(f"An error occurred: {e}")

def progress_hook(d):
    if d['status'] == 'downloading':
        percentage = d.get('_percent_str', '0.0%')
        speed = d.get('_speed_str', 'unknown speed')
        eta = d.get('_eta_str', 'unknown time')
        print(f"Downloading: {percentage} at {speed}, ETA: {eta}", end='\r')
    elif d['status'] == 'finished':
        print("\nDownload completed. Converting audio...")

def convert_to_aac(input_file, output_path):
    # Define output file path with AAC encoding
    output_file = os.path.join(output_path, os.path.splitext(os.path.basename(input_file))[0] + '_converted.mp4')
    
    # Command to convert audio to AAC using ffmpeg
    command = [
        'ffmpeg', '-i', input_file, 
        '-c:v', 'copy',  # Copy video stream as-is
        '-c:a', 'aac',   # Encode audio to AAC
        '-b:a', '192k',  # Set audio bitrate
        output_file
    ]
    
    try:
        # Run the ffmpeg command
        subprocess.run(command, check=True)
        # Remove the original file if conversion was successful
        os.remove(input_file)
        print(f"Converted video saved to: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error during audio conversion: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download YouTube videos and convert audio to AAC format.")
    parser.add_argument("url", help="The URL of the YouTube video to download")
    parser.add_argument("-o", "--output", default=os.path.join(os.path.expanduser('~'), 'Videos', 'Youtube'), help="The output directory (default is C:\\Users\\[NAME]\\Videos\\Youtube)")

    args = parser.parse_args()

    if not os.path.exists(args.output):
        try:
            os.makedirs(args.output)
        except OSError as e:
            print(f"Error creating directory {args.output}: {e}")
            sys.exit(1)

    print(f"Downloading video to: {args.output}")
    download_youtube_video(args.url, args.output)
