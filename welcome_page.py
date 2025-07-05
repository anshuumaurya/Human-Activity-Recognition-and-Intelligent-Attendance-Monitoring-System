# welcome_page.py

import tkinter as tk
from PIL import Image, ImageTk
import os
from login_page import login_window  # Make sure login_page.py exists

def welcome_page():
        welcome_window = tk.Tk()
        welcome_window.title("Welcome Page")
        welcome_window.state('zoomed')
        
        # Set dark theme colors
        bg_color = "#050e2b"  # Dark blue background
        accent_color = "#ff1f5a"  # Pink accent color as in the image
        text_color = "#ffffff"  # White text
        
        welcome_window.configure(bg=bg_color)
        
        # Create a full-window frame
        main_frame = tk.Frame(welcome_window, bg=bg_color)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        # Header with navigation elements (simplified)
        header_frame = tk.Frame(main_frame, bg=bg_color, height=50)
        header_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Content area with left and right sections
        content_frame = tk.Frame(main_frame, bg=bg_color)
        content_frame.pack(expand=True, fill=tk.BOTH, padx=50, pady=50)
        
        # Left section for text
        left_frame = tk.Frame(content_frame, bg=bg_color, width=500)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Main title with two-color text effect
        title_frame = tk.Frame(left_frame, bg=bg_color)
        title_frame.pack(anchor=tk.W, pady=(50, 10))
        
        face_label = tk.Label(title_frame, text="HUMAN ", font=("Arial", 36, "bold"), 
                            fg=text_color, bg=bg_color)
        face_label.pack(side=tk.LEFT)
        
        recognition_label = tk.Label(title_frame, text="RECOGNITION", font=("Arial", 36, "bold"), 
                                fg=accent_color, bg=bg_color)
        recognition_label.pack(side=tk.LEFT)

        face_label = tk.Label(title_frame, text="SYSTEM ", font=("Arial", 36, "bold"), 
                            fg=text_color, bg=bg_color)
        face_label.pack(side=tk.LEFT)
        
        # Description text
        description = "Welcome to Human motion tracking and Activity Recognition system.This system can detect multiple human activities with real-time monitoring like sitting , standing , sleeping, head down,hands up etc..The system provides real-time detection, analytics, and reporting capabilities."
        
        description_label = tk.Label(left_frame, text=description, 
                                font=("Arial", 12), fg=text_color, bg=bg_color,
                                justify=tk.LEFT, wraplength=450)
        description_label.pack(anchor=tk.W, pady=20)
        
        # Start button with bright accent color
        start_button = tk.Button(left_frame, text="ADMIN LOGIN", 
                            font=("Arial", 12, "bold"),
                            bg=accent_color, fg=text_color, 
                            padx=30, pady=10,
                            bd=0, relief="flat", borderwidth=0,
                            command=lambda: [welcome_window.destroy(), login_window()])
        start_button.pack(anchor=tk.W, pady=20)
        
        # Artificial Intelligence text in background (partially transparent/faded)
        ai_label = tk.Label(left_frame, text="ACTIVITY\nRECOGNITION", 
                        font=("Arial", 40, "bold"), 
                        fg="#0a1a4a", bg=bg_color,  # Very dark blue, barely visible
                        justify=tk.LEFT)
        ai_label.place(x=0, y=350)
        
        # Right section for the face recognition graphic
        right_frame = tk.Frame(content_frame, bg=bg_color, width=500)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Load face mesh image if available, otherwise use a placeholder
        try:
            # Replace with your actual image path
            image_path = "face.png"  # You should provide the path to a wireframe face image
            
            # Check if file exists 
            if os.path.exists(image_path):
                face_image = Image.open(image_path)
                face_image = face_image.resize((400, 400), Image.LANCZOS)
                tk_image = ImageTk.PhotoImage(face_image)
                
                image_label = tk.Label(right_frame, image=tk_image, bg=bg_color)
                image_label.image = tk_image  # Keep a reference
                image_label.pack(expand=True)
            else:
                # Create a wireframe face placeholder using text
                placeholder = tk.Label(right_frame, 
                                    text="[Wireframe Face Graphic]", 
                                    font=("Arial", 20),
                                    fg="#00ffff", bg=bg_color,
                                    height=15)
                placeholder.pack(expand=True)
                
                # Draw some "network lines" to simulate the wireframe look
                for i in range(5):
                    line = tk.Frame(right_frame, bg="#00ffff", height=1, width=100)
                    line.place(x=100 + i*20, y=150 + i*30)
        
        except Exception as e:
            print(f"Error loading image: {e}")
            # Placeholder in case of error
            placeholder = tk.Label(right_frame, 
                                text="[Wireframe Face Graphic]", 
                                font=("Arial", 20),
                                fg="#00ffff", bg=bg_color,
                                height=15)
            placeholder.pack(expand=True)
        
        # Add some circuit-like lines in the background for the tech feel
        # This is a simplified version - for a real app, you'd use Canvas to draw proper lines
        for i in range(10):
            h_line = tk.Frame(main_frame, bg="#103060", height=1, width=50)
            h_line.place(x=10 + i*80, y=20 + i*40)
            
            v_line = tk.Frame(main_frame, bg="#103060", height=50, width=1)
            v_line.place(x=30 + i*70, y=10 + i*60)
        
        welcome_window.mainloop()
    
