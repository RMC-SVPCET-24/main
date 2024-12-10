from data_resizer import DataResize
import pandas as pd
import numpy as np

class LoadPadData:
    
    @staticmethod
    def load_and_pad_data(file_paths, target_columns=150):
        data = []
        for file_path in file_paths:
            try:
                # Attempt to read the CSV file
                df = pd.read_csv(file_path)
                current_columns = df.shape[1]

                # Check if padding is needed
                if current_columns < target_columns:
                    padding_columns = target_columns - current_columns
                    padding = pd.DataFrame(np.nan, index=df.index, columns=[f'NaN_pad_{i+1}' for i in range(padding_columns)])
                    df = pd.concat([df, padding], axis=1)
                elif current_columns > target_columns:
                    df = df.iloc[:, :target_columns]

                # Fill NaN values with 0.0
                df.fillna(0.0, inplace=True)
                data.append(df.values)

            except FileNotFoundError:
                print(f"Error: File not found at {file_path}")
            except pd.errors.EmptyDataError:
                print(f"Error: File is empty at {file_path}")
            except pd.errors.ParserError:
                print(f"Error: Could not parse the file at {file_path}")
            except Exception as e:
                print(f"An unexpected error occurred while processing {file_path}: {e}")

        # Handle case where no data was loaded
        if not data:
            print("Warning: No valid data was loaded.")
            return np.array([])

        return np.array(data)


class DataPreprocessing:
    def __init__(self):
        pass

    def dataPreprocess(self):
        try:
            # Resize data
            resize = DataResize()
            reflectivity, total_power, velocity = resize.getProcessFile()

            # Check if the data lists are empty
            if not reflectivity or not total_power or not velocity:
                raise ValueError("One or more data series are empty. Cannot proceed with preprocessing.")

            # Load and pad the data
            load_pad = LoadPadData()
            reflectivity_preprocessed = load_pad.load_and_pad_data(reflectivity)
            total_power_preprocessed = load_pad.load_and_pad_data(total_power)
            velocity_preprocessed = load_pad.load_and_pad_data(velocity)

            # Ensure data is valid before combining
            if reflectivity_preprocessed.size == 0 or total_power_preprocessed.size == 0 or velocity_preprocessed.size == 0:
                raise ValueError("One or more preprocessed data arrays are empty. Cannot combine data.")

            # Combine the data into a single array
            data_combined = np.stack((reflectivity_preprocessed, velocity_preprocessed, total_power_preprocessed), axis=-1)

        except ValueError as ve:
            print(f"ValueError: {ve}")
            data_combined = None
        except Exception as e:
            print(f"An unexpected error occurred during data preprocessing: {e}")
            data_combined = None

        return data_combined


# Add the __name__ == '__main__' block
if __name__ == '__main__':
    # Example file paths (replace with actual paths to your files)
    reflectivity_series = [
        "data/DLH230802080226/Reflectivity_2_sweep_1.csv",
        "data/DLH230802081220/Reflectivity_2_sweep_1.csv",
        "data/DLH230802082220/Reflectivity_2_sweep_1.csv",
        # Add more file paths as needed
    ]
    
    # Instantiate DataPreprocessing class and process the data
    try:
        preprocess = DataPreprocessing()
        combined_data = preprocess.dataPreprocess()
        
        if combined_data is not None:
            print("Data preprocessing successful.")
        else:
            print("Data preprocessing failed.")

    except Exception as e:
        print(f"An error occurred in the main execution: {e}")




