⚠ The Public Data Portal API server is currently down, so the program will not function correctly. ⚠
⚠ Use "Dungeon_Escape.ipynb" when working with Anaconda, and use "Dengeon_Escape.py" when working with Visual Studio Code. ⚠

[Character Controls]
Exploration
 - Control the character using MediaPipe hand tracking.
 - The character moves based on the area detected by the camera.
Battle
 - Connect a microphone and follow the guide commands displayed on the right side to perform battle actions.

[External Packages - Installation Required]
 - pygame
 - opencv-python
 - numpy
 - SpeechRecognition
 - mediapipe
 - requests
 - xmltodict

[Internal Packages - No Installation Required]
 - math
 - sys
 - random
 - time
 - threading
 - weather (custom module included in the project source)

[Setup Guide]
For Anaconda users
1. Create a virtual environment
  ① conda create -n venv python=3.10 -y
  ② conda activate venv
2. Upgrade pip and essential tools
  ① python -m pip install --upgrade pip setuptools wheel
3. Install required packages
  ① pip install pygame opencv-python mediapipe SpeechRecognition requests xmltodict numpy

For Visual Studio Code users
1. Install Python 3.10 or higher
  Download from the official Python website.
2. Create a virtual environment
  cd C:\python   # Example: move to your project folder

  python -m venv venv  # Create virtual environment

  venv\Scripts\activate  # Activate (Windows)
3. Upgrade pip
  python  -m pip install --upgrade pip setuptools wheel
4. Install required packages
  pip install pygame opencv-python mediapipe SpeechRecognition requests xmltodict numpy
5. Run the project
  python Dungeon_Escape.py
