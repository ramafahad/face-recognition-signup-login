from flask import Flask, request, render_template, jsonify
import cv2
import face_recognition
import numpy as np
import os
import base64
import mysql.connector
from database_connection import get_db_connection
from ultralytics import YOLO


phone_detect = YOLO("yolo11n.pt") 


app = Flask(__name__)

UPLOAD_FOLDER = "signed_faces"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)



@app.route('/check_email', methods=['POST'])
def check_email():
    data = request.json  
    email = data.get('email')  
    
    if not email:
        return jsonify({"message": "Email is required"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    
    if user:
        response = {"exists": True, "message": "Email already registered!"}
    else:
        response = {"exists": False, "message": ""}
    
    cursor.close()
    conn.close()
    
    return jsonify(response)


@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get("email")
    image_data = data.get("image")

    if not email or not image_data:
        return jsonify({"message": "Missing email or image data"}), 400

    image_bytes = base64.b64decode(image_data.split(',')[1])
    image_path = os.path.join(UPLOAD_FOLDER, f"{email}.jpg")

    with open(image_path, "wb") as f:
        f.write(image_bytes)

    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)

    if len(encodings) == 0:
        return jsonify({"message": "No face detected"}), 400

    encoding_array = encodings[0]
    encoding_bytes = encoding_array.tobytes()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (email, face_encoding, image_path) VALUES (%s, %s, %s)",
        (email, encoding_bytes, image_path)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Sign-up Successful!"})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get("email")
    image_data = data.get("image")

    if not email or not image_data:
        return jsonify({"message": "Missing email or image data"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT face_encoding FROM users WHERE email = %s", (email,))
    result = cursor.fetchone()
    conn.close()

    if not result:
        return jsonify({"message": "Email not found"}), 401

    stored_encoding = np.frombuffer(result[0], dtype=np.float64)

    image_bytes = base64.b64decode(image_data.split(',')[1])
    image_np = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    face_encodings = face_recognition.face_encodings(image)

    if len(face_encodings) == 0:
        return jsonify({"message": "No face detected"}), 400
    
    results = phone_detect(image)
    for result in results:
        for box in result.boxes:
            label = result.names[int(box.cls)]
            if "cell phone" in label.lower():
                return jsonify({"message": "📵 Phone detected! Authentication denied."}), 403



    match = face_recognition.compare_faces([stored_encoding], face_encodings[0])

    if match[0]:
        return jsonify({"message": "Login Successful!"})
    else:
        return jsonify({"message": "Unauthorized access"}), 401

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
