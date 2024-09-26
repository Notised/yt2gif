import os
import glob
import re

def validate_time_format(time_str):
    pattern = re.compile(r'^(?:(?:([01]?\d|2[0-3]):)?([0-5]?\d):)?([0-5]?\d)$')
    return bool(pattern.match(time_str))

def clean_up_files(temp_dir, log_queue):
    try:
        for file in glob.glob(os.path.join(temp_dir, "frame*.png")):
            os.remove(file)
        log_queue.put("Temporary files cleaned up.")
    except Exception as e:
        log_queue.put(f"Error during cleanup: {e}")