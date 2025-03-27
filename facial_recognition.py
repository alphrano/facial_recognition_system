import cv2
from deepface import DeepFace
from deepface.commons import functions
from config import DETECTOR_BACKEND, ENFORCE_DETECTION
import os

# Suppress TensorFlow warnings
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Threshold tuning (for FRR & FAR below 5%)
INITIAL_THRESHOLD = 0.6
MIN_THRESHOLD = 0.4  # Reduce False Rejection Rate (FRR)
MAX_THRESHOLD = 0.8  # Reduce False Acceptance Rate (FAR)

def detect_faces(frame):
    """Detect faces using DeepFace."""
    try:
        faces = DeepFace.extract_faces(
            frame,
            detector_backend=DETECTOR_BACKEND,
            enforce_detection=ENFORCE_DETECTION
        )
        return faces if faces else None  # Return None if no faces detected
    except Exception as e:
        print(f"🚨 Face detection error: {e}")
        return None

def draw_faces(frame, faces):
    """Draw rectangles around detected faces."""
    if faces:
        for face in faces:
            if "facial_area" in face:
                x, y, w, h = face["facial_area"].values()
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return frame

def verify_face(frame, known_face_data, threshold=INITIAL_THRESHOLD):
    """Verify face identity while dynamically adjusting the threshold."""
    try:
        # Convert to RGB and preprocess (resizes & normalizes)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        preprocessed_frame = functions.preprocess_face(
            frame_rgb, target_size=(160, 160), enforce_detection=False
        )

        if preprocessed_frame is None:
            print("⚠️ No face detected for verification.")
            return False, threshold

        # Perform verification
        result = DeepFace.verify(preprocessed_frame, known_face_data, detector_backend=DETECTOR_BACKEND)

        # Adjust threshold dynamically
        if result["verified"]:
            threshold = max(threshold - 0.02, MIN_THRESHOLD)  # Lower threshold to reduce FRR
        else:
            threshold = min(threshold + 0.02, MAX_THRESHOLD)  # Raise threshold to reduce FAR

        return result["verified"], threshold
    except Exception as e:
        print(f"🚨 Face verification error: {e}")
        return False, threshold

def anti_spoofing(frame):
    """Basic anti-spoofing (eye detection to confirm liveness)."""
    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            if len(eyes) >= 2:
                return True  # Liveness confirmed
        return False  # Possible spoofing

    except Exception as e:
        print(f"🚨 Anti-spoofing error: {e}")
        return False
