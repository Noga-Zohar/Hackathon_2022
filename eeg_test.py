from pathlib import Path
import numpy as np
import pandas as pd
from tkinter.filedialog import askopenfilename
import pytest as pt
from muse_eeg import MuseEEG
from basic_analysis import BasicAnalysis



def main():
    print('enter main')


def test_check_Nan(df):
    assert df.isnull().values.any() == False


def test_empty_df(df):
    assert not df.empty

def test_wrong_input_type():
    data = [1,2,3,4]
    with pt.raises(TypeError):
        q = BasicAnalysis(data)

def test_empty_input():
    data = pd.DataFrame()
    with pt.raises(ValueError):
        q = BasicAnalysis(data)

def test_data_becomes_lf():
    x = MuseEEG()
    x.read_data()
    x.ave_sec()
    q = BasicAnalysis(x.data_per_sec)
    assert q.data.index.names == ['sec','electrode','band']

def test_lf_one_column():
    #check that the long form has only one column - power
    x = MuseEEG()
    x.read_data()
    x.ave_sec()
    q = BasicAnalysis(x.data_per_sec)
    assert list(q.data.columns)==['power'] 

def test_band_wrong_input():
    x = MuseEEG()
    x.read_data()
    x.ave_sec()
    band = "definitelynotabandinthishererecording"
    with pt.raises(ValueError):
        q = BasicAnalysis(x.data_per_sec,band)

def test_stat_power_wrong_input():
    x = MuseEEG()
    x.read_data()
    x.ave_sec()
    q = BasicAnalysis(x.data_per_sec)
    with pt.raises(ValueError):
        q.statistics_powers("this")

def test_stat_power_output_columns():
    x = MuseEEG()
    x.read_data()
    x.ave_sec()
    q = BasicAnalysis(x.data_per_sec)
    df = q.statistics_powers()
    assert list(df.columns)==['mean','std','max']

def test_power_exists():
    x = MuseEEG()
    x.read_data()
    x.ave_sec()
    q = BasicAnalysis(x.data_per_sec)
    df=q.band_significance(value=True)
    assert "power" in df.columns

def test_power_not_exists():
    x = MuseEEG()
    x.read_data()
    x.ave_sec()
    q = BasicAnalysis(x.data_per_sec)
    df=q.band_significance(value=False)
    assert ("power" in df.columns)==False


