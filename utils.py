import numpy as np

def calculate_angle(a, b, c):
    """
    Calculate the angle between three points: a, b, c.
    Parameters a, b, c are (x, y) coordinates of keypoints.
    """
    a = np.array(a)  # Joint 1 (e.g., shoulder)
    b = np.array(b)  # Joint 2 (e.g., elbow)
    c = np.array(c)  # Joint 3 (e.g., wrist)
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    return angle if angle <= 180 else 360 - angle
