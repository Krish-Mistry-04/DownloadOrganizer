# File Automation

An automated file organizer that monitors your Downloads folder and automatically sorts files into appropriate directories based on their file type.

## Features

- **Real-time Monitoring**: Continuously monitors the Downloads folder for new files
- **Automatic File Sorting**: Categorizes files based on their extensions
- **Smart Audio Sorting**: Separates SFX and music files based on file size
- **Duplicate File Handling**: Creates unique filenames for duplicate files
- **Category Support**:
  - Audio files (MP3, WAV, FLAC, etc.)
  - Video files (MP4, AVI, MOV, etc.)
  - Image files (JPG, PNG, GIF, etc.)
  - Document files (PDF, DOCX, XLSX, etc.)

## Requirements

- Python 3.6+
- watchdog package

## Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/file-automation.git
cd file-automation
```

2. Install required dependencies:
```
pip install watchdog
```

## Configuration

Edit the directory paths in the script to match your system:

```python
source_dir = r"C:\Users\YourUsername\Downloads"
dest_dir_sfx = r"C:\Users\YourUsername\Desktop\Downloaded SFX"  
dest_dir_music = r"C:\Users\YourUsername\Desktop\Downloaded music"  
dest_dir_video = r"C:\Users\YourUsername\Desktop\Downloaded videos"  
dest_dir_image = r"C:\Users\YourUsername\Desktop\Downloaded images"  
dest_dir_documents = r"C:\Users\YourUsername\Desktop\Downloaded documents"
```

## Usage

Run the script:

```
python file_automation.py
```

The script will:
1. Create the destination folders if they don't exist
2. Start monitoring your Downloads folder
3. Automatically move files to appropriate folders as they appear
4. Log all activities in the console

To stop the script, press `Ctrl+C` in the terminal.

## How It Works

The script uses the watchdog library to monitor file system events. When a file is created or modified in the Downloads folder, the script:

1. Checks the file extension
2. Determines the appropriate destination folder
3. Moves the file to that folder
4. Creates a unique filename if a file with the same name already exists

For audio files, it makes a special distinction:
- Files smaller than 10MB or with "SFX" in the name go to the SFX folder
- All other audio files go to the music folder

## Extending

You can extend the script by:

- Adding new file extensions to the existing categories
- Creating new categories for other file types
- Customizing the sorting logic

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
