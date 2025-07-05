# total_people.py

import cv2
from datetime import datetime

def start_total_people_counter():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    cap = cv2.VideoCapture(0)

    print("[INFO] Starting Total People Detection (Press 'b' to return to menu)")

    while True:
        success, frame = cap.read()
        if not success:
            print("Failed to access webcam.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        now = datetime.now()
        date_time_str = now.strftime("%A, %B %d, %Y - %I:%M:%S %p")

        # Draw UI text
        cv2.putText(frame, date_time_str, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Total People: {len(faces)}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Draw rectangles around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

        # Exit hint
        cv2.putText(frame, "Press 'b' to return to menu", (10, frame.shape[0] - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.imshow("Total People Detection", frame)

        key = cv2.waitKey(1)
        if key == ord('b'):
            break

    cap.release()
    cv2.destroyAllWindows()
