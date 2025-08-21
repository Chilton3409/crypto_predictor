#!/usr/bin/env python3
#New file created
# Import necessary libraries
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.datasets import load_iris
import numpy as np
import keras 

class IrisClassifier:
    def __init__(self, test_size=0.2, random_state=42):
        self.test_size = test_size
        self.random_state = random_state
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.scaler = StandardScaler()
        self.model = None

    def load_data(self):
        iris = load_iris()
        X = iris.data
        y = iris.target
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=self.test_size, random_state=self.random_state)

    def scale_features(self):
        self.X_train = self.scaler.fit_transform(self.X_train)
        self.X_test = self.scaler.transform(self.X_test)

    def create_model(self):
        self.model = Sequential()
        self.model.add(Dense(64, activation='relu', input_shape=(4,)))
        self.model.add(Dense(32, activation='relu'))
        self.model.add(Dense(3, activation='softmax'))
        self.model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    def train_model(self, epochs=50, batch_size=32):
        self.model.fit(self.X_train, self.y_train, epochs=epochs, batch_size=batch_size, verbose=0)

    def evaluate_model(self):
        y_pred = self.model.predict(self.X_test)
        y_pred_class = np.argmax(y_pred, axis=1)
        accuracy = accuracy_score(self.y_test, y_pred_class)
        print(f"Accuracy: {accuracy:.3f}")
        print("Classification Report:")
        print(classification_report(self.y_test, y_pred_class))
        print("Confusion Matrix:")
        print(confusion_matrix(self.y_test, y_pred_class))

    def run(self):
        self.load_data()
        self.scale_features()
        self.create_model()
        self.train_model()
        self.evaluate_model()


if __name__ == "__main__":
    classifier = IrisClassifier()
    classifier.run()
