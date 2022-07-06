from pathlib import Path
import pandas as pd
from tkinter.filedialog import askopenfilename
import datetime as dt


class MuseEEG:
    def __init__(self):
        self.rdata = None  # for read_data
        self.data = None  # for read_data
        self.data_per_sec = None  # for the ave_sec function
        filepath = askopenfilename()  # pop up - choose a file
        self.filepath = Path(filepath)  # pathlib.Path instance

    def read_data(self):  # read the file into self.data
        self.data = pd.read_csv(self.filepath,  infer_datetime_format=True)  # read the data
        rdata = self.data[['TimeStamp', 'Delta_TP9', 'Delta_AF7', 'Delta_AF8', 'Delta_TP10', 'Theta_TP9', 'Theta_AF7',
                           'Theta_AF8', 'Theta_TP10', 'Alpha_TP9', 'Alpha_AF7', 'Alpha_AF8', 'Alpha_TP10', 'Beta_TP9',
                           'Beta_AF7', 'Beta_AF8', 'Beta_TP10', 'Gamma_TP9', 'Gamma_AF7',
                           'Gamma_AF8', 'Gamma_TP10']].copy()  # read the relevant columns into rdata
        self.rdata = rdata  # assign rdata variable to class

    def ave_sec(self):
        df = self.rdata  # temporary data
        df['Time'] = pd.to_datetime(df['TimeStamp'])  # Time is a new column with time as datetime
        df['Time'] = df['Time'].dt.round(freq='S')  # round all time by seconds
        calc_df = df.groupby('Time').mean()  # group all columns by the same time (seconds accuracy), new val is mean
        print(calc_df)  # just for sanity check- delete row later
        self.data_per_sec = calc_df  # self.data_per_sec is the new table

    def del_first_min(self, m: int = 1):  # Since the first recorded minute is not valid- delete m first minutes
        df = self.data_per_sec.iloc[m*60:, :]  # m*60 is the number of seconds AKA number of rows to delete
        df.reset_index()  # update the indexes
        self.data_per_sec = df  # update data_per_sec


# checking the output
x = MuseEEG()
x.read_data()
data_top = x.data.head()
print(data_top)
t = x.data.dtypes
print(t)
print(x.rdata.head())
