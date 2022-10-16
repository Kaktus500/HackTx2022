import cv2
from camera_input import cameraInput
import pickle
import os
from datetime import datetime
from inspect import getsourcefile

date = datetime.now().isoformat()

basePath = os.path.dirname(os.path.abspath(getsourcefile(lambda: 0)))

data_path = os.path.join(basePath,'model','keypoint_classifier','data','1234')

cam = cameraInput()
cam.capture_video()
with open(data_path, 'wb') as f:
    pickle.dump(cam.capture, f)
