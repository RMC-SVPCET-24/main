import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import ConvLSTM2D, BatchNormalization, Conv2D
from data_scaling import DataScaling
import matplotlib.pyplot as plt

class DataSequence:
    def __init__(self):
        scale = DataScaling()
        self.data = scale.scale_data()  # Call the method to get the actual scaled data

    def create_sequence(self, sequence_length=13):
        X = []
        Y = []
        for i in range(0, len(self.data) - sequence_length, 19):
            for j in range(i, i + 19 - sequence_length):
                X.append(self.data[j:j + sequence_length])
                Y.append(self.data[j + sequence_length])
        
        X, Y = np.array(X), np.array(Y)
        X = X[..., np.newaxis]  # Adding an extra dimension for the ConvLSTM
        Y = Y[..., np.newaxis]

        return X, Y


class ModelMaking:
    def __init__(self, X):
        sequence_length = 13
        # Define input shape based on the shape of X
        self.input_shape = (sequence_length, X.shape[1], X.shape[2], X.shape[3])
        
        self.model = Sequential([
            ConvLSTM2D(filters=32, kernel_size=(2, 2), padding="same", return_sequences=True,
                       input_shape=self.input_shape),
            BatchNormalization(),
            ConvLSTM2D(filters=16, kernel_size=(2, 2), padding="same", return_sequences=False),
            BatchNormalization(),
            Conv2D(filters=3, kernel_size=(2, 2), activation='sigmoid', padding="same")
        ])
        self.model.compile(optimizer='adam', loss='mse')

    def train(self, X, Y, epochs=10, batch_size=32):
        self.model.fit(X, Y, epochs=epochs, batch_size=batch_size)



class PredictionPlotter:
    def __init__(self, data, predicted_next_step):
        """
        Initialize the PredictionPlotter class with actual data and predicted next step.
        
        Parameters:
        - data: The actual data array, expected to have shape (height, width, channels)
        - predicted_next_step: The predicted next step, expected to have shape (height, width, channels)
        """
        self.data = data
        self.predicted_next_step = predicted_next_step

    def plot(self):
        """
        Plots the actual data and predicted next step for each channel (Reflectivity, Velocity, Total Power).
        """
        fig, axs = plt.subplots(2, 3, figsize=(15, 10))  # Create a 2x3 subplot (one row for original data, another for predictions)
        
        # Plot actual data (Reflectivity, Velocity, Total Power)
        axs[0, 0].imshow(self.data[:, :, 0], cmap='viridis')
        axs[0, 0].set_title("Reflectivity (Original)")
        axs[0, 1].imshow(self.data[:, :, 1], cmap='viridis')
        axs[0, 1].set_title("Velocity (Original)")
        axs[0, 2].imshow(self.data[:, :, 2], cmap='viridis')
        axs[0, 2].set_title("Total Power (Original)")
        
        # Plot predicted next step (Reflectivity, Velocity, Total Power)
        axs[1, 0].imshow(self.predicted_next_step[:, :, 0], cmap='viridis')
        axs[1, 0].set_title("Reflectivity (Predicted)")
        axs[1, 1].imshow(self.predicted_next_step[:, :, 1], cmap='viridis')
        axs[1, 1].set_title("Velocity (Predicted)")
        axs[1, 2].imshow(self.predicted_next_step[:, :, 2], cmap='viridis')
        axs[1, 2].set_title("Total Power (Predicted)")
        
        plt.tight_layout()  # Adjust the layout to prevent overlap
        plt.show()




# Example usage:
if __name__ == '__main__':
    # Step 1: Generate sequences
    data_sequence = DataSequence()
    X, Y = data_sequence.create_sequence()

    # Step 2: Initialize model with X
    model_maker = ModelMaking(X)

    # Step 3: Train the model
    model_maker.train(X, Y)
