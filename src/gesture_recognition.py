import cv2
from cvzone.HandTrackingModule import HandDetector
import winsound  # Built-in module for alarm sound on Windows

def play_alarm():
    # Beep at 1000 Hz for 1 second
    winsound.Beep(1000, 1000)

def start_gesture_mode():
    cap = cv2.VideoCapture(0)  # Start webcam
    detector = HandDetector(maxHands=1)  # Detect 1 hand at a time

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)  # Flip image horizontally
        hands, img = detector.findHands(img)  # Detect hands

        if hands:
            hand = hands[0]
            fingers = detector.fingersUp(hand)
            gesture = ""

            if fingers == [0, 1, 0, 0, 0]:
                gesture = "Index Finger"
            elif fingers == [1, 1, 0, 0, 0]:
                gesture = "Peace"
            elif fingers == [0, 0, 0, 0, 0]:
                gesture = "Fist - DANGER Detected!"
                play_alarm()
            elif fingers == [1, 1, 1, 1, 1]:
                gesture = "Open Palm"
            elif fingers == [1, 0, 0, 0, 1]:
                gesture = "Rock Sign - SOS"
                play_alarm()

            # Display the gesture text
            cv2.putText(img, gesture, (20, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1.5, (0, 0, 255) if "DANGER" in gesture else (255, 0, 255), 3)

        cv2.imshow("🖐️ Gesture Recognition for Safety", img)

        # Quit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Run the program
if __name__ == "__main__":
    start_gesture_mode()
