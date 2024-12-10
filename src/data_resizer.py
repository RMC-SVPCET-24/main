import os
import pandas as pd
from data_formatter import DataFormatter
from scipy.ndimage import zoom

class CSVResizerFromList:
    def __init__(self, file_paths, target_shape=(150, 150)):
        self.file_paths = file_paths  # List of file paths
        self.target_shape = target_shape

    def resize_csv(self, file_path):
        try:
            # Load CSV into a numpy array
            data = pd.read_csv(file_path, header=None).values
        except FileNotFoundError as fnf_error:
            print(f"File not found: {file_path}. Error: {fnf_error}")
            return None
        except pd.errors.EmptyDataError:
            print(f"Error: The file {file_path} is empty.")
            return None
        except Exception as e:
            print(f"Error loading file {file_path}: {e}")
            return None  # Return None if there is an error loading the file

        # Ensure data is not empty before resizing
        if data.size == 0:
            print(f"Warning: The file {file_path} is empty.")
            return None

        # Calculate scaling factors
        scale_x = self.target_shape[0] / data.shape[0]
        scale_y = self.target_shape[1] / data.shape[1]

        try:
            # Resize using bilinear interpolation
            resized_data = zoom(data, (scale_x, scale_y), order=1)  # order=1 -> bilinear interpolation
        except Exception as e:
            print(f"Error resizing data from file {file_path}: {e}")
            return None

        return resized_data

    def process_files(self):
        # Process each file in the provided list
        output_paths = []
        for file_path in self.file_paths:
            try:
                file_split_path = file_path.split("/")  # Extract filename
                file_name = file_split_path[-1]  # Get the last element (filename)
                file_dir = file_split_path[-2]  # Get the second to last element (directory name)

                op_dir = os.path.join("/content/WeatherCSV", file_dir)
                os.makedirs(op_dir, exist_ok=True)

                output_file_path = os.path.join(op_dir, file_name)
                resized_data = self.resize_csv(file_path)

                # Check if resizing was successful
                if resized_data is not None:
                    # Save the resized data to the output directory
                    pd.DataFrame(resized_data).to_csv(output_file_path, index=False, header=False)
                    print(f"Resized and saved: {output_file_path}")
                    output_paths.append(output_file_path)
                else:
                    print(f"Skipping saving for {file_path} due to error in resizing.")

            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

        return output_paths
    


class DataResize:
    def __init__(self):
        pass

    def getProcessFile(self):
        try:
            dataSeries = DataFormatter()
            reflectivity_series, total_power_series, velocity_series = dataSeries.getSeriesData()

            if not reflectivity_series:
                print("Warning: No reflectivity data available.")
            if not total_power_series:
                print("Warning: No total power data available.")
            if not velocity_series:
                print("Warning: No velocity data available.")

            resizer = CSVResizerFromList(reflectivity_series, target_shape=(150, 150))
            reflectivity = resizer.process_files()

            resizer = CSVResizerFromList(total_power_series, target_shape=(150 , 150))
            total_power = resizer.process_files()

            resizer = CSVResizerFromList(velocity_series, target_shape=(150, 150))
            velocity = resizer.process_files()

        except Exception as e:
            print(f"Error in getProcessFile: {e}")
            reflectivity, total_power, velocity = [], [], []

        return reflectivity, total_power, velocity


# Example usage
if __name__ == "__main__":
    try:
        # Example list of file paths (you can replace this with actual paths)
        reflectivity_series = [
            "data/DLH230802080226/Reflectivity_2_sweep_1.csv",
            "data/DLH230802081220/Reflectivity_2_sweep_1.csv",
            "data/DLH230802082220/Reflectivity_2_sweep_1.csv",
            # Add more file paths as needed
        ]
        
        # Initialize and process the files
        resizer = CSVResizerFromList(reflectivity_series, target_shape=(150, 150))
        resized_files = resizer.process_files()

    except Exception as e:
        print(f"Error in main execution: {e}")
