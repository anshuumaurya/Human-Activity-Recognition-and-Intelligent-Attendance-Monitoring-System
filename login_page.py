import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import os
from main_menu import main_menu

def login_window():
    window = tk.Tk()
    window.title("AHA System - Admin Login")
    window.state('zoomed')

    primary_color = "#1A365D"
    secondary_color = "#FFF5EE"
    accent_color = "#0EA5E9"
    text_color = "#334155"
    subtle_color = "#E2E8F0"

    window.configure(bg=primary_color)

    container = tk.Frame(window, bg=primary_color)
    container.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.85, relheight=0.85)

    left_panel = tk.Frame(container, bg=primary_color)
    left_panel.place(relx=0, rely=0, relwidth=0.4, relheight=1)

    right_panel = tk.Frame(container, bg=secondary_color)
    right_panel.place(relx=0.4, rely=0, relwidth=0.5, relheight=1)

    separator = tk.Frame(container, width=4, bg="#0D2B4D")
    separator.place(relx=0.4, rely=0, relwidth=0.001, relheight=1)

    try:
        logo_path = "logo.png"
        if os.path.exists(logo_path):
            original_logo = Image.open(logo_path)
            size = min(original_logo.width, original_logo.height)
            mask = Image.new('L', (size, size), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, size, size), fill=255)

            logo_image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            offset_x = (size - original_logo.width) // 2
            offset_y = (size - original_logo.height) // 2
            logo_image.paste(original_logo, (offset_x, offset_y))
            logo_image.putalpha(mask)
            logo_image = logo_image.resize((180, 180), Image.Resampling.LANCZOS)
            logo_photo = ImageTk.PhotoImage(logo_image)

            logo_label = tk.Label(left_panel, image=logo_photo, bg=primary_color)
            logo_label.image = logo_photo
            logo_label.place(relx=0.5, rely=0.35, anchor=tk.CENTER)
        else:
            raise FileNotFoundError("Logo not found")
    except:
        logo_canvas = tk.Canvas(left_panel, width=180, height=180, bg=primary_color, highlightthickness=0)
        logo_canvas.place(relx=0.5, rely=0.35, anchor=tk.CENTER)
        logo_canvas.create_oval(10, 10, 170, 170, fill=accent_color, outline="")
        logo_canvas.create_text(90, 90, text="AHA", fill="white", font=("Arial", 44, "bold"))

    tk.Label(left_panel, text="AHA SYSTEM", font=("Arial", 32, "bold"), fg="white", bg=primary_color).place(relx=0.5, rely=0.56, anchor=tk.CENTER)
    tk.Label(left_panel, text="Human Recognition System", font=("Helvetica", 14), fg="#A3BFFA", bg=primary_color).place(relx=0.5, rely=0.62, anchor=tk.CENTER)
    tk.Frame(left_panel, width=80, height=3, bg=accent_color).place(relx=0.5, rely=0.68, anchor=tk.CENTER)
    tk.Label(left_panel, text="© 2025 AHA Systems • v4.2.1", font=("Arial", 8), fg="#6B7280", bg=primary_color).place(relx=0.5, rely=0.95, anchor=tk.CENTER)

    tk.Label(right_panel, text="Administrator Login", font=("Arial", 26, "bold"), fg=text_color, bg=secondary_color).place(relx=0.5, rely=0.10, anchor=tk.CENTER)
    tk.Label(right_panel, text="Please enter your credentials to access the dashboard", font=("Arial", 10), fg="#64748B", bg=secondary_color).place(relx=0.5, rely=0.15, anchor=tk.CENTER)

    form_frame = tk.Frame(right_panel, bg=secondary_color)
    form_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.7)

    tk.Label(form_frame, text="Username", font=("Arial", 11, "bold"), anchor="w", bg=secondary_color, fg=text_color).pack(fill="x", pady=(0, 5), padx=5)
    username_frame = tk.Frame(form_frame, highlightbackground=subtle_color, highlightcolor=accent_color, highlightthickness=1, bd=0)
    username_frame.pack(fill="x", pady=(0, 20))
    username_entry = tk.Entry(username_frame, font=("Helvetica", 12), bd=0, bg=secondary_color)
    username_entry.pack(fill="x", ipady=10, ipadx=10)

    tk.Label(form_frame, text="Password", font=("Arial", 11, "bold"), anchor="w", bg=secondary_color, fg=text_color).pack(fill="x", pady=(0, 5), padx=5)
    password_frame = tk.Frame(form_frame, highlightbackground=subtle_color, highlightcolor=accent_color, highlightthickness=1, bd=0)
    password_frame.pack(fill="x", pady=(0, 15))
    password_entry = tk.Entry(password_frame, font=("Helvetica", 12), bd=0, bg=secondary_color, show="•")
    password_entry.pack(fill="x", ipady=10, ipadx=10)

    remember_var = tk.IntVar()
    remember_frame = tk.Frame(form_frame, bg=secondary_color)
    remember_frame.pack(fill="x", pady=(0, 20))
    remember_check = tk.Checkbutton(remember_frame, text="Remember me", variable=remember_var, bg=secondary_color, fg=text_color, activebackground=secondary_color)
    remember_check.pack(side=tk.LEFT)

    def forgot_password_popup():
        popup = tk.Toplevel()
        popup.title("Reset Password")
        popup.geometry("350x200")
        popup.configure(bg="white")
        tk.Label(popup, text="Enter recovery email:", font=("Arial", 11), bg="white").pack(pady=10)
        email_entry = tk.Entry(popup, font=("Arial", 12), width=30)
        email_entry.pack(pady=5)

        def send_reset():
            email = email_entry.get()
            if "@" in email:
                messagebox.showinfo("Success", f"Reset link sent to {email}")
                popup.destroy()
            else:
                messagebox.showwarning("Invalid", "Please enter a valid email address")
        tk.Button(popup, text="Send Reset Link", command=send_reset, bg=accent_color, fg="white").pack(pady=15)

    forgot_password = tk.Label(remember_frame, text="Forgot password?", font=("Helvetica", 10), fg="#6B7280", bg=secondary_color)
    forgot_password.pack(side=tk.RIGHT)
    forgot_password.bind("<Enter>", lambda e: forgot_password.config(fg=accent_color, font=("Helvetica", 10, "underline"), cursor="hand2"))
    forgot_password.bind("<Leave>", lambda e: forgot_password.config(fg="#6B7280", font=("Helvetica", 10), cursor=""))
    forgot_password.bind("<Button-1>", lambda e: forgot_password_popup())

    def login():
        username = username_entry.get()
        password = password_entry.get()
        if username == "admin" and password == "password":
            if remember_var.get():
                with open("remember_me.txt", "w") as f:
                    f.write(username)
            else:
                if os.path.exists("remember_me.txt"):
                    os.remove("remember_me.txt")
            window.destroy()
            main_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
            password_entry.delete(0, tk.END)

    login_button = tk.Button(form_frame, text="Login", font=("Arial", 12, "bold"), bg=accent_color, fg="white", bd=0, command=login)
    login_button.pack(fill="x", ipady=10, pady=(10, 15))
    login_button.bind("<Enter>", lambda e: login_button.config(bg="#0284C7"))
    login_button.bind("<Leave>", lambda e: login_button.config(bg=accent_color))

    tk.Frame(form_frame, height=1, bg=subtle_color).pack(fill="x", pady=15)

    def go_back():
        window.destroy()
        from welcome_page import welcome_page
        welcome_page()

    back_button = tk.Button(form_frame, text="Return to Welcome Page", font=("Arial", 11), bg=accent_color, fg="white",bd=0, relief=tk.FLAT,command=go_back)
    back_button.pack(fill="x", ipady=8)
    back_button.bind("<Enter>", lambda e: back_button.config(bg="#0088CC"))
    back_button.bind("<Leave>", lambda e: back_button.config(bg=accent_color))

    # Proper footer using pack instead of place to avoid overflow
    footer = tk.Frame(right_panel, height=3, bg=accent_color)
    footer.pack(side="bottom", fill="x")


    username_entry.focus_set()

    # # Load remembered user
    # if os.path.exists("remember_me.txt"):
    #     with open("remember_me.txt", "r") as f:
    #         username_entry.insert(0, f.read().strip())
    #         remember_check.select()
