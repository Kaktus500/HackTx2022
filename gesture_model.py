import imp
from tabnanny import verbose
import numpy as np
import tensorflow as tf
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split


class Model:
    def __init__(self, model_path, encoder_path) -> None:
        self.model_path = model_path
        self.RANDOM_SEED = 42
        with open(encoder_path, "rb") as f:
            self.encoder = pickle.load(f)

    def load_model(self):
        self.model = tf.keras.models.load_model(self.model_path)

    def train_model(self, data_path):
        encoder = LabelEncoder()
        X_dataset = np.loadtxt(
            data_path,
            delimiter=",",
            dtype="float32",
            usecols=list(range(1, (21 * 2) + 1)),
        )
        y_dataset = np.loadtxt(data_path, delimiter=",", dtype="int32", usecols=(0))
        y_dataset_encoded = encoder.fit_transform(y_dataset)
        X_train, X_test, y_train, y_test = train_test_split(
            X_dataset, y_dataset_encoded, train_size=0.75, random_state=self.RANDOM_SEED
        )
        NUM_CLASSES = len(encoder.classes_)
        model = tf.keras.models.Sequential(
            [
                tf.keras.layers.Input((21 * 2,)),
                tf.keras.layers.Dropout(0.2),
                tf.keras.layers.Dense(20, activation="relu"),
                tf.keras.layers.Dropout(0.4),
                tf.keras.layers.Dense(10, activation="relu"),
                tf.keras.layers.Dense(NUM_CLASSES, activation="softmax"),
            ]
        )
        cp_callback = tf.keras.callbacks.ModelCheckpoint(
            self.model_path, verbose=0, save_weights_only=False
        )
        es_callback = tf.keras.callbacks.EarlyStopping(patience=20, verbose=1)
        model.compile(
            optimizer="adam",
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"],
        )
        model.fit(
            X_train,
            y_train,
            epochs=1000,
            batch_size=64,
            validation_data=(X_test, y_test),
            callbacks=[cp_callback, es_callback],
        )
        self.model = model
        self.encoder = encoder

    def single_prediction(self, landmark_list):
        prediction = self.model.predict(np.array([landmark_list]), verbose=0)
        prediction = np.array([np.argmax(prediction)])
        prediction_decoded = self.encoder.inverse_transform(prediction)[0]
        return prediction_decoded
