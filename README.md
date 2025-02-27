# Face Recognition Signup & Login System
This repository provides a simple implementation of a facial recognition-based authentication system using Flask, opencv, and face_recognition. It allows users to sign up and log in securely by live-capture and compare of their facial features. The system saves the signed up accounts to phpmyadmin database.



## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ramafahad/face-recognition-signup-login.git
   
2. Install the required dependencies:
   ```bash
    pip install -r requirements.txt

3.Set up the MySQL database:
  Create a database and a table to store user data (emails and face encodings).
   ```bash
  CREATE DATABASE face_recognition;
  USE face_recognition;
  
  CREATE TABLE users (
      id INT AUTO_INCREMENT PRIMARY KEY,
      email VARCHAR(255) NOT NULL,
      face_encoding TEXT NOT NULL);
   ```

4.Configure your MySQL connection details in the database_connection.py file.

## Usage

- Start the Flask server:
   ```bash
   python app.py
   
-Allow camera access in your browser to be able to capture your face

-Signup by filling your email then clicking "Sign up with face" to capture your face, don't forget to smile!

-Login by filling your registered email then clicking "log in  with face" to verify your login attempt by comparing the live-feed to stored features


## Acknowledgements
https://codepen.io/blackellis/pen/YzwPZjy was used for UI design


