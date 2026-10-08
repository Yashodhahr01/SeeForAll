# 👁️ SeeForAll – Multilingual AI Vision Assistant

> An AI-powered assistive vision system that helps visually impaired users understand their surroundings through real-time object detection, spatial awareness, distance estimation, and multilingual voice feedback.

---

## 🌟 Overview

**SeeForAll** is an AI-based assistive technology project designed to help visually impaired individuals better understand their surroundings.

The system uses a webcam to capture the environment and applies **YOLO-World** for real-time, open-vocabulary object detection.

Detected objects are analyzed to determine:

- 🔍 What the object is
- 📍 Where the object is located
- 📏 Approximate distance from the camera
- 🗣️ How to describe the object in the selected language

The information is then converted into speech using **Google Text-to-Speech (gTTS)**.

---

## 🎯 Problem Statement

Visually impaired individuals often face difficulties identifying objects, understanding their surroundings, and navigating unfamiliar environments.

Existing assistive solutions can be expensive, hardware-dependent, or limited in the number of objects and languages they support.

### The problem

> How can we develop an affordable AI-based system that can identify objects around a visually impaired person and communicate useful environmental information through voice?

---

## 💡 Proposed Solution

SeeForAll combines computer vision, spatial analysis, multilingual translation, and text-to-speech technology into a single assistive system.

### Working Flow

```text
                📷 Webcam
                    │
                    ▼
          ┌───────────────────┐
          │    YOLO-World     │
          │ Object Detection  │
          └─────────┬─────────┘
                    │
                    ▼
          ┌───────────────────┐
          │ Object Recognition│
          └─────────┬─────────┘
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
   📍 Position           📏 Distance
 Left / Right /        Near / Far /
     Ahead             Very Close
          │                   │
          └─────────┬─────────┘
                    ▼
          🌐 Language Module
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
      Hindi      Kannada      Tamil
        │           │           │
        └───────────┼───────────┘
                    ▼
             🔊 Text-to-Speech
                    │
                    ▼
             👤 User Feedback

✨ Key Features
🤖 1. Real-Time Object Detection

SeeForAll uses YOLO-World for real-time object detection.

The project uses a custom vocabulary containing objects such as:

Person
Car
Bicycle
Motorcycle
Bus
Truck
Laptop
Smartphone
Bottle
Chair
Table
Book
Bag
Animals
Food
Household objects
Medical objects
Traffic objects

and many more.

📍 2. Object Position Detection

The camera frame is divided into three regions:

┌──────────────────────────────────────┐
│                                      │
│    LEFT        AHEAD        RIGHT    │
│                                      │
└──────────────────────────────────────┘

The system identifies whether an object is:

Left
Ahead
Right
Example
Person on your left
Bottle ahead
Car on your right
📏 3. Approximate Distance Estimation

The system estimates the approximate distance using the size of the detected object's bounding box.

It classifies objects into:

Very Close
     ↓
Near
     ↓
Far
Example
Person ahead, very close.

Bottle on your left, near.

Car on your right, far.

Note: The current distance estimation is approximate and is not a replacement for a physical distance sensor.

🌐 4. Multilingual Support

SeeForAll supports five languages.

Language	Code
🇬🇧 English	en
🇮🇳 Hindi	hi
🇮🇳 Kannada	kn
🇮🇳 Tamil	ta
🇮🇳 Telugu	te

When the program starts, the user can select a language:

Choose your language:

1. English
2. Hindi
3. Kannada
4. Tamil
5. Telugu
🔊 5. Voice Feedback

The detected information is converted into speech using Google Text-to-Speech (gTTS).

English
Person ahead, near.
Bottle on your left, very close.
Hindi
व्यक्ति सामने, पास।
बोतल आपकी बाईं ओर, बहुत पास।
Kannada
ವ್ಯಕ್ತಿ ಮುಂದೆ, ಹತ್ತಿರ.
ಬಾಟಲಿ ನಿಮ್ಮ ಎಡಭಾಗದಲ್ಲಿ, ತುಂಬಾ ಹತ್ತಿರ.
Tamil
நபர் முன்னால், அருகில்.
பாட்டில் உங்கள் இடப்புறத்தில், மிகவும் அருகில்.
Telugu
వ్యక్తి ముందు, దగ్గరగా.
బాటిల్ మీ ఎడమ వైపున, చాలా దగ్గరగా.
🧠 Technology Stack
Technology	Purpose
Python	Core development
YOLO-World	Open-vocabulary object detection
Ultralytics	YOLO implementation
OpenCV	Webcam and image processing
PyTorch	Deep learning framework
gTTS	Text-to-speech
Pygame	Audio playback
Git	Version control
GitHub	Project hosting
VS Code	Development environment
🏗️ System Architecture
                CAMERA
                   │
                   ▼
             Video Frame
                   │
                   ▼
             YOLO-WORLD
                   │
                   ▼
           Object Detection
                   │
          ┌────────┴────────┐
          │                 │
          ▼                 ▼
      Position          Distance
          │                 │
          └────────┬────────┘
                   │
                   ▼
            Object Translation
                   │
                   ▼
          Language Selection
                   │
                   ▼
                  gTTS
                   │
                   ▼
             Audio Output
                   │
                   ▼
                USER
📂 Project Structure
SeeForAll/
│
├── see_for_all.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── weights/
│
└── yolov8s-worldv2.pt
Important

The Python virtual environment should remain local:

venv/

It should not be uploaded to GitHub.

Temporary audio files such as:

*.mp3

should also not be uploaded.

⚙️ Installation
1. Clone the Repository
git clone https://github.com/Yashodhahr01/SeeForAll.git

Go to the project folder:

cd SeeForAll
2. Create a Virtual Environment

For Windows:

python -m venv venv

Activate it:

venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt

If Pygame is not installed:

pip install pygame
4. Run the Application
python see_for_all.py
▶️ How to Use

After starting the application, the language selection menu appears:

========================================
             SEE FOR ALL
========================================

Choose your language:

1. English
2. Hindi
3. Kannada
4. Tamil
5. Telugu

Enter your choice (1-5):

Select the required language.

The webcam will then start.

The system will:

Capture the webcam frame.
Detect objects using YOLO-World.
Draw bounding boxes.
Determine the object's position.
Estimate approximate distance.
Translate the object information.
Generate speech.
Play the audio feedback.
🛑 Exit the Application

To stop the application:

Q

or

ESC
💻 Hardware Requirements

The current prototype can run using a normal laptop.

Required
💻 Laptop/Desktop
📷 Webcam
🔊 Speaker or headphones
🌐 Internet connection for gTTS
Current Prototype

No special hardware is required.

The laptop webcam is used for the demonstration.

📊 Current Capabilities

The current prototype supports:

✅ Real-time webcam input
✅ YOLO-World object detection
✅ Custom object vocabulary
✅ Position detection
✅ Approximate distance estimation
✅ English voice output
✅ Hindi voice output
✅ Kannada voice output
✅ Tamil voice output
✅ Telugu voice output
✅ Speech queue
✅ Q / ESC exit
⚠️ Limitations

The current prototype has some limitations:

Distance estimation is approximate.
Detection performance depends on lighting and camera quality.
YOLO-World may not recognize every possible object.
gTTS requires an internet connection.
The current system uses a laptop webcam.
The prototype is not a certified medical or mobility-assistance device.
🚀 Future Enhancements
🧭 Navigation Assistance

Future versions can include:

GPS navigation
Indoor navigation
Obstacle avoidance
Path detection
Turn-by-turn directions
Crosswalk detection
📖 OCR and Text Reading

The system can be extended with OCR to read:

Books
Signs
Documents
Product labels
Menus
Medicine labels
💰 Currency Recognition

Future versions can identify Indian currency notes and provide voice feedback.

🗣️ Voice Commands

Users could interact with the system using commands such as:

"Describe my surroundings"

"What is in front of me?"

"Read this text"

"Find a chair"

"What is on my left?"
📴 Offline AI

A future version can replace online services with offline AI models for:

Speech recognition
Translation
Text-to-speech
Object detection

This would allow the system to work without an internet connection.

📱 Mobile / Wearable Version

The final system could be integrated into:

Smart glasses
Smart hat
Wearable camera
Smartphone application
Assistive pendant
🔬 Project Scope

The long-term vision of SeeForAll is to combine:

Computer Vision
       +
Object Detection
       +
Spatial Awareness
       +
Distance Estimation
       +
OCR
       +
Multilingual AI
       +
Voice Interaction
       +
Navigation
       ↓
AI-Powered Assistive Vision System
🎓 Academic Project
Project Name

SeeForAll – Multilingual AI Vision Assistant

Domain
Artificial Intelligence
Machine Learning
Computer Vision
Natural Language Processing
Assistive Technology
Project Type

Engineering / Academic / Hackathon Project

👥 Contributors
Name	Role
Yashodha H R	AI/ML & Development
Team Member 2	Development
Team Member 3	Development
Team Member 4	Documentation / Testing

Replace the team member names and roles with your actual team details.

📸 Screenshots

Project screenshots can be added here.

Create a folder:

screenshots/

Then add images such as:

screenshots/
├── object-detection.png
├── kannada-output.png
├── english-output.png
└── system-demo.png

Then add them to this README using:

![Object Detection](screenshots/object-detection.png)
🔒 Privacy

The current object detection process runs locally on the computer.

The project uses gTTS for speech generation, which requires an internet connection.

Future versions can implement fully offline speech generation for improved privacy and accessibility.

🙏 Acknowledgements

This project uses open-source technologies including:

Ultralytics YOLO
YOLO-World
OpenCV
PyTorch
Google Text-to-Speech
Pygame
⭐ Future Vision

SeeForAll aims to make AI-powered assistive technology more accessible, affordable, and multilingual.

See the world. Hear the world. Experience the world.

💙 SeeForAll

Technology for a more accessible world.

