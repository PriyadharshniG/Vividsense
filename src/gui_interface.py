import tkinter as tk
from tkinter import messagebox
import subprocess
import os

def start_gesture_app():
    try:
        subprocess.Popen(["python", "src/gesture_recognition.py"])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to launch app:\n{e}")

app = tk.Tk()
app.title("GestureOS Launcher")
app.geometry("400x300")
app.configure(bg="#1f1f2e")

# Header
tk.Label(app, text="GestureOS", font=("Arial", 24, "bold"), fg="#00ffcc", bg="#1f1f2e").pack(pady=20)

# Description
tk.Label(app, text="Control your system with hand gestures!", font=("Arial", 12), fg="white", bg="#1f1f2e").pack(pady=10)

# Launch Button
tk.Button(app, text="Start Gesture Recognition", font=("Arial", 14), bg="#00ffcc", fg="black",
          command=start_gesture_app, padx=10, pady=5).pack(pady=20)

# Footer
tk.Label(app, text="Developed by Priyadharshni G", font=("Arial", 10), fg="gray", bg="#1f1f2e").pack(side="bottom", pady=10)

app.mainloop()
