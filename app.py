import sys
import os
import streamlit as st
import cv2
from pathlib import Path

# Manually add the path of pose_detection.py to the system path
sys.path.append(str(Path("/Users/krishnaarora/Desktop/YOGA").resolve()))

# Now you can import pose_detection
from Pose_detection import process_frame

st.title('Yoga Pose Detection and Alignment Feedback')

# Allow users to upload a video file
video_file = st.file_uploader("Upload a video", type=["mp4", "mov"])

if video_file is not None:
    # Save the uploaded video to a temporary file
    with open("temp_video.mp4", "wb") as f:
        f.write(video_file.read())

    cap = cv2.VideoCapture("temp_video.mp4")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Process the frame for pose detection and alignment feedback
        frame = process_frame(frame)

        # Convert the frame from BGR to RGB for display in Streamlit
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Display the frame in Streamlit
        st.image(frame_rgb, channels="RGB", use_column_width=True)

    cap.release()
