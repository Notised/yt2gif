import subprocess
import os
import glob
from .utils import clean_up_files

def get_video_url(youtube_url, log_queue):
    try:
        result = subprocess.run(f'yt-dlp -f bestvideo -g {youtube_url}', shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        log_queue.put(f"Failed to get video URL: {e.stderr}")
        return None

def create_gif(youtube_url, start_time, end_time, fps, width, quality, output_path, log_queue):
    temp_dir = os.path.join("D", "Temp")
    os.makedirs(temp_dir, exist_ok=True)
    
    log_queue.put("Starting conversion process...")
    
    video_url = get_video_url(youtube_url, log_queue)
    if not video_url:
        return False
    
    log_queue.put(f"Video URL: {video_url}")
    
    command1 = f'ffmpeg -ss {start_time} -to {end_time} -i "{video_url}" -an -filter:v "fps={fps},scale={width}:-2:flags=bicublin" {temp_dir}/frame%03d.png'
    command2 = f'gifski -o {output_path} --quality {quality} --fps {fps} {temp_dir}/frame*.png'
    
    try:
        log_queue.put("Extracting frames...")
        subprocess.run(command1, shell=True, check=True, stderr=subprocess.PIPE, text=True)
        log_queue.put("Creating GIF...")
        subprocess.run(command2, shell=True, check=True, stderr=subprocess.PIPE, text=True)
        log_queue.put("Cleaning up temporary files...")
        clean_up_files(temp_dir, log_queue)
        log_queue.put("Conversion complete!")
        return True
    except subprocess.CalledProcessError as e:
        log_queue.put(f"An error occurred: {e}")
        log_queue.put(f"Error output: {e.stderr}")
        return False