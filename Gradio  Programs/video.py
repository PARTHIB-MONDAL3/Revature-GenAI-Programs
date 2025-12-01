import uuid
import os
import tempfile
import cv2
import numpy as np
from ultralytics import YOLO
import gradio as gr

# Load YOLO
yolo = YOLO("yolov8n.pt")


def _make_output_path(ext="mp4"):
    return os.path.join(tempfile.gettempdir(), f"yolo_out_{uuid.uuid4().hex}.{ext}")


def _process_frames_to_video(frames, fps, size):
    out_path = _make_output_path("mp4")
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(out_path, fourcc, fps, size, True)

    for f in frames:
        if f.ndim == 2:
            f = cv2.cvtColor(f, cv2.COLOR_GRAY2BGR)
        f_bgr = cv2.cvtColor(f, cv2.COLOR_RGB2BGR)
        writer.write(f_bgr)

    writer.release()
    return out_path


def detect_objects_in_video(video_file, process_every_n_frames=1):
    if not video_file:
        raise gr.Error("No video uploaded.")

    video_path = video_file.name  # because gr.File returns an object

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise gr.Error("Could not open video file.")

    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    size = (width, height)

    frames_out = []
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % process_every_n_frames == 0:
            results = yolo(frame)
            annotated = results[0].plot()
            last_annotated = annotated

        frames_out.append(last_annotated)
        frame_idx += 1

    cap.release()
    return _process_frames_to_video(frames_out, fps, size)


# -----------------------------------------
# GRADIO UI (compatible with old versions)
# -----------------------------------------
with gr.Blocks(title="Video Object Detection") as demo:

    gr.Markdown("## YOLOv8 - Video Object Detection")

    video_file = gr.File(label="Upload Video File")     # <--- old compatible
    proc_slider = gr.Slider(1, 10, value=1, step=1, label="Process every N frames")

    out_video = gr.Video(label="Output Video")

    run_btn = gr.Button("Run Detection")

    run_btn.click(
        fn=detect_objects_in_video,
        inputs=[video_file, proc_slider],
        outputs=out_video
    )

demo.launch()
