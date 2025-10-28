#!/usr/bin/env python3
"""
Raspberry Pi inference script for TFLite model.
- Uses `tflite_runtime` if available, else falls back to `tensorflow`.
- Uses OpenCV to capture frames from a camera, runs inference, and prints label + confidence and latency.
- Logs outputs to `results/inference_log.csv`.

Usage: python3 inference_pi.py --model path/to/model.tflite --labels labels.txt
"""

import time
import argparse
import csv
import os

import importlib

try:
    # Load tflite_runtime dynamically to avoid static analyzers reporting an unresolved import
    _tflite_mod = importlib.import_module('tflite_runtime.interpreter')
    Interpreter = _tflite_mod.Interpreter
except Exception:
    # Fallback to full TF (may be heavy on Pi)
    try:
        import tensorflow as tf
        Interpreter = tf.lite.Interpreter
    except Exception:
        # If neither tflite_runtime nor tensorflow is available, provide a clear error at runtime.
        class Interpreter:
            def __init__(self, *args, **kwargs):
                raise RuntimeError("Neither tflite_runtime.interpreter nor tensorflow.lite is available; install one to run inference.")

try:
    _cv2 = importlib.import_module('cv2')
    cv2 = _cv2
except Exception as e:
    raise RuntimeError(
        "OpenCV (cv2) is required for this script; install it with "
        "'pip install opencv-python' or 'sudo apt install python3-opencv' and retry."
    ) from e

import numpy as np


def load_labels(path):
    with open(path, 'r') as f:
        return [l.strip() for l in f.readlines()]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', required=True, help='Path to .tflite model')
    parser.add_argument('--labels', required=True, help='Path to labels.txt (one per line)')
    parser.add_argument('--camera', type=int, default=0, help='Camera device id')
    parser.add_argument('--width', type=int, default=160)
    parser.add_argument('--height', type=int, default=160)
    args = parser.parse_args()

    labels = load_labels(args.labels)
    interpreter = Interpreter(args.model)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    cap = cv2.VideoCapture(args.camera)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)

    os.makedirs('results', exist_ok=True)
    log_path = os.path.join('results', 'inference_log.csv')
    if not os.path.exists(log_path):
        with open(log_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'pred_label', 'confidence', 'latency_ms'])

    print('Starting inference loop. Press q to quit.')
    while True:
        ret, frame = cap.read()
        if not ret:
            print('Camera read failed')
            break
        img = cv2.resize(frame, (args.width, args.height))
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        input_data = np.expand_dims(img_rgb.astype(np.float32) / 255.0, axis=0)

        # Adjust input type if interpreter expects uint8
        if input_details[0]['dtype'] == np.uint8:
            input_data = (input_data * 255).astype(np.uint8)

        start = time.time()
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()
        out = interpreter.get_tensor(output_details[0]['index'])
        latency = (time.time() - start) * 1000.0

        if out.ndim == 2:
            probs = out[0]
        else:
            probs = out
        top = probs.argmax()
        conf = float(probs[top])
        label = labels[top] if top < len(labels) else str(top)

        ts = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f'[{ts}] {label} ({conf:.3f}) latency={latency:.1f}ms')

        with open(log_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([ts, label, conf, f'{latency:.1f}'])

        # display
        cv2.putText(frame, f'{label} {conf:.2f} {latency:.0f}ms', (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
        cv2.imshow('Inference', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
