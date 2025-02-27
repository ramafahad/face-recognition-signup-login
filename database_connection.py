import mysql.connector
from cryptography.fernet import Fernet

ENCRYPTION_KEY = b'JnljgnnlhrIHYF_7rRFWE9Ephay_XT8UM9hJ6IACMLQ='  
cipher = Fernet(ENCRYPTION_KEY)

def encrypt_data(data):
    return cipher.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data):
    return cipher.decrypt(encrypted_data).decode()

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="face_auth"
    )
