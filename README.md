# ytDownloader
i got tired of ass youtube download websites having viruses

## Setup Instructions
===============

### 1. Download the Repository
---------------------------

1. **Clone the repository**:
  ```
  git clone https://github.com/uAreASimp/ytDownloader.git
  ```
2. **Navigate to the repository directory**:
  ```
  cd ytDownloader
  ```


### 2. Use the Example Batch File
-----------------------------

1. **Locate the example batch file**:
- In the repository directory, you'll find an example batch file named `ytdownload_example.bat`.
2. **Edit the batch file**:
- Open `ytdownload_example.bat` in a text editor.
- Replace `C:\path\to\your\script\ytdownload.py` with the actual path to the `ytdownload.py` script in your repository.
3. **Rename and move the batch file**:
- Rename the file to `ytdownload.bat` and move it to a directory of your choice.

### 3. Add the Batch File to Your PATH
----------------------------------

1. **Add the batch file directory to the PATH**:
- Open a Command Prompt as Administrator.
- Use the following command to add the directory where you saved `ytdownload.bat` to the PATH:
  ```
  setx /M PATH "%PATH%;C:\path\to\your\batch\file"
  ```
- Replace `C:\path\to\your\batch\file` with the actual directory where `ytdownload.bat` is located.

### 4. Download and Install FFmpeg
-------------------------------

1. **Download FFmpeg**:
- Go to the [FFmpeg official website](https://ffmpeg.org/download.html) and download the appropriate version for your operating system.
2. **Extract the FFmpeg files**:
- Extract the downloaded archive to a location on your PC, for example, `C:\ffmpeg`.

### 5. Add FFmpeg to Your PATH
--------------------------

1. **Add the FFmpeg `bin` directory to the PATH**:
- Open a Command Prompt as Administrator.
- Use the following command to add the FFmpeg `bin` directory to the PATH:
  ```
  setx /M PATH "%PATH%;C:\ffmpeg\bin"
  ```
- Replace `C:\ffmpeg\bin` with the actual path to the `bin` directory inside your FFmpeg installation.

### 6. Install Python and Required Libraries
----------------------------------------

1. **Install Python**:
- Download and install Python from [python.org](https://www.python.org/downloads/). Make sure to check the option to add Python to your PATH during installation.
2. **Install Required Libraries**:
- Open a Command Prompt and run the following command to install `yt-dlp`:
  ```
  pip install yt-dlp
  ```

### 7. Using the Script
-------------------

1. **Open a Command Prompt**.
2. **Run the script**:
- Use the following command to download a YouTube video:
  ```
  ytdownload https://www.youtube.com/watch?v=your_video_id
  ```
- **Optional**:
  - You can also choose between mp3, wav, and mp4. It is mp4 by default:
    ```
    ytdownload https://www.youtube.com/watch?v=your_video_id [type]
    ```
  - Specify an output directory with the `-o` option:
    ```
    ytdownload -o "C:\path\to\your\output\directory" https://www.youtube.com/watch?v=your_video_id
    ```
  - Full usage:
    ```
    ytdownload -o "C:\path\to\your\output\directory" https://www.youtube.com/watch?v=your_video_id mp3
    ```

## Troubleshooting
===============

- **Conversion Errors**: Ensure FFmpeg is correctly installed and added to your PATH. Check the command prompt output for any FFmpeg error messages.
- **Permission Issues**: Run the command prompt as an administrator if you encounter permission issues.
- **No Response in CMD**: Your python installation may not have worked, try installing python again from either [python.org](https://www.python.org/downloads/) or the Microsoft Store.

## License
=======

This project does not include a specific license. You are free to use and modify the code, but please ensure compliance with YouTube's Terms of Service and any applicable laws.

### Contact
=======

For any questions or issues, please open an issue in the GitHub repository: https://github.com/uAreASimp/ytDownloader/issues
