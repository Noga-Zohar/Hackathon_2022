from pathlib import Path
import numpy as np
import pandas as pd
from tkinter.filedialog import askopenfilename
import datetime as dt


class MuseEEG:
    """
    Class museEEG is for representing and editing the muse EEG data, before analyzing it
    """

    def __init__(self):
        self.band_ave = None
        self.rdata = None  # for read_data
        self.data = None  # for read_data
        self.data_per_sec = None  # for the ave_sec function
        filepath = askopenfilename()  # pop up - choose a file
        self.filepath = Path(filepath)  # pathlib.Path instance
        self.dir = str(self.filepath.parent)

    def read_data(self) -> None:
        """
        read the file into self.data as dataframe, read only the relevant electrode_wave columns into self.rdata
        :return: None
        Assign self.data, self.rdata
        """
        # read the file into self.data
        self.data = pd.read_csv(self.filepath, infer_datetime_format=True)  # read the data
        rdata = self.data[['TimeStamp', 'Delta_TP9', 'Delta_AF7', 'Delta_AF8', 'Delta_TP10', 'Theta_TP9', 'Theta_AF7',
                           'Theta_AF8', 'Theta_TP10', 'Alpha_TP9', 'Alpha_AF7', 'Alpha_AF8', 'Alpha_TP10', 'Beta_TP9',
                           'Beta_AF7', 'Beta_AF8', 'Beta_TP10', 'Gamma_TP9', 'Gamma_AF7',
                           'Gamma_AF8', 'Gamma_TP10']].copy()  # read the relevant columns into rdata
        self.rdata = rdata  # assign rdata variable to class

    def ave_sec(self) -> None:
        """
        Turn the rdata from data per seconds fractions to rdata per seconds. Average all column for each second.
        Additionally, since negative values mean more noise than signal, turn all negative vals to nan.
        :return: None.
        Assign data_per_sec
        """
        df = self.rdata  # temporary data
        df['Time'] = pd.to_datetime(df['TimeStamp'])  # Time is a new column with time as datetime
        df['Time'] = df['Time'].dt.round(freq='S')  # round all time by seconds
        dff = df[['Delta_TP9', 'Delta_AF7', 'Delta_AF8', 'Delta_TP10', 'Theta_TP9', 'Theta_AF7',
                  'Theta_AF8', 'Theta_TP10', 'Alpha_TP9', 'Alpha_AF7', 'Alpha_AF8', 'Alpha_TP10', 'Beta_TP9',
                  'Beta_AF7', 'Beta_AF8', 'Beta_TP10', 'Gamma_TP9', 'Gamma_AF7',
                  'Gamma_AF8', 'Gamma_TP10']]
        dff = dff.abs()
        df[['Delta_TP9', 'Delta_AF7', 'Delta_AF8', 'Delta_TP10', 'Theta_TP9', 'Theta_AF7',
            'Theta_AF8', 'Theta_TP10', 'Alpha_TP9', 'Alpha_AF7', 'Alpha_AF8', 'Alpha_TP10', 'Beta_TP9',
            'Beta_AF7', 'Beta_AF8', 'Beta_TP10', 'Gamma_TP9', 'Gamma_AF7',
            'Gamma_AF8', 'Gamma_TP10']] = dff
        calc_df = df.groupby('Time').mean()  # group all columns by the same time (seconds accuracy), new val is mean
        self.data_per_sec = calc_df  # self.data_per_sec is the new table

    def del_first_min(self, m: int = 1) -> None:
        """
        Delete the first m minutes from the dataset. Since the first minute of every recording is invalid m default as 1
        :param m: int- number of minutes
        :return: None
        :Update self.data_per_second
        """
        df = self.data_per_sec.iloc[m * 60:, :]  # m*60 is the number of seconds AKA number of rows to delete
        df.reset_index()  # update the indexes
        self.data_per_sec = df  # update data_per_sec

    def na_to_zero(self):
        self.data_per_sec = self.data_per_sec.fillna(0)

    def el_mean(self):
        df = self.data_per_sec['Time']
        df['alpha'] = df[['Alpha_TP9', 'Alpha_AF7', 'Alpha_AF8', 'Alpha_TP10']].mean(axis=1)
        df['beta'] = df[['Beta_TP9', 'Beta_AF7', 'Beta_AF8', 'Beta_TP10']].mean(axis=1)
        df['gamma'] = df[['Gamma_TP9', 'Gamma_AF7', 'Gamma_AF8', 'Gamma_TP10']].mean(axis=1)
        df['delta'] = df[['Delta_TP9', 'Delta_AF7', 'Delta_AF8', 'Delta_TP10']].mean(axis=1)
        df['theta'] = df[['Theta_TP9', 'Theta_AF7', 'Theta_AF8', 'Theta_TP10']].mean(axis=1)
        self.band_ave = df
        return df

    def create_dir(self):
        path = Path(self.dir + '/MuseEEG_results/')
        path.mkdir(parents=True, exist_ok=True)
        return path


 # checking the output
# x = MuseEEG()
# x.read_data()
# data_top = x.data.head()
# print(data_top)
# t = x.data.dtypes
# print(t)
# print(x.rdata.head())
