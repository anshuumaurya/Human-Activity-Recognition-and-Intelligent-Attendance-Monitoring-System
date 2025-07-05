import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime
import pandas as pd

# Set correct path for known faces
KNOWN_PATH = "images"
UNAUTHORIZED_LOG = "Unauthorized_Log.csv"
ATTENDANCE_LOG = "Attendance.csv"

# Load known faces
def load_known_faces(path):
    known_encodings = []
    known_names = []
    for filename in os.listdir(path):
        if filename.endswith(('.jpg', '.png', '.jpeg')):
            image = face_recognition.load_image_file(os.path.join(path, filename))
            encoding = face_recognition.face_encodings(image)
            if encoding:
                known_encodings.append(encoding[0])
                name = os.path.splitext(filename)[0]
                known_names.append(name)
    return known_encodings, known_names

# Mark attendance
def mark_attendance(name):
    now = datetime.now()
    dt_string = now.strftime('%Y-%m-%d %H:%M:%S')
    if not os.path.exists(ATTENDANCE_LOG):
        with open(ATTENDANCE_LOG, 'w') as f:
            f.write('Name,Time\n')
    with open(ATTENDANCE_LOG, 'r+') as f:
        lines = f.readlines()
        names_recorded = [line.split(',')[0] for line in lines[1:]]
        if name not in names_recorded:
            f.write(f'{name},{dt_string}\n')

# Log unauthorized entry
def log_unauthorized_entry(face_image):
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    img_filename = f"unauthorized_{now.strftime('%Y%m%d_%H%M%S')}.jpg"
    cv2.imwrite(img_filename, face_image)
    log_entry = {'Time': timestamp, 'Image': img_filename}
    df = pd.DataFrame([log_entry])
    if not os.path.exists(UNAUTHORIZED_LOG):
        df.to_csv(UNAUTHORIZED_LOG, index=False)
    else:
        df.to_csv(UNAUTHORIZED_LOG, mode='a', header=False, index=False)

# Main attendance function
def start_attendance_system():
    print("[INFO] Starting Attendance System")
    known_encodings, known_names = load_known_faces(KNOWN_PATH)

    cap = cv2.VideoCapture(0)

    while True:
        success, frame = cap.read()
        if not success:
            break

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small)
        face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)

            name = "Unknown"
            if matches:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_names[best_match_index]

            top, right, bottom, left = [v * 4 for v in face_location]
            face_crop = frame[top:bottom, left:right]

            if name != "Unknown":
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, f"Authorized: {name}", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                mark_attendance(name)
            else:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(frame, "Unauthorized Intrusion!", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                log_unauthorized_entry(face_crop)

        cv2.putText(frame, "Press 'b' to return to menu", (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
        cv2.imshow("Face Attendance System", frame)

        if cv2.waitKey(1) & 0xFF == ord('b'):
            break

    cap.release()
    cv2.destroyAllWindows()
