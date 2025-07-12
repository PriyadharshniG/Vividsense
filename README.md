# 🌟 Vivid Sense

**Vivid Sense** is a multi-modal interactive desktop application that brings gesture control, voice interaction, virtual mouse capabilities, and a drawing app into one unified launcher. It uses computer vision and AI to provide a smarter, more intuitive user experience.

---

## 🧠 Features

- 🖐 **Gesture Recognition Mode**  
  Control the interface using your hand gestures via webcam.

- 🖱 **Virtual Mouse Mode**  
  Move your cursor and click using hand motions — no physical mouse required!

- 🎨 **Drawing App Mode**  
  A fun and interactive canvas to draw using gesture inputs.

- 🎙 **Voice Assistant Mode**  
  Execute commands and get responses using voice input.

---

## 🖥️ Tech Stack

- **Python**
- **OpenCV**
- **Tkinter** (for GUI)
- **SpeechRecognition** (for voice commands)
- **Custom ML Models** (for gesture recognition)
- **Threading** (for smooth multitasking in GUI)

---

##  Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/PriyadharshniG/Vividsense.git
cd Vividsense
2. Set Up Virtual Environment (Optional but Recommended)
bash
Copy
Edit
python -m venv venv
venv\Scripts\activate    # On Windows
3. Install Requirements
bash
Copy
Edit
pip install -r requirements.txt
If requirements.txt doesn't exist yet, create one using:

bash
Copy
Edit
pip freeze > requirements.txt
🎯 Running the App
bash
Copy
Edit
python run.py
A GUI window will open, allowing you to select between different modes: Gesture, Virtual Mouse, Drawing, and Voice Assistant.

📁 Project Structure
bash
Copy
Edit
Vividsense/
│
├── run.py                     # Main GUI launcher
├── requirements.txt           # Python dependencies
├── .gitignore                 # Ignored files
├── bg.png                     # Background image (optional)
├── icon.ico                   # App icon (optional)
├── src/                       # All core functionality
│   ├── gesture_draw.py
│   ├── virtual_mouse.py
│   ├── gesture_recognition.py
│   └── voice_assistant.py
🙋‍♀️ Developed By
Priyadharshni G
Aspiring Full Stack Developer | Passionate about AI & Human-Computer Interaction

📢 Contributing
Pull requests are welcome! Feel free to fork the repo and submit improvements or new features.


