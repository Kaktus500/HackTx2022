from tkinter.tix import Tree
import cv2
import mediapipe as mp
import keyboard
from threading import Thread, Event
from time import sleep
import copy
import numpy as np
import itertools
import csv


class cameraInput:
    def __init__(self, csv_path) -> None:
        self.capture = []
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands
        self.label = None
        self.csv_path = csv_path

    def infer_gesture(self, model):
        self.capture.clear()
        cap = cv2.VideoCapture(0)
        with self.mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        ) as hands:
            while cap.isOpened():
                success, image = cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    # If loading a video, use 'break' instead of 'continue'.
                    continue
                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = hands.process(image)

                # Draw the hand annotations on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                if results.multi_hand_landmarks is not None:
                    prediction = model.single_prediction(
                        self.process_image(image, results)
                    )
                    print(chr(prediction))
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        self.mp_drawing.draw_landmarks(
                            image,
                            hand_landmarks,
                            self.mp_hands.HAND_CONNECTIONS,
                            self.mp_drawing_styles.get_default_hand_landmarks_style(),
                            self.mp_drawing_styles.get_default_hand_connections_style(),
                        )
                # Flip the image horizontally for a selfie-view display.
                cv2.imshow("MediaPipe Hands", cv2.flip(image, 1))
                if cv2.waitKey(5) & 0xFF == ord("q"):
                    break
        cap.release()
        cv2.destroyAllWindows()

    def capture_demo(self):
        self.capture.clear()
        open(self.csv_path, "w").close()
        cap = cv2.VideoCapture(0)
        t = Thread(target=self.capture_label)
        started = False
        self.label = None
        with self.mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        ) as hands:
            while cap.isOpened():
                if not started:
                    t.start()
                    started = True
                success, image = cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    # If loading a video, use 'break' instead of 'continue'.
                    continue

                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = hands.process(image)

                # Draw the hand annotations on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                if self.label and (self.label != "p"):
                    if results.multi_hand_landmarks is not None:
                        self.capture.append(
                            {
                                "img": image,
                                "key_points": results,
                                "label": ord(self.label),
                            }
                        )
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        self.mp_drawing.draw_landmarks(
                            image,
                            hand_landmarks,
                            self.mp_hands.HAND_CONNECTIONS,
                            self.mp_drawing_styles.get_default_hand_landmarks_style(),
                            self.mp_drawing_styles.get_default_hand_connections_style(),
                        )
                # Flip the image horizontally for a selfie-view display.
                cv2.imshow("MediaPipe Hands", cv2.flip(image, 1))
                if cv2.waitKey(5) & 0xFF == ord("q"):
                    break
        cap.release()
        cv2.destroyAllWindows()
        t.join()

    def capture_label(self):
        while (label := keyboard.read_key()) != "q":
            self.label = label
            print(self.label)
            sleep(0.2)

    def process_image(self, img, result):
        for hand_landmarks in result.multi_hand_landmarks:
            # Bounding box calculation
            brect = self.calc_bounding_rect(img, hand_landmarks)
            # Landmark calculation
            landmark_list = self.calc_landmark_list(img, hand_landmarks)
            # Conversion to relative coordinates / normalized coordinates
            pre_processed_landmark_list = self.pre_process_landmark(landmark_list)
            return pre_processed_landmark_list

    def process_capture(self):
        for frame in self.capture:
            results = frame["key_points"]
            if results.multi_hand_landmarks is not None:
                debug_image = copy.deepcopy(frame["img"])
                for hand_landmarks, handedness in zip(
                    results.multi_hand_landmarks, results.multi_handedness
                ):
                    # Bounding box calculation
                    brect = self.calc_bounding_rect(debug_image, hand_landmarks)
                    # Landmark calculation
                    landmark_list = self.calc_landmark_list(debug_image, hand_landmarks)
                    # Conversion to relative coordinates / normalized coordinates
                    pre_processed_landmark_list = self.pre_process_landmark(
                        landmark_list
                    )
                    # pre_processed_point_history_list = self.pre_process_point_history(debug_image, point_history)
                    # Write to the dataset file
                    self.logging_csv(
                        frame["label"],
                        pre_processed_landmark_list,
                    )
        return True

    def calc_bounding_rect(self, image, landmarks):
        image_width, image_height = image.shape[1], image.shape[0]

        landmark_array = np.empty((0, 2), int)

        for _, landmark in enumerate(landmarks.landmark):
            landmark_x = min(int(landmark.x * image_width), image_width - 1)
            landmark_y = min(int(landmark.y * image_height), image_height - 1)

            landmark_point = [np.array((landmark_x, landmark_y))]

            landmark_array = np.append(landmark_array, landmark_point, axis=0)

        x, y, w, h = cv2.boundingRect(landmark_array)

        return [x, y, x + w, y + h]

    def calc_landmark_list(self, image, landmarks):
        image_width, image_height = image.shape[1], image.shape[0]

        landmark_point = []

        # Keypoint
        for _, landmark in enumerate(landmarks.landmark):
            landmark_x = min(int(landmark.x * image_width), image_width - 1)
            landmark_y = min(int(landmark.y * image_height), image_height - 1)
            # landmark_z = landmark.z

            landmark_point.append([landmark_x, landmark_y])

        return landmark_point

    def pre_process_landmark(self, landmark_list):
        temp_landmark_list = copy.deepcopy(landmark_list)

        # Convert to relative coordinates
        base_x, base_y = 0, 0
        for index, landmark_point in enumerate(temp_landmark_list):
            if index == 0:
                base_x, base_y = landmark_point[0], landmark_point[1]

            temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
            temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

        # Convert to a one-dimensional list
        temp_landmark_list = list(itertools.chain.from_iterable(temp_landmark_list))

        # Normalization
        max_value = max(list(map(abs, temp_landmark_list)))

        def normalize_(n):
            return n / max_value

        temp_landmark_list = list(map(normalize_, temp_landmark_list))

        return temp_landmark_list

    def pre_process_point_history(self, image, point_history):
        image_width, image_height = image.shape[1], image.shape[0]

        temp_point_history = copy.deepcopy(point_history)

        # Convert to relative coordinates
        base_x, base_y = 0, 0
        for index, point in enumerate(temp_point_history):
            if index == 0:
                base_x, base_y = point[0], point[1]

            temp_point_history[index][0] = (
                temp_point_history[index][0] - base_x
            ) / image_width
            temp_point_history[index][1] = (
                temp_point_history[index][1] - base_y
            ) / image_height

        # Convert to a one-dimensional list
        temp_point_history = list(itertools.chain.from_iterable(temp_point_history))

        return temp_point_history

    def logging_csv(self, number, landmark_list):
        with open(self.csv_path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([number, *landmark_list])
        return

    def store_capture(self):
        pass
