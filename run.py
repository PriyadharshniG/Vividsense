# run.py
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import sys
import threading

# Import your module functions
from src.gesture_draw import start_drawing_app
from src.virtual_mouse import start_virtual_mouse
from src.gesture_recognition import start_gesture_mode
from src.voice_assistant import activate_voice_assistant

# Globals
current_task_window = None
current_thread = None

def stop_background_tasks():
    print("Stopping background tasks...")

# Stops the current opened task window
def stop_current_task():
    global current_task_window
    if current_task_window and current_task_window.winfo_exists():
        current_task_window.destroy()
        print("Closed current module window.")

# Safe threaded launcher function
def run_in_thread(func, title):
    global current_task_window, current_thread
    stop_current_task()
    
    current_task_window = tk.Toplevel(app)
    current_task_window.title(title)
    current_task_window.geometry("700x600")

    def task_wrapper():
        try:
            func()
        except Exception as e:
            print(f"{title} Error: {e}")
            messagebox.showerror("Error", f"Failed to start {title}:\n{e}")

    current_thread = threading.Thread(target=task_wrapper, daemon=True)
    current_thread.start()

# Mode Launchers
def launch_gesture_mode():
    run_in_thread(start_gesture_mode, "Gesture Mode")

def launch_virtual_mouse():
    run_in_thread(start_virtual_mouse, "Virtual Mouse Mode")

def launch_drawing_app():
    run_in_thread(start_drawing_app, "Drawing App Mode")

def launch_voice_assistant():
    run_in_thread(activate_voice_assistant, "Voice Assistant Mode")

# Button hover effects
def on_enter(e): e.widget['background'], e.widget['fg'] = '#1f1f2e', '#00ffcc'
def on_leave(e): e.widget['background'], e.widget['fg'] = '#00ffcc', 'black'
def on_exit_hover(e): e.widget['background'] = '#cc0000'
def on_exit_leave(e): e.widget['background'] = 'red'

# Confirm and clean exit
def confirm_exit():
    if messagebox.askyesno("Exit", "Are you sure you want to exit the application?"):
        stop_current_task()
        stop_background_tasks()
        app.destroy()
        sys.exit()

# Main GUI window
app = tk.Tk()
app.title("Vivid Sense Launcher")
app.geometry("700x600")
app.configure(bg="#2b2b2b")
app.protocol("WM_DELETE_WINDOW", confirm_exit)

# Optional icon
try: app.iconbitmap("icon.ico")
except: pass

# Background image
try:
    from PIL import ImageTk, Image
    bg_image = Image.open("bg.png").resize((700, 600))
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(app, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except: pass

# Header
header_frame = tk.Frame(app, bg="#2b2b2b")
header_frame.pack(pady=30)
tk.Label(header_frame, text="Vivid Sense", font=("Helvetica Neue", 32, "bold"), fg="#00ffcc", bg="#2b2b2b").pack(pady=10)
tk.Label(header_frame, text="Choose a mode to begin", font=("Arial", 16), fg="white", bg="#2b2b2b").pack(pady=5)

# Button style and mode list
button_style = {
    "font": ("Arial", 14), "bg": "#00ffcc", "fg": "black", "padx": 15, "pady": 10,
    "width": 30, "bd": 0, "relief": "raised", "cursor": "hand2"
}
modes = [
    ("🖐 Gesture Recognition Mode", launch_gesture_mode),
    ("🖱 Virtual Mouse Mode", launch_virtual_mouse),
    ("🎨 Drawing App Mode", launch_drawing_app),
    ("🎙 Voice Assistant Mode", launch_voice_assistant)
]

# Mode buttons
button_frame = tk.Frame(app, bg="#2b2b2b")
button_frame.pack(pady=20)

for text, command in modes:
    btn = tk.Button(button_frame, text=text, command=command, **button_style)
    btn.pack(pady=12)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

# Exit button
exit_btn = tk.Button(app, text="Exit Application", command=confirm_exit, font=("Arial", 16), bg="red", fg="white", padx=15, pady=10, width=30)
exit_btn.pack(pady=20)
exit_btn.bind("<Enter>", on_exit_hover)
exit_btn.bind("<Leave>", on_exit_leave)

# Footer
footer_frame = tk.Frame(app, bg="#2b2b2b")
footer_frame.pack(side="bottom", pady=15)
tk.Label(footer_frame, text="Developed by Priyadharshni G", font=("Arial", 12), fg="gray", bg="#2b2b2b").pack()

# Start the app
app.mainloop()