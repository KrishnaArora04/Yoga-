import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose()

def calculate_angle(a, b, c):
    """
    Calculate the angle between three points (in radians).
    Parameters:
    a, b, c - tuples of (x, y) coordinates
    """
    a = np.array(a)  # First joint (e.g., shoulder)
    b = np.array(b)  # Second joint (e.g., elbow)
    c = np.array(c)  # Third joint (e.g., wrist)
    
    # Calculate angle using the atan2 function
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)  # Convert radians to degrees
    return angle if angle <= 180 else 360 - angle  # Ensure the angle is within [0, 180]

def process_frame(image):
    """
    Process a single frame to detect poses and calculate angles for feedback.
    """
    # Convert the frame to RGB (MediaPipe requires RGB images)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    if results.pose_landmarks:
        # Draw landmarks on the image
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
        # Extract landmark coordinates
        landmarks = results.pose_landmarks.landmark
        
        # Calculate the angles for key joints (e.g., shoulder, elbow, wrist)
        shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        
        # Calculate elbow angle
        angle = calculate_angle(shoulder, elbow, wrist)
        
        # Add the angle text on the frame
        cv2.putText(image, f"Elbow Angle: {int(angle)}", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Provide feedback based on the angle
        if angle < 70:
            feedback = "Straighten your arm!"
        elif angle > 160:
            feedback = "Elbow too straight!"
        else:
            feedback = "Good elbow position!"
        
        # Display the feedback on the frame
        cv2.putText(image, feedback, (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    return image

def main():
    """
    Main function to capture video, process frames, and display the result.
    """
    # Open the video file (or use the webcam)
    cap = cv2.VideoCapture("/Users/krishnaarora/Desktop/YOGA/pose.mp4")  # Replace with your video path

    # Read and process the frames in the video
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Process the current frame for pose detection and alignment feedback
        frame = process_frame(frame)

        # Display the processed frame with pose landmarks and feedback
        cv2.imshow("Pose Detection & Alignment Feedback", frame)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    # Release the video capture object and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
