import os
from os.path import exists, join, splitext
from shutil import move
from time import sleep
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Use raw strings for Windows paths
source_dir = r"C:\Users\Krish\Downloads"
dest_dirs = {
    "sfx": r"C:\Users\Krish\OneDrive\Desktop\Downloaded_SFX",
    "music": r"C:\Users\Krish\OneDrive\Desktop\Downloaded_music",
    "video": r"C:\Users\Krish\OneDrive\Desktop\Downloaded_videos",
    "image": r"C:\Users\Krish\OneDrive\Desktop\Downloaded_images",
    "documents": r"C:\Users\Krish\OneDrive\Desktop\Downloaded_documents",
}

# File type extensions
image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".webp", ".tiff", ".bmp", ".ico"]
video_extensions = [".mp4", ".m4v", ".avi", ".wmv", ".mov", ".flv", ".webm"]
audio_extensions = [".m4a", ".flac", ".mp3", ".wav", ".wma", ".aac"]
document_extensions = [".doc", ".docx", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]

# Create destination directories if they don't exist
for dir_path in dest_dirs.values():
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        logging.info(f"Created directory: {dir_path}")

def make_unique(dest, name):
    """Generate a unique filename if the file already exists."""
    filename, extension = splitext(name)
    counter = 1
    while exists(join(dest, name)):
        name = f"{filename}({counter}){extension}"
        counter += 1
    return name

def move_file(dest, file_path, name):
    """Move a file to the destination, ensuring a unique name."""
    dest_path = join(dest, name)
    if exists(dest_path):
        unique_name = make_unique(dest, name)
        move(file_path, join(dest, unique_name))
    else:
        move(file_path, dest_path)
    logging.info(f"Moved file: {name} to {dest}")

class MoverHandler(FileSystemEventHandler):
    def on_created(self, event):
        """Handle new file creation events."""
        if event.is_directory:
            return  # Skip directories
        file_path = event.src_path
        name = os.path.basename(file_path)
        
        # Wait briefly to ensure the file is fully written
        sleep(1)  # Adjust delay as needed
        
        # Check if the file still exists and is stable
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            return
        
        # Process the file
        self.process_file(file_path, name)

    def process_file(self, file_path, name):
        """Determine file type and move it to the appropriate directory."""
        try:
            ext = splitext(name)[1].lower()

            # Audio files
            if ext in audio_extensions:
                size = os.path.getsize(file_path)
                if size < 10_000_000 or "SFX" in name.upper():  # 10 MB
                    move_file(dest_dirs["sfx"], file_path, name)
                else:
                    move_file(dest_dirs["music"], file_path, name)
                return

            # Video files
            if ext in video_extensions:
                move_file(dest_dirs["video"], file_path, name)
                return

            # Image files
            if ext in image_extensions:
                move_file(dest_dirs["image"], file_path, name)
                return

            # Document files
            if ext in document_extensions:
                move_file(dest_dirs["documents"], file_path, name)
                return

        except Exception as e:
            logging.error(f"Error processing {name}: {e}")

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.info("File automation script started")

    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, source_dir, recursive=False)  # Non-recursive for Downloads
    observer.start()

    logging.info(f"Watching directory: {source_dir}")
    logging.info("Press Ctrl+C to stop")

    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
        logging.info("File automation script stopped")
    observer.join()