import tkinter as tk
from recognition_mode import start_motion_activity_system
from dashboard import activity_analytics_dashboard
from attendance import start_attendance_system
from total_people import start_total_people_counter

def main_menu():
    menu_window = tk.Tk()
    menu_window.title("Recognition Mode")
    menu_window.state('zoomed')
    menu_window.configure(bg="#0a192f")

    ACCENT = "#64ffda"
    DARK_BG = "#0a192f"
    BTN_FONT = ("Helvetica", 15, "bold")

    container = tk.Frame(menu_window, bg=DARK_BG)
    container.pack(fill="both", expand=True)

    left_panel = tk.Frame(container, bg=DARK_BG)
    left_panel.pack(side="left", fill="both", expand=True)

    tk.Label(left_panel, text="AHA SYSTEM", font=("Arial", 30, "bold"), fg="white", bg=DARK_BG).pack(pady=(100, 10))
    tk.Label(left_panel, text="Human Recognition System", font=("Arial", 14), fg=ACCENT, bg=DARK_BG).pack()
    tk.Frame(left_panel, width=80, height=3, bg=ACCENT).pack(pady=10)

    # Summary About the Page
    summary_text = (
        "This dashboard allows you to:\n"
        "- Recognize employee activities in real-time\n"
        "- Count total people present\n"
        "- Track attendance with face recognition\n"
        "- View detailed analytics and activity logs\n\n"
        "Use the buttons on the right to access each feature."
    )
    tk.Label(left_panel, text=summary_text, font=("Arial", 12), fg="white", bg=DARK_BG, justify="left", wraplength=350).pack(pady=(10, 20))


    right_panel = tk.Frame(container, bg="#E7C7C7")
    right_panel.pack(side="right", fill="both", expand=True)

    tk.Label(right_panel, text="Welcome to Employee Tracker Page", font=("Helvetica", 26, "bold"), fg=DARK_BG, bg="white").pack(pady=(40, 20))

    def create_button(text, command):
        btn = tk.Button(right_panel, text=text, font=BTN_FONT, bg=ACCENT, fg=DARK_BG,
                        width=30, height=2, bd=0, activebackground="#52e0c4", command=command)
        btn.bind("<Enter>", lambda e: btn.config(bg="#52e0c4"))
        btn.bind("<Leave>", lambda e: btn.config(bg=ACCENT))
        return btn

    create_button("Start Activity Recognition", lambda: [menu_window.destroy(), start_motion_activity_system("Activity")]).pack(pady=10)
    create_button("Start Total People Counter", lambda: [menu_window.destroy(), start_total_people_counter()]).pack(pady=10)
    create_button("Start Attendance System", lambda: [menu_window.destroy(), start_attendance_system()]).pack(pady=10)
    create_button("Open Analytics Dashboard", lambda: [menu_window.destroy(), activity_analytics_dashboard()]).pack(pady=10)

    # Back to Login Page Button
    def go_back_to_login():
        menu_window.destroy()
        from login_page import login_window  # Dynamic import to avoid circular error
        login_window()

    create_button("Back to Login Page", go_back_to_login).pack(pady=20)

    create_button("Exit", menu_window.destroy).pack(pady=10)

    menu_window.mainloop()
