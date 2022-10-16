import csv
import cv2
from camera_input import cameraInput
import pickle
import os
from datetime import datetime
from inspect import getsourcefile
from gesture_model import Model

date = datetime.now().isoformat()

basePath = os.path.dirname(os.path.abspath(getsourcefile(lambda: 0)))

data_path = os.path.join(
    basePath, "model", "keypoint_classifier", "data", "keypoint.csv"
)

model_path = os.path.join(
    basePath, "model", "keypoint_classifier", "models", "keypoint_classifier.hdf5"
)
data_path = os.path.join(
    basePath, "model", "keypoint_classifier", "data", "keypoint.csv"
)
encoder_path = os.path.join(basePath, "le.obj")

cam = cameraInput(csv_path=data_path)
cam.capture_demo()
cam.process_capture()
model = Model(model_path, encoder_path)
model.load_model()
cam.infer_gesture(model)
