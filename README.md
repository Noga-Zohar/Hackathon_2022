# Hackathon_2022
Muse-generated EEG Data Extraction and Preprocessing.

# Project Description
The Muse headband captures 7 channels of EEG data to detect brain activity and provide real-time biofeedback. The goal of this project will be to create a utility application that will visualize and preprocess the raw data in preparation for further analyses (conduct standard and basic transformations, e.g. averaging over time and Fourier analysis).

![Muse](https://user-images.githubusercontent.com/101252448/177865771-477d0b9a-4058-471c-9345-64fe1965b473.jpg)

# Functionalties
The application is able to read the data and preprocess it (removal of nan, changing values to absolute values, averaging power per second) as well as transform it (into long form) and perform basic analysis (e.g., simple descriptive statistics and visualization, duration calculation and higlighting of specific events) on a single Muse EEG recording (mainly the absolute power recordings.
In addition the application can also make simple comparisons between large numbers of different recordings, comparing the most powerful recording cell at each second and performing correlations (in work).

# Classes
The application is comprised of 3 classes:
    - MuseEEG - reads and preprocesses data (the function functionalities can use the data from this class to immediately make simple graphs)
    - BasicAnalysis - performs several types of analysis on one recording, as well as visualization
    - ComparativeAnalysis - compares between 2 or more recordings

