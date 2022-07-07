# Hackathon_2022
Muse-generated EEG Data Extraction and Preprocessing.

# Project Description
The Muse headband captures 7 channels of EEG data to detect brain activity and provide real-time biofeedback. The goal of this project will be to create a utility application that will visualize and preprocess the raw data in preparation for further analyses (conduct standard and basic transformations, e.g. averaging over time and Fourier analysis).

![Muse](https://user-images.githubusercontent.com/101252448/177865771-477d0b9a-4058-471c-9345-64fe1965b473.jpg)

# In Short...
* As there are several (very comprehensive) tools for processing raw EEG data, we decided to handle the data Muse creates for the power of each wave band in each electrode.
* We created 3 classes that feed of each other (MuseEEG -> BasicAnalysis -> ComparativeAnalysis) though we tried to allow for some flexibility in that. 
* As we are unsure what researchers might wish to do with the data we aimed to allow multiple analysis possibilities (maintaining the raw data, averaging per second, long form presentation and several other preprocessing steps that can be discarded if not needed).
* We tried to create many basic analysis and graphing possibilities so that a focused researcher will be able to choose the option that suits their needs and expand on it
* We gathered that the relevant PIs lab might wish to compare within-person Muse recording in the future and began building a few different descriptive and statisitc tools. This is still in progress.
* We skimmed the surface with code testing. This is also still in progress.

# SET-UP
```
* Having python 3.7 version is a requierment 
* You need to have a .csv file extracted from an EEG Muse session
* Clone the repository into your integrated development environment
```

# running the analysis
The easiest way of running the analysis is using the **main.py** file

* Run main.py
* Choose the relevant file for the analysis
* the data will run through the class ***MuseEEG*** in **muse_eeg.py**
* Data will be formated for the different analysis possibilities
* A new Folder named **MuseEEG_results** will open in the original file location
* Using funtionalities.py to plot graph of different band/electrode records.
* Using basic_analysis.py to transform the data (into long form) and perform basic analysis (e.g., simple descriptive statistics and visualization, duration calculation and higlighting of specific events) on a single Muse EEG recording
* Using comparative_analysis.py to compare data from multiple experiments/measurements.

# muse_eeg.py
Contains MuseEEG class with the following functions:
- read_data - read the csv into dataframe
- ave_sec - turn data into data per second
- del_first_min - delete the first minute of recording (not valid by definition)
- na_to_zero - turn nan to 0
- create_dir - create a new directory for the results and return the path's name

# functionalities.py
- create_graph_per_electrode
- create_graph_per_wave
- time_correction

# basic_analysis.py
Contains BasicAnalysis class with the following functions:
- new_dir - creates attribute of designated path for analysis output
- time_info - prints the duration of the recording in secs and HH:MM:SS format
- statistics_power - returns df of simple descriptive statistics (mean, std, max) for each wave band power in every second averaged over electrodes as well as a graph of mean power vs. time. Can also be applied to electrodes instead of waves
- highest_band_power - returns df of wave bands' power recording that exceeded an inputted threshold calculated uniquely for each wave band*electrode combo
- band_significance - returns the most powerful band*electrode combo for each second
- specific_band_most_significant - returns the seconds during which a specific band and\or electrode appeared in band_significance, as well as calculating the commonality of that occurence

# comparative_analysis.py
Contains ComparativeAnalysis class with the following functions:

- new_dir - creates attribute of designated path for analysis output
- compare_electrodes - Compare highest band powers for pairwise comparisons of single experiments.
- correlate_data - Calculate correlation coefficient per each band of each electrode, for pairwise comparisons of single experiments. (in progress)
