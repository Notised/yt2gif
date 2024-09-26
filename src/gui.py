import PySimpleGUI as sg
import threading
import queue
from .converter import create_gif
from .utils import validate_time_format

def create_window():
    layout = [
        [sg.Text("YouTube URL:"), sg.Input(key="-URL-")],
        [sg.Text("Start Time (HH:MM:SS):"), sg.Input(key="-START-", size=(10,1)), 
         sg.Text("End Time (HH:MM:SS):"), sg.Input(key="-END-", size=(10,1))],
        [sg.Text("FPS:"), sg.Slider(range=(1, 60), default_value=15, orientation='h', size=(20, 15), key="-FPS-")],
        [sg.Text("Quality:"), sg.Combo(["480p (Good)", "640p (Balanced)", "720p (High)", "1080p (Highest)"], default_value="640p (Balanced)", key="-QUALITY-")],
        [sg.Text("Output Path:"), sg.Input(key="-OUTPUT-"), sg.FileSaveAs(file_types=(("GIF Files", "*.gif"),))],
        [sg.Button("Convert"), sg.Button("Exit")],
        [sg.Multiline(size=(60, 15), key='-LOG-', autoscroll=True, reroute_stdout=True, reroute_stderr=True, disabled=True)]
    ]
    return sg.Window("yt2gif", layout)

def convert_thread(values, log_queue, window):
    youtube_url = values["-URL-"]
    start_time = values["-START-"]
    end_time = values["-END-"]
    fps = int(values["-FPS-"])
    quality = values["-QUALITY-"]
    output_path = values["-OUTPUT-"]

    if not validate_time_format(start_time) or not validate_time_format(end_time):
        log_queue.put("Invalid time format. Please use HH:MM:SS")
        window.write_event_value('-CONVERSION-DONE-', "Failed")
        return

    quality_map = {
        "480p (Good)": (480, 75),
        "640p (Balanced)": (640, 80),
        "720p (High)": (720, 90),
        "1080p (Highest)": (1080, 99)
    }
    width, gifski_quality = quality_map[quality]

    if create_gif(youtube_url, start_time, end_time, fps, width, gifski_quality, output_path, log_queue):
        window.write_event_value('-CONVERSION-DONE-', "Success")
    else:
        window.write_event_value('-CONVERSION-DONE-', "Failed")

def run_gui(window):
    log_queue = queue.Queue()

    while True:
        event, values = window.read(timeout=100)
        
        if event == sg.WINDOW_CLOSED or event == "Exit":
            break
        
        if event == "Convert":
            threading.Thread(target=convert_thread, args=(values, log_queue, window), daemon=True).start()
        
        if event == '-CONVERSION-DONE-':
            if values[event] == "Success":
                sg.popup("Conversion complete!", "Your GIF has been created successfully.")
            else:
                sg.popup_error("An error occurred during conversion. Please check the log for details.")
        
        try:
            message = log_queue.get_nowait()
            window['-LOG-'].print(message)
        except queue.Empty:
            pass

    window.close()