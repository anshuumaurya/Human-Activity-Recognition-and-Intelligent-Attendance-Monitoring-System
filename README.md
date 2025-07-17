# Human-Activity-Recognition-and-Intelligent-Attendance-Monitoring-System
A full-featured Python-based intelligent surveillance system that combines face recognition, human activity detection, attendance logging, and analytics visualization — all in one place.
This project is ideal for employee or student tracking, performance monitoring, and secure workplace access.

# Technologies Used
| Technology          | Use Case                                 |
| ------------------- | ---------------------------------------- |
| Python              | Core programming language                |
| OpenCV              | Video feed, face capture, people counter |
| Face Recognition    | Identify authorized persons              |
| MediaPipe           | Detect body pose and activity            |
| Tkinter             | User interface (GUI)                     |
| Pandas, NumPy       | Data handling and analysis               |
| Matplotlib, Seaborn | Data visualization                       |
| FPDF                | Export reports to PDF                    |
| Scikit-learn        | Confusion matrix, accuracy metrics       |


# System Modules 
# 1. Admin Login Interface
File: login_page.py
Simple login page (admin / password)
“Remember me” functionality (saves user locally)
“Forgot Password” popup UI
Loads the Main Menu on success

# 2. Main Menu Navigation
File: main_menu.py
Provides access to all major functionalities:
Activity Recognition System
Face Recognition Attendance
Total People Counter
Analytics Dashboard
Back to Login
Exit

# 3. Face Recognition-Based Attendance
File: attendance.py
# Purpose: Detect and log known persons; flag unknowns.
# How it works:
Loads known faces from the images/ folder
Captures faces in real time from webcam
Compares them to known encodings
# If Match (Authorized):
Draws green box
Shows name and “Authorized”
Saves name + timestamp in Attendance.csv
Logs activity in activity_data.csv
# If No Match (Unauthorized):
Draws red box
Shows “Unauthorized Intrusion!”
Captures face as image: unauthorized_YYYYMMDD_HHMMSS.jpg
Saves log in Unauthorized_Log.csv
# 4.Activity Recognition System
File: recognition_mode.py
# Purpose: Monitor posture, activity, and detect presence in real-time.
Detectable Activities:
| Activity        | Detection Logic                     |
| --------------- | ----------------------------------- |
| **Standing**    | Shoulders far above hips, knees low |
| **Sitting**     | Knees above hip level               |
| **Head Down**   | Nose lower than average ear level   |
| **Hands Up**    | Wrists above shoulders              |
| **Using Phone** | Wrists near face (≤30 cm)           |
| **Sleeping**    | Eyes closed (EAR check) + no motion |
| **Absent**      | No person detected in frame         |

# 3-Level Alert System (for Absence)
| Time Passed | Alert Displayed                      |
| ----------- | ------------------------------------ |
| ⏱️ 5 sec    | ⚠️ "Absence detected!"               |
| ⏱️ 10 sec   | ⚠️ "Please return to your position!" |
| ⏱️ 15 sec+  | 🔴 "FINAL WARNING!!" + timer shown   |


This ensures:
Gentle warning first
Stronger alert if user still missing
Timer tracks how long they’re away

# AI-Driven Behavior Logging
Every 10 seconds:
Logs total time spent per activity in activity_data.csv
Used later for charts, trends, reports

# 5. Total People Counter
File: total_people.py
Purpose: Count number of faces seen on camera using HaarCascade.
Displays:

Date & time
Total face count
Press 'b' to return to main menu

# 6. Analytics Dashboard
File: dashboard.py
Purpose: Visualize, analyze, and report performance.

Tabs:
Activity Analytics
Attendance Records
Reports

🔍 Dashboard Capabilities:
| Feature                       | Description                                   |
| ----------------------------- | --------------------------------------------- |
| Filter Data                   | Last 7 days, This Month, All Time             |
| Add Sample Data (for testing) | Add fake activity or attendance manually      |
| Pie Chart                     | Activity distribution visualization           |
| Weekly Summary                | Total time/activity breakdown                 |
| Confusion Matrix              | Accuracy comparison between real vs predicted |
| Accuracy Over Time            | Training/validation accuracy simulated        |
| Export to PDF                 | Saves report from dashboard                   |


# 7. Reports You Can Generate
Activity Summary Report
Attendance Summary
Performance Analytics
Detailed CSV Export (attendance + activity)

Reports show:
Most common activity
Total duration breakdown
Top attendees
Security alert level
Unauthorized entry rate

# Data Files (Generated Automatically)
File Name	Purpose
| File Name              | Purpose                              |
| ---------------------- | ------------------------------------ |
| `Attendance.csv`       | Authorized entries with time logs    |
| `Unauthorized_Log.csv` | Timestamp and image of unknown faces |
| `activity_data.csv`    | Duration per activity, per day       |

# App Flow Summary
1. Run the app → `python run.py`
2. Login as admin → `login_page.py`
3. Choose from main menu:
    ├── Activity Detection
    ├── Attendance Logging
    ├── Total People Counter
    ├── Dashboard & Reports


