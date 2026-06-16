# Real-Time Face Recognition Attendance System

A real-time attendance management system powered by Face Recognition and One-Shot Learning. The system automatically identifies registered users through a webcam and records attendance in real time. Facial images and user information are stored in Supabase, while facial embeddings are generated and serialized for efficient recognition.

---

## Overview

Traditional attendance systems require manual check-ins, which are time-consuming and prone to fraud. This project automates the attendance process using facial recognition technology.

The system follows a One-Shot Learning approach, meaning each user only needs a small number of sample images for registration. These images are converted into facial embeddings and later used for real-time face matching.

---

## Features

* Real-time face recognition using webcam input
* One-Shot Learning based enrollment
* Automatic attendance recording
* Face image storage using Supabase Storage
* User information management with Supabase Database
* Fast face matching using pre-computed embeddings
* Simple enrollment workflow
* Scalable cloud-based architecture

---

## System Workflow

### 1. Face Registration

The first step is to collect facial samples from each user.

* Capture face images using a camera.
* Save the original images.
* Upload images to Supabase Storage.
* Store user metadata in Supabase Database.

```text
User
  ↓
Capture Face Images
  ↓
Supabase Storage
```

---

### 2. Face Cropping and Preprocessing

Since images are captured under different conditions and resolutions, facial regions must be normalized before feature extraction.

The preprocessing stage:

* Detects the face region.
* Crops the face from the original image.
* Resizes the cropped face to a fixed size.
* Removes unnecessary background information.

Benefits:

* Consistent input dimensions.
* Better embedding quality.
* Improved recognition accuracy.

```text
Original Image
      ↓
Face Detection
      ↓
Face Cropping
      ↓
Fixed-Size Face Image
```

---

### 3. Face Encoding Generation

The `encode_generator.py` script is responsible for generating facial embeddings.

Process:

1. Retrieve registered face images.
2. Detect and encode each face.
3. Generate a numerical feature vector (embedding).
4. Save embeddings into a serialized `.pkl` file.

The generated embeddings serve as the facial identity database used during recognition.

```text
Face Images
      ↓
Feature Extraction
      ↓
Face Embeddings
      ↓
encodings.pkl
```

---

### 4. Real-Time Face Recognition

The `main.py` file performs real-time attendance tracking.

Workflow:

1. Open webcam stream.
2. Detect faces in each frame.
3. Generate embedding for detected faces.
4. Load stored embeddings from the `.pkl` file.
5. Compare embeddings using similarity matching.
6. Identify the closest registered user.
7. Retrieve user information from Supabase.
8. Mark attendance automatically.

```text
Webcam Stream
      ↓
Face Detection
      ↓
Face Encoding
      ↓
Embedding Comparison
      ↓
Identity Match
      ↓
Attendance Logging
```

---

## Project Architecture

```text
                    ┌─────────────────────┐
                    │      Supabase       │
                    │                     │
                    │  User Information   │
                    │  Face Images        │
                    └──────────┬──────────┘
                               │
                               ▼

                     Face Registration
                               │
                               ▼

                     Face Preprocessing
                               │
                               ▼

                     EncodeGenerator.py
                               │
                               ▼

                         encodings.pkl
                               │
                               ▼

                          main.py
                               │
                               ▼

                     Real-Time Recognition
                               │
                               ▼

                    Attendance Management
```

---

## Technologies Used

### Computer Vision

* OpenCV
* Face Recognition
* NumPy

### Database & Storage

* Supabase Database
* Supabase Storage

### Serialization

* Pickle (`.pkl`)

### Programming Language

* Python

## How It Works

### Enrollment Phase

* Capture user face images.
* Crop and normalize faces.
* Upload images to Supabase.
* Generate embeddings using `encode_generator.py`.
* Save embeddings into `encode_file.pkl`.

### Recognition Phase

* Start webcam stream.
* Detect face in real time.
* Generate face embedding.
* Compare with stored embeddings.
* Identify user.
* Record attendance automatically.

---

## Advantages

* Requires only a few sample images per person.
* Fast recognition process.
* Lightweight embedding storage.
* Cloud-based image management.
* Easy integration into schools, universities, and workplaces.
* Real-time attendance tracking.

---

## Future Improvements

* Face anti-spoofing detection
* Multiple face tracking
* Attendance analytics dashboard
* Mobile application support
* Deep learning-based embedding models
* Multi-camera deployment

---

## License

This project is developed for educational and research purposes.
