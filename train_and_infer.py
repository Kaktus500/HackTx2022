import csv
import cv2
from camera_input import cameraInput
import pickle
import os
from datetime import datetime
from inspect import getsourcefile
from gesture_model import Model
from time import sleep

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
print("Show the gesture in")
sleep(1)
print("3")
sleep(1)
print("2")
sleep(1)
print("1")
sleep(1)
print("Press q when finished")
cam.capture_demo(label="1")
cam.process_capture()
print("Capture finished")
print("Showcase a baseline movement")
sleep(1)
print("3")
sleep(1)
print("2")
sleep(1)
print("1")
sleep(1)
print("Press q when finished")
cam.capture_demo(label="d")
cam.process_capture()
print("Capture finished")
model = Model(model_path, encoder_path)
model.train_model(data_path=data_path)
cam.infer_gesture(model)
