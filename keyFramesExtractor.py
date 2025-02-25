import cv2
import os

def extract_frames(video_path, output_folder, interval=10, start_time=1):
    os.makedirs(output_folder, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))  # Get frame rate
    start_frame = frame_rate * start_time
    count = 0
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if count >= start_frame:  # Start saving after 1 second
            if (count - start_frame) % (frame_rate * interval) == 0:
                frame_filename = f"{output_folder}/frame_{frame_count}.jpg"
                cv2.imwrite(frame_filename, frame)
                frame_count += 1
        count += 1
    cap.release()

video_path = "./assets/base.mp4"
output_folder = "extracted_frames"
extract_frames(video_path, output_folder)
print(f"Frames extracted and saved in {output_folder}")
