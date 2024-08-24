import yt_dlp
import argparse
import os
import subprocess
import sys

def download_youtube_video(url, output_path='.', file_type='mp4'):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',  # Use MP4 as the default merge format
        'noplaylist': True,
        'quiet': False,
        'progress_hooks': [progress_hook],
    }

    try:
        print("Starting the download...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
        
        # Only convert if the desired file type is different from the default format
        if file_type != 'mp4':
            print(f"\nDownload completed. Converting to {file_type.upper()} format...")
            convert_file(filename, output_path, file_type)
        else:
            # For video formats like mp4, ensure the audio is encoded properly
            print(f"\nDownload completed. Converting to MP4 format with AAC audio...")
            convert_video(filename, output_path)
        
        print("Operation completed successfully!")
    
    except Exception as e:
        print(f"An error occurred: {e}")

def progress_hook(d):
    if d['status'] == 'downloading':
        percentage = d.get('_percent_str', '0.0%')
        speed = d.get('_speed_str', 'unknown speed')
        eta = d.get('_eta_str', 'unknown time')
        print(f"Downloading: {percentage} at {speed}, ETA: {eta}", end='\r')
    elif d['status'] == 'finished':
        print("\nDownload completed. Converting...")

def convert_file(input_file, output_path, file_type):
    # Define output file path with specified file type
    output_file = os.path.join(output_path, os.path.splitext(os.path.basename(input_file))[0] + f'.{file_type}')
    
    # Determine the conversion command based on the file type
    if file_type == 'mp3':
        command = [
            'ffmpeg', '-i', input_file,
            '-q:a', '0',   # Best quality for MP3
            '-map', 'a',
            output_file
        ]
    elif file_type == 'wav':
        command = [
            'ffmpeg', '-i', input_file,
            '-c:a', 'pcm_s16le',  # PCM 16-bit little-endian
            output_file
        ]
    elif file_type == 'mp4':
        # This should not be needed here as `convert_video` handles MP4 conversions
        print(f"File is already in {file_type.upper()} format.")
        return
    else:
        print(f"Unsupported file type: {file_type}")
        return
    
    try:
        # Run the ffmpeg command
        subprocess.run(command, check=True)
        # Remove the original file if conversion was successful
        os.remove(input_file)
        print(f"Converted file saved to: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")

def convert_video(input_file, output_path):
    # Define output file path with MP4 format and AAC encoding
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = os.path.join(output_path, f"{base_name}_converted.mp4")
    
    # Command to convert video to MP4 format with AAC audio encoding
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
        print(f"Error during conversion: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download YouTube videos and convert to specified file format.")
    parser.add_argument("url", help="The URL of the YouTube video to download")
    parser.add_argument("type", nargs='?', default='mp4', choices=['mp3', 'wav', 'mp4'], help="The file type to convert to (default is mp4)")
    parser.add_argument("-o", "--output", default=os.path.join(os.path.expanduser('~'), 'Videos', 'Youtube'), help="The output directory (default is C:\\Users\\[NAME]\\Videos\\Youtube)")

    args = parser.parse_args()

    if not os.path.exists(args.output):
        try:
            os.makedirs(args.output)
        except OSError as e:
            print(f"Error creating directory {args.output}: {e}")
            sys.exit(1)

    print(f"Downloading video to: {args.output}")
    download_youtube_video(args.url, args.output, args.type)
