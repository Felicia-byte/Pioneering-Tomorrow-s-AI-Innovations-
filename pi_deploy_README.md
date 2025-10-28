Raspberry Pi inference instructions

1. Copy the quantized TFLite model to the Pi, e.g., `recyclables_model_int8.tflite`.
2. Copy a `labels.txt` file with one class label per line (matching model training order).
3. Install runtime and dependencies (example for Raspberry Pi OS):

```powershell
python3 -m pip install --upgrade pip
python3 -m pip install tflite-runtime numpy opencv-python
```

Note: `opencv-python` may be heavy; for Raspberry Pi consider `opencv-python-headless` or build OpenCV with required bindings.

4. Run inference:

```powershell
python3 inference_pi.py --model /home/pi/recyclables_model_int8.tflite --labels /home/pi/labels.txt
```

5. Press `q` in the display window to quit. Logs will be written to `results/inference_log.csv`.
