import cv2
import os

# Set user ID (change for each user)
user_id = "user_01"

# Directory to save images
save_dir = f"dataset/{user_id}"
os.makedirs(save_dir, exist_ok=True)

# Open webcam
cap = cv2.VideoCapture(0)

# Counter for image filenames
image_count = 0
total_images = 20  # Number of images to capture

print("Press 'SPACE' to capture an image. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Couldn't capture frame")
        break

    # Show webcam feed
    cv2.imshow("Press SPACE to capture", frame)

    key = cv2.waitKey(1) & 0xFF

    # Capture image when SPACE is pressed
    if key == ord(' '):
        image_path = os.path.join(save_dir, f"{user_id}_{image_count}.jpg")
        cv2.imwrite(image_path, frame)
        print(f"Saved: {image_path}")
        image_count += 1

        # Stop after capturing the required number of images
        if image_count >= total_images:
            print("Image capture complete.")
            break

    # Quit when 'q' is pressed
    elif key == ord('q'):
        break

# Release webcam
cap.release()
cv2.destroyAllWindows()
