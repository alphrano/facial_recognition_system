import cv2
import numpy as np
from deepface import DeepFace
from deepface.commons import functions
from database import add_user_to_cookout_db
import sys
import os

# Suppress TensorFlow warnings
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'


def capture_image():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Error: Could not access the webcam. Please check if it's connected.")
        sys.exit(1)

    print("🎥 Webcam is ON. Press 's' to capture an image, or 'q' to exit.")

    captured_frame = None

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Error: Failed to capture a frame.")
                break

            cv2.imshow("📸 Capture Image (Press 's' to Save, 'q' to Quit)", frame)

            key = cv2.waitKey(1)
            if key == ord('s'):
                captured_frame = frame.copy()
                print("✅ Image captured successfully!")
                break
            elif key == ord('q'):
                print("🔴 Exiting without saving.")
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()

    return captured_frame


def enroll_user():
    try:
        username = input("👤 Enter username: ")
        email = input("📧 Enter email: ")
        phone = input("📞 Enter phone number: ")

        image = capture_image()
        if image is None:
            print("⚠️ No image captured. Enrollment aborted.")
            return

        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Preprocess image
        image_rgb = functions.preprocess_face(image_rgb, target_size=(160, 160), enforce_detection=False)

        print("🕵️‍♂️ Processing facial embeddings...")

        try:
            embeddings = DeepFace.represent(image_rgb, model_name="Facenet", enforce_detection=False)

            if not embeddings or len(embeddings) == 0:
                print("❌ Error: No face detected in the image.")
                return

        except Exception as e:
            print(f"🚨 DeepFace error: {str(e)}")
            return

        # Convert embeddings to bytes for database storage
        facial_data = np.array(embeddings[0]["embedding"], dtype=np.float32).tobytes()

        # Save user to the database
        add_user_to_cookout_db(username, email, phone, facial_data)
        print(f"✅ User {username} enrolled successfully!")

    except KeyboardInterrupt:
        print("\n🔴 Enrollment canceled by user.")
    except Exception as e:
        print(f"🚨 Error during enrollment: {str(e)}")


if __name__ == "__main__":
    enroll_user()
