import tkinter as tk
from tkinter import ttk
from zeroconf import Zeroconf, ServiceInfo
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application
import threading
import av
import cv2
import logging
import io
import os
import subprocess
import platform

# Configure logging settings
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Network Discovery with Zeroconf
def register_service():
    desc = {'version': '1.0'}
    info = ServiceInfo(
        "_airplay._tcp.local.",
        "MyPythonAirPlay._airplay._tcp.local.",
        addresses=[b'\xC0\xA8\x01\x64'],  # Example IP address in byte format
        port=7000,  # Example port
        properties=desc,
        server="myairplay.local."
    )
    zeroconf = Zeroconf()
    zeroconf.register_service(info)
    logging.info("Service registered with Zeroconf")

# Server
class MainHandler(RequestHandler):
    def get(self):
        self.write("AirPlay-like service running")

# saves the video and plays it (optional)
class VideoHandler(RequestHandler):
    def post(self):
        try:
            video_data = self.request.body
            logging.info("Received video data")

            # Save the video data to a file
            with open("received_video.mp4", "wb") as video_file:
                video_file.write(video_data)
            
            logging.info("Video saved locally as received_video.mp4")

            # Use BytesIO to create a file-like object from the video data
            input_stream = io.BytesIO(video_data)

            # Process the video data (optional, if you still want to display it)
            # process_video(input_stream)

            # After saving the video, call this function
            play_video_with_default_player("received_video.mp4")

            self.write("Video processed and saved successfully")
        except Exception as e:
            logging.error(f"Error processing video: {e}")
            self.set_status(500)
            self.write("Error processing video")

# Playing the Raw Video using a Media Player
def play_video_with_default_player(file_path):
    try:
        if platform.system() == 'Darwin':       # macOS
            subprocess.run(['open', file_path])
        elif platform.system() == 'Windows':    # Windows
            os.startfile(file_path)
        else:                                   # Linux
            subprocess.run(['xdg-open', file_path])
    except Exception as e:
        logging.error(f"Error playing video with default player: {e}")

# plays video as image frames 
# class VideoHandler(RequestHandler):
#     def post(self):
#         try:
#             video_data = self.request.body
#             logging.info("Received video data")
#             # Use BytesIO to create a file-like object from the video data
#             input_stream = io.BytesIO(video_data)
#             # Process the video data
#             process_video(input_stream)
#             self.write("Video processed successfully")
#         except Exception as e:
#             logging.error(f"Error processing video: {e}")
#             self.set_status(500)
#             self.write("Error processing video")

def make_app():
    return Application([
        (r"/", MainHandler),
        (r"/video", VideoHandler),
    ])

def run_server():
    app = make_app()
    app.listen(7000)
    IOLoop.current().start()

# Video Processing with PyAV
def process_video(input_stream):
    try:
        container = av.open(input_stream)
        for frame in container.decode(video=0):
            img = frame.to_ndarray(format='bgr24')
            cv2.imshow('Frame', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except Exception as e:
        logging.error(f"Error processing video: {e}")
    finally:
        cv2.destroyAllWindows()

# UI with Tkinter
def start_service():
    logging.info("Starting AirPlay-like service...")
    threading.Thread(target=run_server, daemon=True).start()
    update_status("Service started")

def stop_service():
    logging.info("Stopping AirPlay-like service...")
    IOLoop.current().stop()
    update_status("Service stopped")

def update_status(message):
    status_label.config(text=message)

def run_ui():
    root = tk.Tk()
    root.title("AirPlay-like Service")

    mainframe = ttk.Frame(root, padding="10")
    mainframe.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    start_button = ttk.Button(mainframe, text="Start Service", command=start_service)
    start_button.grid(row=0, column=0, padx=5, pady=5)

    stop_button = ttk.Button(mainframe, text="Stop Service", command=stop_service)
    stop_button.grid(row=0, column=1, padx=5, pady=5)

    global status_label
    status_label = ttk.Label(mainframe, text="Service not started")
    status_label.grid(row=1, column=0, columnspan=2)

    root.mainloop()

if __name__ == "__main__":
    register_service()
    run_ui()  # Run the UI in the main thread