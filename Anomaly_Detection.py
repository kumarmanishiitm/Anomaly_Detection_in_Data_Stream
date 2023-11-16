import time
import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

class AnomalyDetectorIsolationForest:
    def __init__(self, window_size=10,contamination=0.05):
        self.window_size = window_size
        self.data_stream = []
        self.anomalies = []
        self.contamination=contamination
        # Initialize the Isolation Forest model
        self.model = IsolationForest(n_estimators=100,contamination=self.contamination)

    def simulate_data_stream(self):
        while True:
            data_point = self.generate_data_point()
            self.data_stream.append(data_point)
            self.detect_anomaly(data_point)
            self.visualize_data_stream()
            time.sleep(1)

    def generate_data_point(self):
    	# Simulate a data stream with regular patterns, seasonal elements, and random noise
        time1 = time.time()%1000
        regular_pattern = np.tanh(0.02 * time1) * 10
        seasonal_pattern = np.tanh(0.1 * time1) * 5
        #noise = np.random.normal(0, 2,1000)
        noise = random.gauss(0, 1)
        data_stream = regular_pattern + seasonal_pattern + noise
        return data_stream

    def detect_anomaly(self, data_point):
        if len(self.data_stream) > self.window_size:
            window_data = np.array(self.data_stream[-self.window_size:]).reshape(-1, 1)

            self.model.fit(window_data)

            # Predict anomaly score
            anomaly_score = self.model.decision_function([[data_point]])

            if anomaly_score < 0:
                print(len(self.data_stream), f"Anomaly detected: {data_point}", )
                self.anomalies.append((len(self.data_stream), data_point))

    def visualize_data_stream(self):
        plt.plot([i for i in range(len(self.data_stream))], self.data_stream, label="Data Stream")
        if self.anomalies:
            anomalies_x, anomalies_y = zip(*self.anomalies)
            plt.scatter(anomalies_x, anomalies_y, color='red', label="Anomalies")
        plt.xlabel("Data Point Index")
        plt.ylabel("Data Value")
        plt.title("Real-Time Data Stream Visualization with Anomalies (Isolation Forest)")
        plt.legend()
        plt.pause(0.1)
        plt.clf()

if __name__ == "__main__":
    isolation_forest_detector = AnomalyDetectorIsolationForest(window_size=10,contamination=0.2)
    isolation_forest_detector.simulate_data_stream()

