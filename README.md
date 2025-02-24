# Screen-Me: Apple Screen Mirror Python Local Service
This project implements a Python service intended for screen mirroring over a local network. Initially designed to mirror iPhone screens, the current iteration focuses on receiving and processing video files sent over the network. The service consists of a server (main.py) that listens for incoming video data and a client (mock_post.py) that sends video files to the server.

# Features
Local Network Video Receiver:
- The server listens for incoming video data on the local network.

Video Saving:
- Upon receiving video data, the server saves it as an .mp4 file on the local machine.
Automatic Playback: Once saved, the video is opened automatically using the default media player configured on the PC.
Components

Server (main.py):
- Listens for incoming video data sent over the network.
- Saves the received video as received_video.mp4.
- Automatically opens the saved video using the PC's default application for .mp4 files.

Client (mock_post.py):
- Sends a video file (video.mp4) to the server.
- Can be used to simulate the process of sending video data to the server.
- Usage

Start the Server:
- Run main.py to start the server. It will listen for incoming video data.

Send a Video:
- Use mock_post.py to send a video file (video.mp4) to the server.

Playback:
- The server saves the received video and opens it with the default video player.

# Future Enhancements
1. Implementing real-time screen mirroring capabilities for iOS devices.
2. Enhancing security and authentication for video transmission.
3. Adding support for different video formats and resolutions.

