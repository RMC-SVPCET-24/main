import numpy as np
from sklearn.preprocessing import MinMaxScaler
from data_preprocess import DataPreprocessing

class DataScaling:

    def __init__(self):
        try:
            dataPre = DataPreprocessing()
            self.data = dataPre.dataPreprocess()

            # Check if the data is valid
            if self.data is None or self.data.size == 0:
                raise ValueError("Preprocessed data is invalid or empty.")

            self.scaler = MinMaxScaler()

        except ValueError as ve:
            print(f"ValueError in initialization: {ve}")
            self.data = None
            self.scaler = None
        except Exception as e:
            print(f"An unexpected error occurred during initialization: {e}")
            self.data = None
            self.scaler = None

    def scale_data(self):
        try:
            if self.data is None:
                raise ValueError("Data is not initialized correctly. Cannot scale data.")

            shape = self.data.shape
            data_reshaped = self.data.reshape(-1, shape[-1])

            # Perform scaling
            data_scaled = self.scaler.fit_transform(data_reshaped).reshape(shape)
            return data_scaled

        except ValueError as ve:
            print(f"ValueError in scaling data: {ve}")
            return None
        except AttributeError as ae:
            print(f"AttributeError in scaling data: {ae}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred during scaling: {e}")
            return None

    def inverse_scale(self):
        try:
            if self.data is None:
                raise ValueError("Data is not initialized correctly. Cannot inverse scale data.")

            shape = self.data.shape
            data_reshaped = self.data.reshape(-1, shape[-1])

            # Perform inverse scaling
            data_inverse_scaled = self.scaler.inverse_transform(data_reshaped).reshape(shape)
            return data_inverse_scaled

        except ValueError as ve:
            print(f"ValueError in inverse scaling data: {ve}")
            return None
        except AttributeError as ae:
            print(f"AttributeError in inverse scaling data: {ae}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred during inverse scaling: {e}")
            return None


