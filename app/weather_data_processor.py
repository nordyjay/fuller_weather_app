import pandas as pd
from pathlib import Path
import sys 

import sys



class CSVReader:
    """
    Returns a concatenated data frame of all csv in the specified directory
    """

    def __init__(self):
        #self.path = path
        self.dir = Path('/usr/src/app/weather_data/')
        print(self.dir)
        self.build_df()
        self.check_index()
        self.drop_columns = [
            "Longitude (x)",
            "Latitude (y)",
            "Date/Time",
            "Year",
            "Month",
            "Day",
            "Time",
            "Temp Flag",
            "Dew Point Temp Flag",
            "Rel Hum Flag",
            "Wind Dir Flag",
            "Wind Spd Flag",
            "Visibility Flag",
            "Stn Press Flag",
            "Hmdx Flag",
            "Wind Chill Flag",
        ]
        self.preprocess_and_drop()

    def build_df(self):
        self.df = (pd.read_csv(f) for f in self.dir.glob("*.csv"))
        self.df = pd.concat(self.df)

        return self.df

    def check_index(self):
        if isinstance(self.df.index, pd.DatetimeIndex) == True:
            pass
        else:
            self.df.index = pd.to_datetime(self.df["Date/Time"])
        return self.df

    def preprocess_and_drop(self):
        self.df.drop(columns=self.drop_columns, axis=1, inplace=True)
        self.df["Hmdx"].fillna(0, inplace=True)
        self.df["Wind Chill"].fillna(0, inplace=True)
        self.df["Weather"].fillna(0, inplace=True)
        self.df.dropna(inplace=True)

        return self.df
