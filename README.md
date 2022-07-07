# Hackathon_2022
Muse-generated EEG Data Extraction and Preprocessing.

# Project Description
The Muse headband captures 7 channels of EEG data to detect brain activity and provide real-time biofeedback. The goal of this project will be to create a utility application that will visualize and preprocess the raw data in preparation for further analyses (conduct standard and basic transformations, e.g. averaging over time and Fourier analysis).

![Muse](https://user-images.githubusercontent.com/101252448/177865771-477d0b9a-4058-471c-9345-64fe1965b473.jpg)

# In Short...
* We decided

# SET-UP
```
* Having python XXX version is a requierment 
* You need to have a .csv file extracted from an EEG Muse session
* Clone the repository into your integrated development environment
* ?
```

# running the analysis
The easiest way of running the analysis is using the **main.py** file

* Run main.py
* Choose the relevant file for the analysis
* the data will run through the class ***MuseEEG*** in **muse_eeg.py**
* Data will be formated for the different analysis possibilities
* A new Folder named **MuseEEG_results** will open in the original file location
* Using funtionalities.py to **XXX**
* Using basic_analysis.py to **XXX**
* Using comparative analysis.py to **XXX**

# muse_eeg.py
Contains MuseEEG class with the following functions:
- read_data - read the csv into dataframe
- ave_sec - turn data into data per second
- del_first_min - delete the first minute of recording (not valid by definition)
- na_to_zero - turn nan to 0
- create_dir - create a new directory for the results and return the path's name

# functionalities.py
Contains MuseEEG class with the following functions:
- safaf
- fSGAG
- FSDFA

# basic_analysis.py
Contains MuseEEG class with the following functions:
- safaf
- fSGAG
- FSDFA

# comparative analysis.py
Contains MuseEEG class with the following functions:
- safaf
- fSGAG
- FSDFA
