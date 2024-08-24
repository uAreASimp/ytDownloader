# ytDownloader
i got tired of ass youtube download websites having viruses

## Setup Instructions

### 1. Download the Repository

1. **Clone the repository**:
```
git clone https://github.com/uAreASimp/ytDownloader.git
```

2. **Navigate to the repository directory**:
```
cd ytDownloader
```

### 2. Create a Batch File

1. **Create a new batch file**:
- In the repository directory, create a file named `ytdownload.bat` with the following content:
  ```
  @echo off
  python "C:\path\to\your\script\download_youtube.py" %*
  ```
- **Update the script path**: Replace `C:\path\to\your\script\download_youtube.py` with the actual path to the `download_youtube.py` script in your repository.

### 3. Add the Batch File to Your PATH

1. **Locate your PATH environment variable**:
- Open **Control Panel** -> **System and Security** -> **System** -> **Advanced system settings** -> **Environment Variables**.
2. **Edit the PATH variable**:
- In the **System variables** section, find the `Path` variable and click **Edit**.
- Add the directory where you saved `ytdownload.bat` to the PATH. Click **OK** to save the changes.

### 4. Download and Install FFmpeg

1. **Download FFmpeg**:
- Go to the [FFmpeg official website](https://ffmpeg.org/download.html) and download the appropriate version for your operating system.
2. **Extract the FFmpeg files**:
- Extract the downloaded archive to a location on your PC, for example, `C:\ffmpeg`.

### 5. Add FFmpeg to Your PATH

1. **Locate the FFmpeg `bin` directory**:
- For example, if you extracted FFmpeg to `C:\ffmpeg`, the `bin` directory will be `C:\ffmpeg\bin`.
2. **Update your PATH environment variable**:
- Go back to **Control Panel** -> **System and Security** -> **System** -> **Advanced system settings** -> **Environment Variables**.
- In the **System variables** section, find the `Path` variable and click **Edit**.
- Add the path to the `bin` directory (e.g., `C:\ffmpeg\bin`). Click **OK** to save the changes.

### 6. Install Python and Required Libraries

1. **Install Python**:
- Download and install Python from [python.org](https://www.python.org/downloads/). Make sure to check the option to add Python to your PATH during installation.
2. **Install Required Libraries**:
- Open a command prompt and run the following command to install `yt-dlp`:
  ```
  pip install yt-dlp
  ```

### 7. Using the Script

1. **Open a Command Prompt**.
2. **Run the script**:
- Use the following command to download a YouTube video and convert it to MP4 format:
  ```
  ytdownload https://www.youtube.com/watch?v=your_video_id
  ```
- **Optional**: Specify an output directory with the `-o` option:
  ```
  ytdownload https://www.youtube.com/watch?v=your_video_id -o "C:\path\to\your\output\directory"
  ```

## Troubleshooting

- **Conversion Errors**: Ensure FFmpeg is correctly installed and added to your PATH. Check the command prompt output for any FFmpeg error messages.
- **Permission Issues**: Run the command prompt as an administrator if you encounter permission issues.

## License

This project does not include a specific license. You are free to use and modify the code, but please ensure compliance with YouTube's Terms of Service and any applicable laws.

## Contact

For any questions or issues, please open an issue in the GitHub repository: [https://github.com/yourusername/yourrepository/issues](https://github.com/uAreASimp/ytDownloader/issues)

Happy downloading and converting!
