from pathlib import Path
import numpy as np
import pandas as pd
from tkinter.filedialog import askopenfilename
import pytest as pt


def main():
    print('enter main')


def test_check_Nan(df):
    assert df.isnull().values.any() == False


def test_empty_df(df):
    assert not df.empty


