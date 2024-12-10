import os
import zipfile


class DataIngestor:
    def ingest(self, file_path: str, output_folder: str) -> None:
        """
        Extracts the contents of a zip file into the specified output folder.

        Parameters:
        - file_path (str): Path to the zip file.
        - output_folder (str): Folder where the contents will be extracted.
        """
        if not file_path.endswith(".zip"):
            raise ValueError(f"The provided file '{file_path}' is not a .zip file.")

        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")

        os.makedirs(output_folder, exist_ok=True)  # Ensure the output folder exists

        try:
            with zipfile.ZipFile(file_path, "r") as zip_ref:
                zip_ref.extractall(output_folder)  # Extract all files into the folder
            print(f"Extracted '{file_path}' to '{output_folder}'.")
        except zipfile.BadZipFile:
            raise zipfile.BadZipFile(f"The file '{file_path}' is not a valid zip file.")
        except Exception as e:
            raise Exception(f"An error occurred while processing '{file_path}': {e}")


if __name__ == "__main__":
    ingestor = DataIngestor()

    # Specify the folder containing zip files
    folder_path = "data"
    output_folder = "extracted_files"

    try:
        # Check if the folder exists
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"The folder '{folder_path}' does not exist.")

        # Get a list of filenames in the folder
        filenames = os.listdir(folder_path)

        if not filenames:
            print(f"The folder '{folder_path}' is empty. No files to process.")
            exit()

        # Process each zip file in the folder
        for file in filenames:
            file_path = os.path.join(folder_path, file)
            try:
                ingestor.ingest(file_path, output_folder)
            except ValueError as ve:
                print(f"Skipping file '{file}': {ve}")
            except FileNotFoundError as fnf:
                print(f"Skipping missing file '{file}': {fnf}")
            except zipfile.BadZipFile as bzf:
                print(f"Skipping invalid zip file '{file}': {bzf}")
            except Exception as e:
                print(f"Error processing file '{file}': {e}")

    except FileNotFoundError as fnf_error:
        print(f"Error: {fnf_error}")
    except PermissionError as perm_error:
        print(f"Error: Insufficient permissions to access files. {perm_error}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
