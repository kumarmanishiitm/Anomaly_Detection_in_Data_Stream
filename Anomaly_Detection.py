import numpy as np
import time
import random
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

class Anomaly_Detector_using_IsolationForest:
    def __init__(self, window_size=10, contamination=0.2):
        """
        Initializes an instance of the Anomaly_Detector_using_IsolationForest class.

        Parameters:
        - window_size (int): Size of the window for anomaly detection.
        - contamination (float): Proportion of anomalies expected in the data stream.

        Attributes:
        - window_size (int): Size of the window for anomaly detection.
        - data_stream (list): A list to store the incoming data stream.
        - anomalies (list): A list to store detected anomalies.
        - contamination (float): Proportion of anomalies expected in the data stream.
        - model (IsolationForest): An instance of the IsolationForest model for anomaly detection.

        Initializes the Isolation Forest model with specified parameters.
        """
        # Initialize window 
        self.window_size = window_size
        
        # Initialize an empty list to store the data stream
        self.data_stream = []
        
        # Initialize an empty list to store detected anomalies
        self.anomalies = []
        
        # Set the proportion of anomalies
        self.contamination = contamination
        
        # Initialize the Isolation Forest model with 100 estimators and specified contamination
        self.model = IsolationForest(n_estimators=100, contamination=self.contamination)

    def simulate_the_data_stream(self):
        """
        Simulates the data stream in real-time.

        Continuously generates synthetic data points, appends them to the data stream,
        detects anomalies, and visualizes the data stream. The loop runs indefinitely with
        a sleep interval of 1 second between iterations.

        This method is designed for real-time simulation and anomaly detection.

        Note: This function should be executed in a separate thread or process to avoid
        blocking the main execution.
        """
        while True:
            data_point = self.generate_our_data_point()  # Generate a synthetic data point
            self.data_stream.append(data_point)          # Append the data point to the stream
            self.detect_anomaly(data_point)              # Detect anomalies in real-time
            self.visualize_data_stream()                  # Visualize the data stream
            time.sleep(1)                                 # Pause for 1 second between iterations

    def generate_our_data_point(self):
        """
        Generates a synthetic data point for the data stream.

        Simulates a data stream with regular patterns, seasonal elements, and random noise.
        The time component is obtained using the current time modulo 1000 for periodicity.
        The regular and seasonal patterns are created using the hyperbolic tangent function.
        Random noise is introduced using Gaussian distribution, and all components are combined
        to form the simulated data point.

        Returns:
        - data_stream (float): The simulated data point for the data stream.
        """
        # Obtain the current time modulo 1000 for periodicity
        time1 = time.time() % 1000
        #time1=len(self.data_stream)
        
        # Create a regular pattern and seasonal pattern using hyperbolic tangent function
        regular_pattern = np.tanh(0.02 * time1) * 10
        seasonal_pattern = np.tanh(0.1 * time1) * 5
        
        # Generate random noise using Gaussian distribution
        noise = random.gauss(0, 1)
        
         # Combine the components to form the simulated data point
        data_stream = regular_pattern + seasonal_pattern + noise
        
        # Return the simulated data point
        return data_stream

    def detect_anomaly(self, data_point):
        """
        Detects anomalies in the data stream.

        Parameters:
        - data_point (float): The current data point to be evaluated for anomaly detection.

        This method adds the data point to the window, trains the Isolation Forest model
        with the current window, and predicts whether the current data point is an anomaly.
        If an anomaly is detected, it prints a message and appends the anomaly information
        to the list of detected anomalies.

        Parameters:
        - data_point (float): The current data point to be evaluated for anomaly detection.
        """
        # Add data point to the window
        if len(self.data_stream) > self.window_size:
            window_data = self.data_stream[-self.window_size:]
            
            # Train the model with the current window
            self.model.fit(np.array(window_data).reshape(-1, 1))

            # Predict if the current data point is an anomaly
            anomaly_score = self.model.decision_function([[data_point]])

            if anomaly_score < 0:
                print(f"Anomaly detected: {data_point} at Time Step {len(self.data_stream)}")
                self.anomalies.append((len(self.data_stream), data_point))

    def visualize_data_stream(self):
        """
        Visualizes the data stream and detected anomalies in real-time.

        This method creates a line plot for the entire data stream and checks for
        anomalies, plotting them in red. It utilizes Matplotlib for visualization.
        """
        # Creating a line plot for the data stream
        x_values = [i for i in range(len(self.data_stream))]
        y_values = self.data_stream
         # Plot data stream
        plt.plot(x_values, y_values, label="Data Stream")

        # Checking for anomalies and plotting them in red
        if self.anomalies:
            anomalies_x, anomalies_y =[],[]
            
            # Alternative representation using a for loop and zip
            for anomaly in self.anomalies:
                anomalies_x.append(anomaly[0])
                anomalies_y.append(anomaly[1])
            plt.scatter(anomalies_x, anomalies_y, color="red", label="Anomaly")

        plt.xlabel("Data Point")
        plt.ylabel("Data Value")
        plt.title("Real-Time Data Stream and Anomalies using Isolation Forest")
        plt.legend()
        plt.pause(0.1)  # Pause to allow for real-time visualization
        plt.clf()       # Clear the plot for the next iteration

if __name__ == "__main__":
     #we have checked parameters contamination with many values
     #cont=[0.1,0.2,0.3,0.05]
     #for contamination in cont:
     #	Algo_isolation_forest = Anomaly_Detector_using_IsolationForest(window_size=10, contamination=0.2)
     #	Algo_isolation_forest.simulate_the_data_stream()
     	
     	
    # Create an instance of the AnomalyDetectorIsolationForest class with a window size of 10 and contamination=0.2
    Algo_isolation_forest = Anomaly_Detector_using_IsolationForest(window_size=10, contamination=0.2)
    # Simulate a data stream
    Algo_isolation_forest.simulate_the_data_stream()

