# src/utils.py
# Add any utility functions you want, for example:
def set_color_for_drawing(finger_count):
    if finger_count == 1:
        return (0, 255, 0)  # Green for 1 finger
    elif finger_count == 2:
        return (255, 0, 0)  # Red for 2 fingers
    else:
        return (0, 0, 255)  # Blue for more than 2 fingers
