import os
import numpy as np
import cv2
from deepface import DeepFace
import pickle

# Dataset path
DATASET_PATH = "dataset/"
EMBEDDINGS_PATH = "face_embeddings.pkl"

def preprocess_image(image_path):
    """Reads an image, resizes it, and converts to RGB."""
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (160, 160))  # Resize for FaceNet
    return img

def extract_embeddings():
    """Extracts facial embeddings from images and saves them."""
    face_data = []
    labels = []

    for user in os.listdir(DATASET_PATH):
        user_folder = os.path.join(DATASET_PATH, user)

        for img_name in os.listdir(user_folder):
            img_path = os.path.join(user_folder, img_name)
            img = preprocess_image(img_path)

            # Generate embeddings
            embedding = DeepFace.represent(img, model_name="Facenet", enforce_detection=False)

            if embedding:
                face_data.append(embedding[0]["embedding"])
                labels.append(user)

    # Save embeddings
    with open(EMBEDDINGS_PATH, "wb") as f:
        pickle.dump({"embeddings": np.array(face_data), "labels": labels}, f)

    print(f"✅ Face embeddings saved to {EMBEDDINGS_PATH}")

if __name__ == "__main__":
    extract_embeddings()
