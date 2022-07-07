import pathlib
from pathlib import Path
import numpy as np
import pandas as pd
from tkinter.filedialog import askopenfilename
import pytest as pt


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
        str_path = str(self.filepath)
        if not (str_path.endswith('.csv') == True):
            raise Exception('This is no CSV file')
        self.data = pd.read_csv(self.filepath, infer_datetime_format=True)  # read the data
        c_list = ['TimeStamp', 'Delta_TP9', 'Delta_AF7', 'Delta_AF8', 'Delta_TP10', 'Theta_TP9', 'Theta_AF7',
                    'Theta_AF8', 'Theta_TP10', 'Alpha_TP9', 'Alpha_AF7', 'Alpha_AF8', 'Alpha_TP10', 'Beta_TP9',
                    'Beta_AF7', 'Beta_AF8', 'Beta_TP10', 'Gamma_TP9', 'Gamma_AF7',
                    'Gamma_AF8', 'Gamma_TP10']
        i = 0
        for col in c_list:
            if col not in self.data.columns:
                i = +1
        print
        if i>0:
            raise Exception("some band columns do not exist")
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
        if len(self.data_per_sec) < 61:
            raise Exception('data is less than a minute long, therefore not valid')
        df = self.data_per_sec.iloc[m * 60:, :]  # m*60 is the number of seconds AKA number of rows to delete
        df.reset_index()  # update the indexes
        self.data_per_sec = df  # update data_per_sec

    def na_to_zero(self) -> None:
        """
        turning NaN vals in dataframe into 0
        :return:
        """
        self.data_per_sec = self.data_per_sec.fillna(0)

    def create_dir(self) ->pathlib.Path:
        """
        creates a directory for future results in the same location as analyzed csv file. Use of self.dir
        :return: Path object, for the results directory
        """
        path = Path(self.dir + '/MuseEEG_results/')
        path.mkdir(parents=True, exist_ok=True)
        return path




if __name__ == "__main__":
    import eeg_test as tst
    temp = MuseEEG()
    temp.read_data()
    temp.ave_sec()
    temp.del_first_min()
    temp.na_to_zero()
    test_functions = ["test_check_Nan", "test_empty_df"]  # list of function names
    errors = []
    for func in test_functions:
        try:
            f = getattr(tst, func) # tst.check_Nan
            f(temp.data_per_sec)
        except Exception as e:
            errors.append(f"Failed when testing method '{func}'")
    if len(errors) > 0:
        print(errors)
    else:
        print("Tests pass successfully.")