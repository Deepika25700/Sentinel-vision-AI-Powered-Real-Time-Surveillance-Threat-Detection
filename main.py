import streamlit as st
import cv2
import time
from ultralytics import YOLO
import requests
import os
from dotenv import load_dotenv
from io import BytesIO

# CONFIG

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

VIDEO_SOURCE = "video.mp4"
LOITER_TIME = 15

model = YOLO("yolov8n.pt")

# STREAMLIT SETUP

st.set_page_config(page_title="AI Security System", layout="wide")
st.title("AI Surveillance System (YOLO + Telegram)")

left, right = st.columns([2, 1])
video_box = left.empty()
log_box = right.empty()

# SESSION STATE

if "run" not in st.session_state:
    st.session_state.run = False

if "alerts" not in st.session_state:
    st.session_state.alerts = []

# BUTTONS

with right:
    if st.button("Start"):
        st.session_state.run = True

    if st.button("Stop"):
        st.session_state.run = False

# VIDEO CAPTURE

cap = cv2.VideoCapture(VIDEO_SOURCE)

if not cap.isOpened():
    st.error("Video not found or cannot be opened")
    st.stop()

ret, frame = cap.read()
if not ret:
    st.error("Cannot read video frame")
    st.stop()

h, w, _ = frame.shape

# SECURITY ZONE
ZONE_X1, ZONE_Y1 = int(w * 0.2), int(h * 0.2)
ZONE_X2, ZONE_Y2 = int(w * 0.7), int(h * 0.7)

# MEMORY

zone_entry_time = {}
person_first_seen = {}
intrusion_alerted = set()
loiter_alerted = set()

# TELEGRAM FUNCTIONS

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        r = requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
        print("Telegram:", r.text)
    except Exception as e:
        print("Telegram error:", e)


def send_photo(frame, caption):
    try:
        _, buffer = cv2.imencode(".jpg", frame)
        bio = BytesIO(buffer.tobytes())
        bio.name = "alert.jpg"

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        r = requests.post(
            url,
            data={"chat_id": CHAT_ID, "caption": caption},
            files={"photo": bio}
        )
        print("Photo:", r.text)

    except Exception as e:
        print("Photo error:", e)

# MAIN LOOP

while True:

    if not st.session_state.run:
        time.sleep(0.5)
        continue

    ret, frame = cap.read()
    if not ret:
        break

    results = model.track(
        frame,
        persist=True,
        tracker="bytetrack.yaml",
        verbose=False
    )

    # DRAW ZONE
    cv2.rectangle(frame, (ZONE_X1, ZONE_Y1), (ZONE_X2, ZONE_Y2), (0, 0, 255), 2)

    if results and results[0].boxes is not None and results[0].boxes.id is not None:

        for box in results[0].boxes:

            # PERSON ONLY
            if int(box.cls[0]) != 0:
                continue

            track_id = int(box.id[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            # FIRST SEEN
            if track_id not in person_first_seen:
                person_first_seen[track_id] = time.time()

            # ZONE CHECK
            inside = (ZONE_X1 <= cx <= ZONE_X2 and ZONE_Y1 <= cy <= ZONE_Y2)

            if inside:

                if track_id not in zone_entry_time:
                    zone_entry_time[track_id] = time.time()

                zone_time = time.time() - zone_entry_time[track_id]

                # INTRUSION ALERT (instant)
                if track_id not in intrusion_alerted:
                    msg = f" INTRUSION ALERT | ID: {track_id}"
                    st.session_state.alerts.append(msg)
                    send_telegram(msg)
                    send_photo(frame, msg)
                    intrusion_alerted.add(track_id)

                # LOITERING ALERT
                if zone_time > LOITER_TIME and track_id not in loiter_alerted:
                    msg = f" LOITERING ALERT | ID: {track_id}"
                    st.session_state.alerts.append(msg)
                    send_telegram(msg)
                    send_photo(frame, msg)
                    loiter_alerted.add(track_id)

            else:
                zone_entry_time.pop(track_id, None)

            # DRAW BOX
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"ID:{track_id}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # DISPLAY
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    video_box.image(frame_rgb, use_container_width=True)

    log_box.write("### Alerts")
    log_box.write(st.session_state.alerts[-10:])

    time.sleep(0.03)

cap.release()
