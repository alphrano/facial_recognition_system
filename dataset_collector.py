import cv2
import os

# Function to capture images for a given user ID
def capture_images(user_id, num_images=20, save_path="dataset"):
    """
    Captures images from webcam, detects the face, and saves them.

    Args:
    user_id (str): Unique ID for the user (e.g., "user_1")
    num_images (int): Number of images to capture
    save_path (str): Folder to save the images
    """

    # Create user folder if it doesn't exist
    user_folder = os.path.join(save_path, user_id)
    os.makedirs(user_folder, exist_ok=True)

    # Open webcam
    cap = cv2.VideoCapture(0)  # Use 0 for default webcam

    image_count = 0
    print("Press 'SPACE' to capture an image. Press 'q' to quit.")

    while image_count < num_images:
        ret, frame = cap.read()
        if not ret:
            print("Error: Couldn't access webcam")
            break

        # Show webcam feed
        cv2.imshow("Face Capture - Press 'SPACE' to Save", frame)

        key = cv2.waitKey(1) & 0xFF

        # Capture image when SPACE is pressed
        if key == ord(' '):
            image_path = os.path.join(user_folder, f"{image_count}.jpg")
            cv2.imwrite(image_path, frame)
            print(f"Saved: {image_path}")
            image_count += 1

        # Quit when 'q' is pressed
        elif key == ord('q'):
            print("Exiting...")
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"✅ Captured {image_count} images for {user_id}")

# Run script for a specific user
if __name__ == "__main__":
    user_id = input("Enter user ID: ")
    capture_images(user_id)
