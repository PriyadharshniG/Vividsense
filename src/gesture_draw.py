import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import threading

# Initialize mediapipe hand module
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# Global variables
canvas = None
save_triggered = False

# Tkinter App
def start_drawing_app():
    global canvas, save_triggered
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        messagebox.showerror("Error", "Cannot open camera")
        return

    prev_x, prev_y = 0, 0
    drawing = False
    line_color = (0, 255, 0)  # Default color (Green)
    line_thickness = 5
    history = []  # To store drawing history for undo
    eraser_mode = False

    def save_drawing():
        global canvas
        # Save the canvas to a file
        file_name = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_name:
            cv2.imwrite(file_name, canvas)
            messagebox.showinfo("Save", "Drawing saved successfully!")

    def undo_drawing():
        global canvas
        # Undo the last stroke
        if history:
            canvas[:] = history.pop()
            cv2.putText(canvas, 'Undo Complete!', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        if canvas is None:
            canvas = np.zeros_like(frame)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw landmarks on hand
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Get fingertip (index finger tip) coordinates
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                x, y = int(index_tip.x * w), int(index_tip.y * h)

                # Eraser mode
                if eraser_mode:
                    cv2.circle(canvas, (x, y), 20, (0, 0, 0), -1)  # Draw black circle (erase)
                elif drawing:
                    cv2.line(canvas, (prev_x, prev_y), (x, y), line_color, line_thickness)

                prev_x, prev_y = x, y

                # Check for gestures
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                thumb_x, thumb_y = int(thumb_tip.x * w), int(thumb_tip.y * h)
                distance = np.hypot(x - thumb_x, y - thumb_y)

                # Toggle drawing/eraser mode
                if distance < 40:
                    drawing = not drawing
                    if drawing:
                        cv2.putText(frame, 'Drawing Mode', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    else:
                        cv2.putText(frame, 'Eraser Mode', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                # Change color: fist = Red, peace = Blue
                if distance < 40:
                    # Fist (for Red)
                    fist_gesture = check_fist_gesture(hand_landmarks)
                    if fist_gesture:
                        line_color = (0, 0, 255)  # Red
                        cv2.putText(frame, 'Color: Red', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

                    # Peace (for Blue)
                    peace_gesture = check_peace_gesture(hand_landmarks)
                    if peace_gesture:
                        line_color = (255, 0, 0)  # Blue
                        cv2.putText(frame, 'Color: Blue', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

                # Undo Gesture (index and thumb together)
                if distance < 40:
                    undo_drawing()

                # Hi-Five gesture for saving drawing
                if check_highfive_gesture(hand_landmarks) and not save_triggered:
                    file_name = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
                    if file_name:
                        cv2.imwrite(file_name, canvas)
                        save_triggered = True
                        cv2.putText(frame, 'Saved!', (10, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                else:
                    save_triggered = False  # Reset to allow another save later

        # Combine canvas and frame
        blended = cv2.addWeighted(frame, 0.5, canvas, 0.5, 0)
        cv2.imshow("Virtual Drawing - Press 'q' to Quit", blended)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def check_fist_gesture(hand_landmarks):
    # Check if all fingers are folded (fist gesture)
    thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

    if index.y < thumb.y and middle.y < thumb.y and ring.y < thumb.y and pinky.y < thumb.y:
        return True
    return False

def check_peace_gesture(hand_landmarks):
    # Check if index and middle fingers are extended (peace gesture)
    index = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    if index.y < middle.y:
        return True
    return False

def check_highfive_gesture(hand_landmarks):
    # Check if all fingers are spread (Hi-Five gesture)
    tips = [
        mp_hands.HandLandmark.THUMB_TIP,
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP
    ]
    bases = [
        mp_hands.HandLandmark.THUMB_IP,
        mp_hands.HandLandmark.INDEX_FINGER_MCP,
        mp_hands.HandLandmark.MIDDLE_FINGER_MCP,
        mp_hands.HandLandmark.RING_FINGER_MCP,
        mp_hands.HandLandmark.PINKY_MCP
    ]
    
    for tip, base in zip(tips, bases):
        if hand_landmarks.landmark[tip].y > hand_landmarks.landmark[base].y:
            return False
    return True

# Tkinter GUI
def launch_drawing_app():
    # Launch the drawing app in a separate thread to prevent blocking the Tkinter UI
    drawing_thread = threading.Thread(target=start_drawing_app)
    drawing_thread.start()

def save_drawing():
    global canvas
    file_name = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if file_name:
        cv2.imwrite(file_name, canvas)
        messagebox.showinfo("Save", "Drawing saved successfully!")

# Tkinter Setup
root = tk.Tk()
root.title("Virtual Drawing App")
root.geometry("400x200")

btn = tk.Button(root, text="Launch Drawing App", command=launch_drawing_app, font=("Arial", 14), bg="lightblue")
btn.pack(pady=20)

save_btn = tk.Button(root, text="Save Drawing", command=save_drawing, font=("Arial", 14), bg="lightgreen")
save_btn.pack(pady=20)

if __name__ == "__main__":
    root.mainloop()
