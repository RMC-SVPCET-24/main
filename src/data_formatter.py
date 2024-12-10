import data_gathering


class DataFormatter:
    def __init__(self):
        pass

    def arange_data(self, data):
        """
        Rearranges data into sequential frames to assist in forming video-like sequences.

        Parameters:
        - data (list): List of data points to arrange.

        Returns:
        - List: Rearranged list in the desired sequence.
        """
        if not isinstance(data, list):
            raise TypeError("The input data must be a list.")

        if not data:
            raise ValueError("The input data list is empty.")

        try:
            a, b, c, d, e, f, g, h, i, j = (
                list(),
                list(),
                list(),
                list(),
                list(),
                list(),
                list(),
                list(),
                list(),
                list(),
            )
            for ind, value in enumerate(data, 1):
                if ind % 10 == 1:
                    a.append(value)
                elif ind % 10 == 2:
                    b.append(value)
                elif ind % 10 == 3:
                    c.append(value)
                elif ind % 10 == 4:
                    d.append(value)
                elif ind % 10 == 5:
                    e.append(value)
                elif ind % 10 == 6:
                    f.append(value)
                elif ind % 10 == 7:
                    g.append(value)
                elif ind % 10 == 8:
                    h.append(value)
                elif ind % 10 == 9:
                    i.append(value)
                elif ind % 10 == 0:
                    j.append(value)
            return [*a, *b, *c, *d, *e, *f, *g, *h, *i, *j]
        except Exception as e:
            raise Exception(f"An error occurred while rearranging data: {e}")

    def getSeriesData(self):
        """
        Retrieves and arranges data series for reflectivity, total power, and velocity.

        Returns:
        - Tuple: Three lists containing arranged data series.
        """
        try:
            dataGather = data_gathering.DataGathering()

            # Attempt to retrieve files from directory
            try:
                dataGather.gotoDir()
            except Exception as e:
                raise Exception(f"Error navigating directory: {e}")

            # Attempt to gather data
            try:
                reflectivity_data, total_power_data, velocity_data = dataGather.getData()
            except Exception as e:
                raise Exception(f"Error gathering data: {e}")

            # Validate and arrange each dataset
            try:
                reflectivity_series = self.arange_data(reflectivity_data)
            except Exception as e:
                print(f"Error arranging reflectivity data: {e}")
                reflectivity_series = []

            try:
                total_power_series = self.arange_data(total_power_data)
            except Exception as e:
                print(f"Error arranging total power data: {e}")
                total_power_series = []

            try:
                velocity_series = self.arange_data(velocity_data)
            except Exception as e:
                print(f"Error arranging velocity data: {e}")
                velocity_series = []

            return reflectivity_series, total_power_series, velocity_series

        except Exception as e:
            print(f"An unexpected error occurred in getSeriesData: {e}")
            return [], [], []


if __name__ == "__main__":
    try:
        # Create an instance of DataFormatter
        data_formatter = DataFormatter()

        # Call getSeriesData to process and arrange data
        print("Processing data...")
        reflectivity_series, total_power_series, velocity_series = data_formatter.getSeriesData()

        # Output results
        if reflectivity_series:
            print(f"Processed Reflectivity Series: {len(reflectivity_series)} items")
        else:
            print("No reflectivity data processed.")

        if total_power_series:
            print(f"Processed Total Power Series: {len(total_power_series)} items")
        else:
            print("No total power data processed.")

        if velocity_series:
            print(f"Processed Velocity Series: {len(velocity_series)} items")
        else:
            print("No velocity data processed.")

    except Exception as e:
        print(f"An unexpected error occurred in the main block: {e}")
