import pickle
import numpy as np
from sklearn.metrics import accuracy_score
from deepface import DeepFace

EMBEDDINGS_PATH = "face_embeddings.pkl"


def calculate_frr_far():
    """Calculates FRR and FAR for the system."""

    # Load stored embeddings
    with open(EMBEDDINGS_PATH, "rb") as f:
        data = pickle.load(f)

    embeddings = np.array(data["embeddings"])
    labels = np.array(data["labels"])

    false_rejections = 0
    false_acceptances = 0
    total_tests = 0

    for i in range(len(embeddings)):
        test_embedding = embeddings[i]
        actual_label = labels[i]

        # Simulate verification against all users
        for j in range(len(embeddings)):
            predicted_label = labels[j]
            similarity = np.linalg.norm(test_embedding - embeddings[j])

            if similarity < 0.6 and actual_label != predicted_label:
                false_acceptances += 1
            elif similarity >= 0.6 and actual_label == predicted_label:
                false_rejections += 1

            total_tests += 1

    frr = (false_rejections / total_tests) * 100
    far = (false_acceptances / total_tests) * 100

    print(f"✅ False Rejection Rate (FRR): {frr:.2f}%")
    print(f"✅ False Acceptance Rate (FAR): {far:.2f}%")


if __name__ == "__main__":
    calculate_frr_far()
