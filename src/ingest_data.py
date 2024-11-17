import os
import zipfile
from abc import ABC, abstractmethod
import pandas as pd


class DataIngestor(ABC):
    @abstractmethod
    def ingest(self, file_path: str) -> pd.DataFrame:
        pass

class ZipDataIngestor(DataIngestor):
    def ingest(self, file_path: str) -> pd.DataFrame:
        if not file_path.endswith(".zip"):
            raise ValueError("The provided file is not a .zip file.")
        

        #this is extracting data from zip file
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall("extracted_data")


        extracted_files = os.listdir("extracted_data") # mostly this code is creating dir

        #this line is storing all the csv file into csv file (as name)
        csv_files = [f for f in extracted_files if f.endswith(".csv")]

        
if __name__ == "__main__":
    # Specify the folder path
    folder_path = "C:/Users/Hp/OneDrive/Desktop/Capstone/project/data"

    # Get a list of filenames in the folder
    filenames = os.listdir(folder_path)

    # Print the list of filenames
    print(filenames)


    