from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.Hash import HMAC, SHA256
import base64
import os

# Secure key storage
KEY_FILE = "secret.key"

def get_aes_key():
    """
    Load the AES key from an environment variable or a key file.
    """
    if "AES_KEY" in os.environ:
        return base64.b64decode(os.environ["AES_KEY"])  # Load from env variable

    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as key_file:
            return key_file.read()

    key = get_random_bytes(32)  # Generate a new key
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)

    return key

# Load or generate the AES key
key = get_aes_key()

def derive_iv(template):
    """
    Derives an IV from the message using HMAC-SHA256.
    """
    h = HMAC.new(key, template.encode(), SHA256)
    return h.digest()[:AES.block_size]  # Use first 16 bytes as IV

def encrypt_template(template):
    """
    Encrypts the given template using AES-CBC with a derived IV.
    """
    iv = derive_iv(template)  # Deterministic IV
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct_bytes = cipher.encrypt(pad(template.encode(), AES.block_size))
    return base64.b64encode(ct_bytes).decode()

def decrypt_template(encrypted_template, original_template):
    """
    Decrypts an AES-CBC encrypted template using a derived IV.
    Requires the original template for IV derivation.
    """
    encrypted_data = base64.b64decode(encrypted_template)
    iv = derive_iv(original_template)  # Get the same IV from the original template
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return pt.decode()
