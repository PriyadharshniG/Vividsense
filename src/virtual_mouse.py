import cv2
import numpy as np
import pyautogui
from cvzone.HandTrackingModule import HandDetector
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import time
import pyttsx3

def start_virtual_mouse():
    # Initialize Camera
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    # Initialize Hand Detector
    detector = HandDetector(detectionCon=0.8, maxHands=1)

    # Screen Size
    screen_width, screen_height = pyautogui.size()

    # Cursor Smoothening
    smoothening = 7
    plocX, plocY = 0, 0
    clocX, clocY = 0, 0

    # Volume Control Setup
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume_ctrl = cast(interface, POINTER(IAudioEndpointVolume))
    vol_range = volume_ctrl.GetVolumeRange()
    minVol, maxVol = vol_range[0], vol_range[1]

    # Text-to-Speech Engine
    engine = pyttsx3.init()
    def speak(text):
        engine.say(text)
        engine.runAndWait()

    # Dragging state
    dragging = False

    # Scroll timer
    last_scroll_time = time.time()
    scroll_delay = 0.5  # in seconds

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img, draw=True)

        if hands:
            hand = hands[0]
            lmList = hand["lmList"]
            fingers = detector.fingersUp(hand)

            x1, y1 = lmList[8][0], lmList[8][1]   # Index
            x2, y2 = lmList[12][0], lmList[12][1] # Middle

            x3 = np.interp(x1, (100, 1180), (0, screen_width))
            y3 = np.interp(y1, (100, 620), (0, screen_height))
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            # Move Cursor (Only Index)
            if fingers == [0,1,0,0,0]:
                pyautogui.moveTo(screen_width - clocX, clocY)
                cv2.circle(img, (x1, y1), 10, (0, 255, 0), cv2.FILLED)

            # Left Click (Thumb + Index)
            if fingers == [1,1,0,0,0]:
                pyautogui.click()
                speak("Click")
                time.sleep(0.3)

            # Right Click (Index + Pinky)
            if fingers == [0,1,0,0,1]:
                pyautogui.click(button='right')
                speak("Right Click")
                time.sleep(0.3)

            # Drag (Index + Middle)
            if fingers == [0,1,1,0,0]:
                if not dragging:
                    pyautogui.mouseDown()
                    dragging = True 
                    cv2.putText(img, "Dragging", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)
            else:
                if dragging:
                    pyautogui.mouseUp()
                    dragging = False

            # Scroll Up (Index + Middle + Ring)
            if fingers == [0,1,1,1,0] and time.time() - last_scroll_time > scroll_delay:
                pyautogui.scroll(300)
                cv2.putText(img, "Scrolling Up", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 3)
                last_scroll_time = time.time()

            # Scroll Down (Middle + Ring + Pinky)
            if fingers == [0,0,1,1,1] and time.time() - last_scroll_time > scroll_delay:
                pyautogui.scroll(-300)
                cv2.putText(img, "Scrolling Down", (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 3)
                last_scroll_time = time.time()

            # Volume Control (Thumb + Index)
            if fingers == [1,1,0,0,0]:
                length, _, _ = detector.findDistance(lmList[4], lmList[8], img)
                vol = np.interp(length, [20, 200], [minVol, maxVol])
                volume_ctrl.SetMasterVolumeLevel(vol, None)
                cv2.putText(img, f'Volume: {int(np.interp(vol, [minVol, maxVol], [0,100]))}%', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 3)

            # Brightness Control (Thumb + Pinky)
            if fingers == [1,0,0,0,1]:
                length, _, _ = detector.findDistance(lmList[4], lmList[20], img)
                brightness = np.interp(length, [20, 200], [0, 100])
                cv2.putText(img, f'Brightness: {int(brightness)}%', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 3)

            # Screenshot (All Fingers)
            if sum(fingers) == 5:
                filename = f"screenshot_{int(time.time())}.png"
                pyautogui.screenshot(filename)
                speak("Screenshot Taken")
                cv2.putText(img, "Screenshot!", (500, 400), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,255), 4)
                time.sleep(0.5)

            # Minimize (Index + Middle + Ring)
            if fingers == [0,1,1,1,0]:
                pyautogui.hotkey('win', 'down')
                speak("Window Minimized")
                cv2.putText(img, "Window Minimized", (50, 350), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)
                time.sleep(0.3)

            # Maximize (Thumb + Index + Pinky)
            if fingers == [1,1,0,0,1]:
                pyautogui.hotkey('win', 'up')
                speak("Window Maximized")
                cv2.putText(img, "Window Maximized", (50, 350), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)
                time.sleep(0.3)

            # Close (Thumb + Ring + Pinky)
            if fingers == [1,0,0,1,1]:
                pyautogui.hotkey('alt', 'f4')
                speak("Window Closed")
                cv2.putText(img, "Window Closed", (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                time.sleep(0.3)

        cv2.imshow("Virtual Mouse", img)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Run the function
if __name__ == "__main__":
    start_virtual_mouse()
