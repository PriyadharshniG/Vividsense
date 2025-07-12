import pyautogui

def control_app(command):
    if command == "cut":
        pyautogui.hotkey('ctrl', 'x')
    elif command == "copy":
        pyautogui.hotkey('ctrl', 'c')
    elif command == "paste":
        pyautogui.hotkey('ctrl', 'v')
    elif command == "maximize":
        pyautogui.hotkey('win', 'up')
    elif command == "minimize":
        pyautogui.hotkey('win', 'down')
