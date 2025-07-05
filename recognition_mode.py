import cv2
import mediapipe as mp
import time
import pandas as pd
from datetime import datetime
from dashboard import activity_data, actual_activities, predicted_activities, save_activity_data

def start_motion_activity_system(mode="Activity"):
    mp_pose = mp.solutions.pose
    mp_face_mesh = mp.solutions.face_mesh
    pose = mp_pose.Pose()
    face_mesh = mp_face_mesh.FaceMesh()

    video = cv2.VideoCapture(0)
    last_activity = None
    activity_start_time = time.time()

    standing_time = sitting_time = head_down_time = hands_up_time = 0
    sleeping_time = using_phone_time = absent_time = 0

    absence_count = 0
    person_was_present = True
    absent_start_time = None

    phone_detection_counter = 0
    sleeping_detection_counter = 0
    prev_landmarks = None
    body_motion_history = []

    debug_counter = 0
    debug_frequency = 30

    def is_sleeping(face_landmarks, motion):
        try:
            left_eye_top = face_landmarks[159]
            left_eye_bottom = face_landmarks[23]
            right_eye_top = face_landmarks[386]
            right_eye_bottom = face_landmarks[374]

            def ear(top, bottom):
                return abs(top.y - bottom.y)

            left_ear = ear(left_eye_top, left_eye_bottom)
            right_ear = ear(right_eye_top, right_eye_bottom)
            eye_closed = left_ear < 0.035 and right_ear < 0.035
            low_motion = len(motion) >= 20 and sum(motion[-20:]) / 20 < 0.015

            return eye_closed and low_motion
        except:
            return False

    def is_using_phone(landmarks, face_landmarks):
        if landmarks is None or face_landmarks is None:
            return False
        try:
            nose = face_landmarks[1]
            left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
            right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
            left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
            right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]

            def dist(p1, p2):
                return ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5

            lw_dist = dist(left_wrist, nose)
            rw_dist = dist(right_wrist, nose)

            lw_up = left_wrist.y < left_elbow.y
            rw_up = right_wrist.y < right_elbow.y

            return (lw_dist < 0.3 and lw_up) or (rw_dist < 0.3 and rw_up)
        except:
            return False

    def detect_activity(landmarks, face_landmarks):
        nonlocal prev_landmarks, phone_detection_counter, sleeping_detection_counter
        nonlocal body_motion_history, debug_counter

        if landmarks is None:
            return "No Person Detected"

        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
        right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
        left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
        nose = landmarks[mp_pose.PoseLandmark.NOSE.value]
        left_ear = landmarks[mp_pose.PoseLandmark.LEFT_EAR.value]
        right_ear = landmarks[mp_pose.PoseLandmark.RIGHT_EAR.value]

        hip_avg_y = (left_hip.y + right_hip.y) / 2
        shoulder_avg_y = (left_shoulder.y + right_shoulder.y) / 2
        knee_avg_y = (left_knee.y + right_knee.y) / 2
        wrist_avg_y = (left_wrist.y + right_wrist.y) / 2
        ear_avg_y = (left_ear.y + right_ear.y) / 2

        debug_counter += 1

        # Phone detection
        if is_using_phone(landmarks, face_landmarks):
            phone_detection_counter += 1
            if phone_detection_counter > 15:
                return "Using Phone"
        else:
            phone_detection_counter = max(0, phone_detection_counter - 2)

        # Motion tracking
        if prev_landmarks:
            motion = sum(
                abs(landmarks[i].x - prev_landmarks[i].x) +
                abs(landmarks[i].y - prev_landmarks[i].y)
                for i in range(len(landmarks))
            ) / len(landmarks)
            body_motion_history.append(motion)
            if len(body_motion_history) > 30:
                body_motion_history.pop(0)
        else:
            motion = 0

        prev_landmarks = landmarks

        # Sleeping detection
        if is_sleeping(face_landmarks, body_motion_history):
            sleeping_detection_counter += 3
            if debug_counter % debug_frequency == 0:
                print(f"[DEBUG] Sleeping counter: {sleeping_detection_counter}/90")
            if sleeping_detection_counter > 90:
                return "Sleeping"
        else:
            sleeping_detection_counter = max(0, sleeping_detection_counter - 1)

        if nose.y > ear_avg_y + 0.05:
            return "Head Down"
        if wrist_avg_y < shoulder_avg_y:
            return "Hands Up"
        if abs(shoulder_avg_y - hip_avg_y) > 0.1 and knee_avg_y < hip_avg_y:
            return "Standing"
        if knee_avg_y > hip_avg_y:
            return "Sitting"

        return "Unknown Activity"

    def return_to_menu():
        from main_menu import main_menu
        save_activity_data()
        video.release()
        cv2.destroyAllWindows()
        main_menu()

    while True:
        success, frame = video.read()
        if not success:
            break

        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pose_results = pose.process(img_rgb)
        face_results = face_mesh.process(img_rgb)

        landmarks = pose_results.pose_landmarks.landmark if pose_results.pose_landmarks else None
        face_landmarks = face_results.multi_face_landmarks[0].landmark if face_results.multi_face_landmarks else None

        if landmarks:
            activity = detect_activity(landmarks, face_landmarks)

            current_time = time.time()
            if last_activity and last_activity != activity:
                duration = current_time - activity_start_time
                if last_activity == "Standing": standing_time += duration
                elif last_activity == "Sitting": sitting_time += duration
                elif last_activity == "Head Down": head_down_time += duration
                elif last_activity == "Hands Up": hands_up_time += duration
                elif last_activity == "Sleeping": sleeping_time += duration
                elif last_activity == "Using Phone": using_phone_time += duration
                activity_start_time = current_time
                last_activity = activity
            elif not last_activity:
                last_activity = activity
                activity_start_time = current_time

            actual_activities.append(activity)
            predicted_activities.append(activity)

            person_was_present = True
            if absent_start_time:
                absent_time += time.time() - absent_start_time
                absent_start_time = None

        else:
            activity = "No Person Detected"
            if person_was_present:
                person_was_present = False
                absent_start_time = time.time()
                absence_count += 1

            current_absent_duration = time.time() - absent_start_time if absent_start_time else 0
            if absence_count == 1 and current_absent_duration > 5:
                cv2.putText(frame, "Absence detected!", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
            elif absence_count == 2 and current_absent_duration > 10:
                cv2.putText(frame, "Please return to your position!", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 2)
            elif absence_count >= 3 and current_absent_duration > 15:
                timer = int(current_absent_duration - 15)
                cv2.putText(frame, "FINAL WARNING!!", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                cv2.putText(frame, f"Absence Timer: {timer}s", (10, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        # Display label
        
        color = (255, 255, 255)
        if activity == "Sleeping":
            color = (0, 0, 255)
        elif activity == "Using Phone":
            color = (255, 0, 255)
        elif activity == "Head Down":
            color = (0, 165, 255)

        cv2.putText(frame, activity, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        # ✅ Show sleep counter on screen (debug)
        if activity == "Sleeping":
            cv2.putText(frame, f"Sleep Counter: {sleeping_detection_counter}/90", 
                        (10, frame.shape[0] - 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.putText(frame, "Press 'b' to return", (10, frame.shape[0] - 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)

        cv2.imshow("Activity Recognition", frame)


        if cv2.waitKey(1) & 0xFF == ord('b'):
            now = datetime.now().strftime("%Y-%m-%d")
            if standing_time > 0: activity_data.loc[len(activity_data)] = [now, "Standing", standing_time]
            if sitting_time > 0: activity_data.loc[len(activity_data)] = [now, "Sitting", sitting_time]
            if head_down_time > 0: activity_data.loc[len(activity_data)] = [now, "Head Down", head_down_time]
            if hands_up_time > 0: activity_data.loc[len(activity_data)] = [now, "Hands Up", hands_up_time]
            if sleeping_time > 0: activity_data.loc[len(activity_data)] = [now, "Sleeping", sleeping_time]
            if using_phone_time > 0: activity_data.loc[len(activity_data)] = [now, "Using Phone", using_phone_time]
            if absent_time > 0: activity_data.loc[len(activity_data)] = [now, "Absent", absent_time]
            return_to_menu()
            break

    video.release()
    cv2.destroyAllWindows()
