import mysql.connector
import numpy as np
from mysql.connector import Error
from werkzeug.security import generate_password_hash
from config import DB_CONFIG, COOKOUT_DB


# Helper function to connect to a database safely
def connect_db(db_config):
    try:
        return mysql.connector.connect(**db_config)
    except Error as e:
        print(f"Database connection failed: {e}")
        return None  # Prevents crash


# Functions for `cookout_db` (user credentials)
def add_user_to_cookout_db(username, email, phone, password):
    """
    Add a new user to the `cookout_db` database with hashed password.
    """
    hashed_password = generate_password_hash(password, method='sha256')  # ✅ Secure hashing

    conn = connect_db(COOKOUT_DB)
    if conn is None:
        return False

    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (username, email, phone, password)
        VALUES (%s, %s, %s, %s)
    """, (username, email, phone, hashed_password))
    conn.commit()
    cursor.close()
    conn.close()
    return True  # ✅ Indicates success


def get_user_from_cookout_db(username):
    """
    Retrieve a user from the `cookout_db` database by username.
    """
    conn = connect_db(COOKOUT_DB)
    if conn is None:
        return None

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user


# Functions for `facial_recognition` database
def add_user_to_facial_db(user_id, facial_data):
    """
    Add facial data for a user to the `facial_recognition` database.
    """
    conn = connect_db(DB_CONFIG)
    if conn is None:
        return False

    cursor = conn.cursor()

    # ✅ Convert numpy array to bytes before storing in database
    facial_data_bytes = facial_data.tobytes()

    cursor.execute("""
        INSERT INTO facial_recognition (user_id, facial_data)
        VALUES (%s, %s)
    """, (user_id, facial_data_bytes))
    conn.commit()
    cursor.close()
    conn.close()
    return True


def get_user_by_facial_data(input_embedding, threshold=0.6):
    """
    Retrieve a user from the `facial_recognition` database by comparing facial data.
    """
    conn = connect_db(DB_CONFIG)
    if conn is None:
        return None

    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM facial_recognition")
        faces = cursor.fetchall()

        if not faces:  # ✅ Check if database is empty
            return None

        for face in faces:
            stored_embedding = np.frombuffer(face["facial_data"], dtype=np.float32)

            similarity = np.dot(input_embedding, stored_embedding) / (
                    np.linalg.norm(input_embedding) * np.linalg.norm(stored_embedding)
            )

            if similarity > threshold:
                return face  # Return the matching face record
        return None

    finally:
        cursor.close()
        conn.close()
