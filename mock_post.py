import requests

"""
    first run server main.py and start service
    this mock_post.py will send the video2.mp4 file to the server and the server will receive that video and play it back
"""

# Path to the video file you want to send
video_file_path = './test/video2.mp4'

# Server URL
url = 'http://localhost:7000/video'

# Open the video file in binary mode and send it as a POST request
with open(video_file_path, 'rb') as video_file:
    try:
        response = requests.post(url, data=video_file)
        if response.status_code == 200:
            print("Video sent successfully!")
        else:
            print(f"Failed to send video. Server responded with status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")