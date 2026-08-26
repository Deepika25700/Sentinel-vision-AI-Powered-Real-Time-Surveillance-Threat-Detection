# Sentinel-vision-AI-Powered-Real-Time-Surveillance-Threat-Detection

An intelligent video surveillance platform that transforms conventional CCTV footage into actionable security intelligence. The system continuously analyzes live camera feeds or recorded videos, detects and tracks individuals, evaluates their movement patterns, and identifies potentially critical security situations automatically.

By combining YOLOv8, DeepSORT, and contextual rule-based analysis, the system reduces the need for constant manual monitoring and helps security personnel focus on events that require attention.

Overview

Traditional CCTV systems primarily record and display video, leaving security personnel responsible for identifying suspicious activity manually.

This project introduces an AI-based monitoring layer that can:

Understand objects appearing in video streams
Maintain the identity of tracked individuals across frames
Monitor predefined security zones
Analyze movement over time
Identify potentially suspicious situations
Generate alerts when security rules are violated
Provide visual feedback directly on the processed video

The architecture is designed to be modular, allowing additional detection models, notification services, analytics, and camera sources to be integrated in the future.

Key Capabilities
🎯 Intelligent Detection

Uses YOLOv8 to identify objects in each video frame with low latency, making the system suitable for real-time surveillance scenarios.

👥 Persistent Tracking

DeepSORT associates detections between consecutive frames, allowing the system to follow individual people and maintain their movement history.

🚧 Zone-Based Monitoring

Security areas can be defined within the camera view. The system can determine when a tracked person enters or remains inside a protected region.

⏱️ Behavioral Analysis

Instead of analyzing isolated frames, the system considers movement over time to identify events such as prolonged presence or unusual movement.

🚨 Automated Alerts

When predefined security conditions are satisfied, the system generates an alert without requiring an operator to continuously observe the entire camera feed.

Security Intelligence

The system can be configured to identify events such as:

Event	Description
Restricted Area Entry	Detects people entering predefined protected zones
Loitering	Identifies individuals remaining in an area beyond a configured duration
Unauthorized Access	Monitors movement through restricted locations
Suspicious Movement	Evaluates predefined movement patterns
Zone Presence	Tracks individuals present within monitored regions
System Architecture
                 ┌─────────────────────┐
                 │   CCTV / Video File  │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    Video Capture    │
                 │      OpenCV         │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │     YOLOv8          │
                 │  Object Detection   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │      DeepSORT       │
                 │  Object Tracking    │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Event & Rule Engine │
                 │                     │
                 │ • Zone Analysis     │
                 │ • Loitering         │
                 │ • Access Rules      │
                 │ • Movement Analysis │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Alert Generation  │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Annotated Video /   │
                 │ Security Response   │
                 └─────────────────────┘

Technology Stack
Python — Core development
YOLOv8 — Real-time object detection
DeepSORT — Multi-object tracking
OpenCV — Video processing and visualization
PyTorch — Deep learning framework
NumPy — Numerical and data processing
Workflow
Capture frames from a CCTV camera, webcam, or video file.
Run object detection using YOLOv8.
Pass detected objects to DeepSORT for identity tracking.
Maintain tracking information across consecutive frames.
Evaluate object positions, movement, and duration against security rules.
Identify events that satisfy predefined conditions.
Generate appropriate security alerts.
Display the analyzed video with tracking and event annotations.
Installation

Clone the repository:

git clone https://github.com/yourusername/your-repository.git
cd your-repository


Install the required dependencies:

pip install -r requirements.txt


Make sure the required YOLO model weights and configuration files are available according to the project setup.

Usage

Run the application:

python main.py

Webcam
python main.py --source 0

Video File
python main.py --source video.mp4

CCTV / RTSP Stream

If supported by the implementation, an RTSP stream can be supplied as the video source:

python main.py --source "rtsp://camera-stream"

Example Use Cases

The system can be adapted for:

🏢 Office and corporate security
🏭 Industrial facility monitoring
📦 Warehouse surveillance
🎓 Campus security
🏬 Commercial establishments
🏗️ Restricted construction areas
🚪 Controlled-access environments
🏙️ Public-space monitoring
Why This Project?

The goal is to move surveillance from passive video recording to proactive security intelligence.

Rather than requiring an operator to continuously watch multiple screens, the system automatically analyzes video and highlights situations that deserve attention. This makes AI-assisted surveillance useful for environments where continuous monitoring, rapid response, and scalable camera coverage are important.

Future Development

Potential extensions include:

Email and SMS notifications
Telegram and WhatsApp integration
Face recognition
Vehicle detection and tracking
Weapon and dangerous-object detection
Crowd density analysis
Multiple-camera tracking
Cloud-based processing
Web-based monitoring dashboard
Event history and reporting
Security analytics and visualization
Database integration
Edge-device deployment
Learning Outcomes

This project provides practical experience with:

Computer Vision
Deep Learning
Object Detection
Multi-Object Tracking
Real-Time Video Processing
Spatial and Temporal Analysis
Event-Based Decision Systems
AI Application Development
Python and OpenCV
Model Integration and Deployment
Project Structure

A suggested structure for the project:

project/
│
├── main.py
├── requirements.txt
├── README.md
│
├── models/
│   └── yolov8_model.pt
│
├── tracking/
│   └── deepsort.py
│
├── detection/
│   └── detector.py
│
├── rules/
│   └── event_analyzer.py
│
├── alerts/
│   └── alert_manager.py
│
├── utils/
│   └── video_utils.py
│
└── videos/
    └── sample.mp4

Disclaimer

This project is intended for educational, research, and authorized security-monitoring purposes. Any deployment involving CCTV, identification, or monitoring should comply with applicable privacy, surveillance, and data-protection requirements.

License

This project is licensed under the MIT License.

⭐ Project Tagline

From CCTV Footage to Security Intelligence.
