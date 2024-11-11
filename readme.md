# FaceMatch-Drive

FaceMatch-Drive is a Python-based application that uses the Google Drive API and face recognition to match images in a Google Drive folder with user-provided images. This application authenticates using a Google Cloud service account and utilizes face recognition to identify similar faces within the given images.

## Table of Contents
1. [Features](#features)
2. [Requirements](#requirements)
3. [Setup](#setup)
4. [Running the Project](#running-the-project)
5. [File Structure](#file-structure)
<!-- 6. [Usage](#usage)
7. [Notes on Service Account Authentication](#notes-on-service-account-authentication)
8. [Troubleshooting](#troubleshooting) -->

---

## Features
- **Google Drive Integration:** Retrieves images from a Google Drive folder and uploads matched images to another Drive folder.
- **Face Recognition:** Uses facial recognition to identify matches between images.
- **REST API:** Exposes an endpoint for uploading images and performing matches.

---

## Requirements
1. Python 3.10 or later
2. Google Cloud Service Account with access to Google Drive API
3. The following Python packages:
   - `google-auth`
   - `google-api-python-client`
   - `google-auth-oauthlib`
   - `google-auth-httplib2`
   - `face-recognition` (or an alternative face recognition library)

---

## Setup

### Step 1: Google Cloud Service Account and API Configuration
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. **Create a New Project** (or select an existing project).
3. Enable the **Google Drive API** for this project.
4. **Create a Service Account**:
   - Go to **IAM & Admin > Service Accounts**.
   - Create a new service account and download the credentials file as `credentials.json`.
5. **Set Permissions**:
   - Ensure the service account has `Viewer` or `Editor` permissions on Google Drive.
   - Share the Google Drive folder(s) with the service account email.

### Step 2: Clone the Repository and Set Up Environment
1. **Clone the repository**:
   ```bash
   git clone https://github.com/garchit/FaceMatch-Drive.git
   cd FaceMatch-Drive

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt

3. **Configure Environment Variables**
    ```bash
    export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"

Replace /path/to/credentials.json with the full path to your credentials.json file. 

4. **Add .gitignore for Sensitive Files**
    
5. **Running the Project**

    1. *Start Application*
    ``` bash
    python app.py
    ```
    2. *Endpoints*:

    POST /match: Upload images for comparison with Google Drive images.
    Note: Endpoint names and details may vary depending on your implementation in app.py.


6. **File Stucture**
    ```bash
    FaceMatch-Drive/
    │
    ├── app.py                    # Main application file
    ├── requirements.txt          # List of Python packages required
    ├── .gitignore                # Ignored files for Git
    ├── README.md                 # Project documentation
    └── src/
        ├── drive_api.py          # Handles Google Drive API interactions
        ├── face_recognition.py   # Implements face recognition functions
        └── utils.py              # Utility functions for processing images

