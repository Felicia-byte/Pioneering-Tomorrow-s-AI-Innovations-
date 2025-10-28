# Pioneering Tomorrow’s AI Innovations — Edge AI Prototype

This folder contains an Edge AI prototype scaffold: a Colab/Jupyter notebook that demonstrates training a lightweight image classifier (transfer learning with MobileNetV2), converting it to TensorFlow Lite, and a short guide to deploy on Raspberry Pi.

Files

- `edge_ai_prototype_notebook.ipynb` — Colab-compatible notebook with training + TFLite conversion example.
- `requirements.txt` — Python dependencies for local runs.

Quick start (Colab)

1. Open the notebook in Colab: Upload the notebook file or open from GitHub.\n2. If using your own dataset, upload a directory with `train/<class>/*` and `val/<class>/*` or modify the notebook to use your Kaggle dataset (see notes).\n3. Run the cells in order. The notebook includes model save and TFLite conversion.

Raspberry Pi deployment (high level)

1. Copy the quantized TFLite model (e.g., `recyclables_model_int8.tflite`) to the Pi.\n2. Install runtime on Pi (for Raspberry Pi OS, prefer `tflite-runtime`):\n

```powershell
# On the Pi (example for Raspbian / Raspberry Pi OS, adjust version & link):
python3 -m pip install --upgrade pip
python3 -m pip install tflite-runtime
python3 -m pip install numpy pillow
```

3.Write an inference script that uses `tflite_runtime.Interpreter` to load the model and run inference on camera frames. Use OpenCV or PiCamera to capture frames, resize to the model's input size, run inference, and display predicted label with confidence.

Notes on dataset and metrics

- For the assignment use a recyclable-items dataset (TrashNet or similar) from Kaggle.\n- Track metrics: train/val accuracy, confusion matrix, per-class precision/recall.\n- Compare float32 vs int8 model size and latency on-device.

Resources & tips

- If you can't run on an actual Pi, you can test latency by running the TFLite model on a small ARM emulator or measure inference time on Colab (CPU) as a proxy.\n- For best Edge performance, use post-training quantization and optimize the input resolution to balance accuracy and latency.

Contact
If you want, I can adapt this notebook to use a specific Kaggle dataset and add a simple evaluation script that outputs accuracy & confusion matrix to `results/`.
