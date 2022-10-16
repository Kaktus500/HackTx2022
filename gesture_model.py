from tabnanny import verbose
import numpy as np
import tensorflow as tf
import pickle


class Model:
    def __init__(self, model_path, encoder_path) -> None:
        self.model_path = model_path
        with open(encoder_path, "rb") as f:
            self.encoder = pickle.load(f)

    def load_model(self):
        self.model = tf.keras.models.load_model(self.model_path)

    def single_prediction(self, landmark_list):
        prediction = self.model.predict(np.array([landmark_list]), verbose=0)
        prediction = np.array([np.argmax(prediction)])
        prediction_decoded = self.encoder.inverse_transform(prediction)[0]
        return prediction_decoded
