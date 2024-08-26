import tkinter as tk
from tkinter import filedialog, messagebox
import yt_dlp
import os
import subprocess
import sys
import threading

def get_ffmpeg_path():
    if hasattr(sys, '_MEIPASS'):
        path = os.path.join(sys._MEIPASS, 'ffmpeg', 'ffmpeg.exe')
    else:
        path = os.path.join(os.path.dirname(__file__), 'ffmpeg', 'ffmpeg.exe')
    return path

def get_yt_dlp_path():
    if hasattr(sys, '_MEIPASS'):
        path = os.path.join(sys._MEIPASS, 'yt-dlp', 'yt-dlp.exe')
    else:
        path = os.path.join(os.path.dirname(__file__), 'yt-dlp', 'yt-dlp.exe')
    return path

def download_youtube_video(url, output_path, file_type, open_directory):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'noplaylist': True,
        'quiet': False,
        'progress_hooks': [lambda d: progress_hook(d, progress_label, root)],
        'ffmpeg_location': get_ffmpeg_path(),
        'force': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
        
        if file_type != 'mp4':
            convert_file(filename, output_path, file_type)
        else:
            convert_video(filename, output_path)
        
        if open_directory:
            open_file_explorer(output_path)
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def progress_hook(d, progress_label, root):
    if d['status'] == 'downloading':
        percentage = d.get('_percent_str', '0.0%')
        speed = d.get('_speed_str', 'unknown speed')
        eta = d.get('_eta_str', 'unknown time')
        title = d.get('info_dict', {}).get('title', 'Unknown Title')
        progress_label.config(text=f"Downloading '{title}', {percentage} at {speed}, ETA: {eta}")
        root.update_idletasks()
    elif d['status'] == 'finished':
        progress_label.config(text="Download completed. Fixing audio...")

def convert_file(input_file, output_path, file_type):
    output_file = os.path.join(output_path, os.path.splitext(os.path.basename(input_file))[0] + f'.{file_type}')
    ffmpeg_path = get_ffmpeg_path()
    if file_type == 'mp3':
        command = [ffmpeg_path, '-y', '-i', input_file, '-q:a', '0', '-map', 'a', output_file]
    elif file_type == 'wav':
        command = [ffmpeg_path, '-y', '-i', input_file, '-c:a', 'pcm_s16le', output_file]
    
    try:
        subprocess.run(command, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        os.remove(input_file)
        progress_label.config(text=f"Download completed! Saved at {output_file}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error during conversion: {e}")

def convert_video(input_file, output_path):
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = os.path.join(output_path, f"{base_name}_converted.mp4")
    ffmpeg_path = get_ffmpeg_path()
    command = [
        ffmpeg_path, '-y', '-i', input_file,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-b:a', '192k',
        output_file
    ]
    
    try:
        subprocess.run(command, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        os.remove(input_file)

        # Rename the output file to remove "_converted"
        final_output_file = os.path.join(output_path, f"{base_name}.mp4")
        os.rename(output_file, final_output_file)
        
        progress_label.config(text=f"Download completed! Saved at {final_output_file}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error during conversion: {e}")


def open_file_explorer(path):
    try:
        if sys.platform == 'win32':
            os.startfile(path)
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', path])
        else:
            subprocess.Popen(['xdg-open', path])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open file explorer: {e}")

def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        directory_entry.delete(0, tk.END)
        directory_entry.insert(0, directory)

def start_download():
    url = url_entry.get()
    file_type = format_var.get()
    output_path = directory_entry.get()
    open_directory = open_dir_var.get()

    if not output_path:
        output_path = os.path.join(os.path.expanduser('~'), 'Videos', 'Youtube')
        if not os.path.exists(output_path):
            os.makedirs(output_path)
    
    if not url:
        messagebox.showwarning("Input Error", "Please provide a YouTube URL.")
        return

    try:
        with yt_dlp.YoutubeDL() as ydl:
            info_dict = ydl.extract_info(url, download=False)
            title = info_dict.get('title', 'Unknown Title')
            ext = 'mp4' if file_type == 'mp4' else file_type
            output_file = os.path.join(output_path, f"{title}.{ext}")

            if os.path.exists(output_file):
                os.remove(output_file)
            
    except Exception as e:
        messagebox.showerror("Error", f"Failed to extract video information: {e}")
        return

    progress_label.config(text="Starting download...")
    root.update_idletasks()

    # Start the download in a separate thread
    download_thread = threading.Thread(target=download_youtube_video, args=(url, output_path, file_type, open_directory))
    download_thread.start()

# Create the main application window
root = tk.Tk()
root.title("YouTube Downloader")

# YouTube URL input
tk.Label(root, text="YouTube URL:").grid(row=0, column=0, padx=10, pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10)

# Output directory selection
tk.Label(root, text="Output Directory:").grid(row=1, column=0, padx=10, pady=10)
directory_entry = tk.Entry(root, width=50)
directory_entry.grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=browse_directory).grid(row=1, column=2, padx=10, pady=10)

# Format selection
tk.Label(root, text="Format:").grid(row=2, column=0, padx=10, pady=10)
format_var = tk.StringVar(value="mp4")
tk.OptionMenu(root, format_var, "mp4", "mp3", "wav").grid(row=2, column=1, padx=10, pady=10)

# Open directory checkbox
open_dir_var = tk.BooleanVar(value=False)
open_dir_checkbox = tk.Checkbutton(root, text="Open directory after download", variable=open_dir_var)
open_dir_checkbox.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Download progress label
progress_label = tk.Label(root, text="")
progress_label.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

# Download button
tk.Button(root, text="Download", command=start_download).grid(row=5, column=0, columnspan=3, padx=10, pady=20)

# Run the application
root.mainloop()
