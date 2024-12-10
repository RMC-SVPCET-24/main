import os

class DataGathering:

    def __init__(self):
        self.all_files = list()

    def gotoDir(self):
        try:
            
            # Ensure the directory exists
            if not os.path.exists('extracted_files'):
                raise FileNotFoundError("The directory 'extracted_files' does not exist.")
            
            # List all files and directories in 'extracted_files'
            for file in os.listdir(r'extracted_files'):
                self.all_files.append(file)
            
            # Remove '.git' if present
            if '.git' in self.all_files:
                self.all_files.remove('.git')
            
            # Sort the list of files/directories
            self.all_files.sort()

        except FileNotFoundError as fnf_error:
            print(f"Error: {fnf_error}")
        except PermissionError as perm_error:
            print(f"Error: Insufficient permissions to access the directory. {perm_error}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def getData(self):
        reflectivity_data = list()
        total_power_data = list()
        velocity_data = list()

        dir = r'extracted_files'

        try:
            # Ensure the directory exists before proceeding
            if not os.path.exists(dir):
                raise FileNotFoundError(f"The directory '{dir}' does not exist.")

            for _file in self.all_files:
                file_path = os.path.join(dir, _file)
                
                # Check if the path is a directory
                if not os.path.isdir(file_path):
                    print(f"Skipping '{_file}' as it is not a directory.")
                    continue

                for i in range(1, 11):
                    # Generate file paths and add them to respective lists
                    reflectivity_file = os.path.join(file_path, f'Reflectivity_2_sweep_{i}.csv')
                    total_power_file = os.path.join(file_path, f'TotalPower_2_sweep_{i}.csv')
                    velocity_file = os.path.join(file_path, f'Velocity_2_sweep_{i}.csv')

                    # Verify if the files exist before appending
                    if os.path.exists(reflectivity_file):
                        reflectivity_data.append(reflectivity_file)
                    else:
                        print(f"Warning: File '{reflectivity_file}' not found.")

                    if os.path.exists(total_power_file):
                        total_power_data.append(total_power_file)
                    else:
                        print(f"Warning: File '{total_power_file}' not found.")

                    if os.path.exists(velocity_file):
                        velocity_data.append(velocity_file)
                    else:
                        print(f"Warning: File '{velocity_file}' not found.")

        except FileNotFoundError as fnf_error:
            print(f"Error: {fnf_error}")
        except PermissionError as perm_error:
            print(f"Error: Insufficient permissions to access files. {perm_error}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        return reflectivity_data, total_power_data, velocity_data

if __name__ == '__main__':
    # Example usage
    data_gathering = DataGathering()
    data_gathering.gotoDir()  # Prepare the directory list
    reflectivity, total_power, velocity = data_gathering.getData()  # Gather data

    # Print the results
    print("Reflectivity Files:", reflectivity)
    print("Total Power Files:", total_power)
    print("Velocity Files:", velocity)
