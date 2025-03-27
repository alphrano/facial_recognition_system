import cv2
import os
import numpy as np
import json
from deepface import DeepFace
from deepface.commons import functions
from facial_recognition import detect_faces, draw_faces, verify_face, anti_spoofing
from encryption import encrypt_template
from notification import send_email_notification
from config import ADMIN_EMAIL, DETECTOR_BACKEND
from database import get_user_by_facial_data
from custom_logging import (
    log_auth_success,
    log_auth_failure,
    log_system_event,
    log_error
)

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # Suppress TensorFlow warnings

# Dynamic threshold settings
INITIAL_THRESHOLD = 0.6
current_threshold = INITIAL_THRESHOLD

# Start webcam feed
cap = cv2.VideoCapture(0)
log_system_event("Facial recognition system started")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            log_error("Failed to capture video frame", "Camera initialization")
            break

        # Detect faces
        faces = detect_faces(frame)

        if faces:
            frame = draw_faces(frame, faces)

            for face in faces:
                try:
                    if "facial_area" not in face:
                        continue

                    # Extract face region
                    x, y, w, h = (
                        face["facial_area"]["x"],
                        face["facial_area"]["y"],
                        face["facial_area"]["w"],
                        face["facial_area"]["h"],
                    )
                    face_region = frame[y:y + h, x:x + w]

                    # Anti-spoofing check on the cropped face
                    if not anti_spoofing(face_region):
                        log_auth_failure("Potential spoofing detected")
                        print("Potential spoofing detected! Access denied.")
                        continue

                    # Convert BGR to RGB and preprocess face
                    face_region_rgb = cv2.cvtColor(face_region, cv2.COLOR_BGR2RGB)
                    preprocessed_face = functions.preprocess_face(
                        face_region_rgb, target_size=(160, 160), enforce_detection=False
                    )

                    # Extract embeddings
                    embeddings = DeepFace.represent(
                        preprocessed_face,
                        model_name="Facenet",
                        enforce_detection=False
                    )

                    if not embeddings:
                        log_auth_failure("No face embeddings extracted")
                        continue

                    facial_data = embeddings[0]["embedding"]

                    # Convert to bytes for database lookup
                    facial_data_bytes = np.array(facial_data, dtype=np.float32).tobytes()
                    user = get_user_by_facial_data(facial_data_bytes)

                    if user:
                        is_verified, current_threshold = verify_face(
                            face_region, user["stored_embeddings"], current_threshold
                        )

                        if is_verified:
                            # Encrypt template with JSON format
                            facial_data_json = json.dumps(facial_data.tolist())
                            encrypted_template = encrypt_template(facial_data_json)

                            print(f"Authorized: {user['username']}, Template: {encrypted_template}")
                            log_auth_success(user['username'])

                            send_email_notification(
                                ADMIN_EMAIL,
                                "Access Granted",
                                f"User {user['username']} authenticated successfully."
                            )
                        else:
                            log_auth_failure("Verification failed", str(facial_data[:10]))
                    else:
                        log_auth_failure("Unknown user", str(facial_data[:10]))

                except Exception as e:
                    log_error(str(e), "Face processing loop")
                    continue

        # Display video feed
        cv2.imshow("Facial Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            log_system_event("System shutdown initiated by user")
            break

except Exception as e:
    log_error(str(e), "Main execution loop")
    print(f"Critical error: {e}. Restarting system...")
    cap.release()
    cv2.destroyAllWindows()
    cap = cv2.VideoCapture(0)  # Restart webcam

finally:
    cap.release()
    cv2.destroyAllWindows()
    log_system_event("System resources released")
