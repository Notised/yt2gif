# yt2gif

yt2gif is a Python application that allows you to convert sections of YouTube videos into high-quality GIFs.

## Features

- Extract specific time ranges from YouTube videos
- Customize FPS and quality settings
- Simple graphical user interface
- Progress logging

## Requirements

- Python 3.6+
- FFmpeg
- yt-dlp
- gifski

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/Notised/yt2gif.git
   cd yt2gif
   ```

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Ensure you have FFmpeg, yt-dlp, and gifski installed on your system and accessible from the command line.

## Usage

Run the main.py file:

```
python main.py
```

1. Enter the YouTube URL
2. Specify the start and end times in HH:MM:SS format
3. Adjust FPS and quality settings as needed
4. Choose the output path for your GIF
5. Click "Convert" and wait for the process to complete

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.