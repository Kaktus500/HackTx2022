import csv
import cv2
from camera_input import cameraInput
import pickle
import os
from datetime import datetime
from inspect import getsourcefile

date = datetime.now().isoformat()

basePath = os.path.dirname(os.path.abspath(getsourcefile(lambda: 0)))

data_path = os.path.join(
    basePath, "model", "keypoint_classifier", "data", "keypoint.csv"
)

cam = cameraInput(csv_path=data_path)
cam.capture_video()
cam.process_capture()
