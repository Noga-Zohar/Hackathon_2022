#----------------------------------------------------------------------------
#                              Hackathon 2022
#            Muse-generated EEG Data Extraction and Preprocessing.
#
# Created By: Itai Caspit, Inbal Kuperwasser, Noga Zohar,
#               Ben Zion Haddad, Uri Bertocchi
#----------------------------------------------------------------------------

# imports
from subprocess import TimeoutExpired
from muse_eeg import MuseEEG
from basic_analysis import BasicAnalysis
from comparative_analysis import ComparativeAnalysis
from comparative_analysis import InputError
from functionalities import *
from pathlib import Path

#from functions import call_muse_eeg
#from functions import call_basic_analysis
#from functions import call_compare_analysis
#from functions import call_graphs

# main script

# create an MuseEEG object
eeg = MuseEEG()
# read the chosen csv file into eeg.data, and place only the relevant rows for band information into rdata
eeg.read_data()
# transform the rdata values from fractions of seconds into their average (per second). negative values into positive.
# new data is now on eeg.data_per_sec
eeg.ave_sec()
# delete the first minute of recorded data (non-valid). Can input specified minutes instead (eeg.data_per_sec)
#eeg.del_first_min()
# transform Nan rdata values into zeroes (eeg.data_per_sec)
eeg.na_to_zero()
# create and return new directory for the result files, in the same folder as the original file
new_path = eeg.create_dir()

# create a long-form version of the data (which is averaged per second)
# saves data to result files under "long_form_eeg.csv"
# it is possible (but not mandated) to also input a band and/or electrode of interest
# it is also possible to use this class for recordings with different bands and electrodes
lf_eeg = BasicAnalysis(eeg.data_per_sec,relevant_band="Alpha",relevant_electrode="TP9")
lf_eeg.new_dir(new_path)
# get information regarding the duration of recording
lf_eeg.time_info()
# create a df with statistic info (mean, std, max) of every band for each second of the recording across electrodes
# this also creates a pop-up graph of mean power [bell] vs. time [sec] for all the bands
# saves data to result files under "statistics_powers_band.csv"
# save graph to result file under "plot_mean_band.png"
lf_eeg.statistics_powers()
# an identical version for the electrodes rather than the bands
lf_eeg.statistics_powers("electrode")
# create a df for seconds in which a recording is above a certain threshold (mean+x*std). x is defaulted to 2
# the threshold is calculated individually for each recording channel (i.e. band+electrode combination)
# save df to result file under "above_threshold_power.csv"
lf_eeg.highest_band_powers()
# create a df displaying the most powerful band-electrode combination for each second
# if argument values == False the df id returned without the values of power
# save df to result file under "most_powerful_point.csv"
lf_eeg.band_significance()
# create a df higlighting the seconds in which the band and/or electrode specified where part of the most powerful band-electrode combo
# # save df to result file under "relevant_peaks.csv"
lf_eeg.specific_band_most_significant()

# save few basic graphs
create_graph_per_electrode(df=eeg.data, electrode_name='AF7', fig_path=Path(new_path) / 'AF7.png')
create_graph_per_electrode(df=eeg.data, electrode_name='AF8', fig_path=Path(new_path) / 'AF8.png')
create_graph_per_electrode(df=eeg.data, electrode_name='TP9', fig_path=Path(new_path) / 'TP9.png')
create_graph_per_electrode(df=eeg.data, electrode_name='TP10', fig_path=Path(new_path) / 'TP10.png')

create_graph_per_wave(df=eeg.data, wave_length='Delta', fig_path=Path(new_path) / 'Delta.png')
create_graph_per_wave(df=eeg.data, wave_length='Alpha', fig_path=Path(new_path) / 'Alpha.png')
create_graph_per_wave(df=eeg.data, wave_length='Beta', fig_path=Path(new_path) / 'Beta.png')
create_graph_per_wave(df=eeg.data, wave_length='Theta', fig_path=Path(new_path) / 'Theta.png')
create_graph_per_wave(df=eeg.data, wave_length='Gamma', fig_path=Path(new_path) / 'Gamma.png')


# list for testing ComparativeAnalysis
list = [lf_eeg, lf_eeg]

# create a ComparativeAnalysis object
ca_eeg = ComparativeAnalysis(list)
# create new dir
ca_eeg.new_dir(new_path)
# compare highest band powers for pairwise comparisons of single experiments
ca_eeg.compare_electrodes()
# Calculate correlation coefficient per each band of each electrode,
# for pairwise comparisons of single experiments
#ca_eeg.correlate_data() #this is not yet operational (midnight problems), but the underlying code can be seen in ComparativeAnalysis

# ---------------------------------------------------------------------

# the following block is commented because of
# a minor issue with the conditions

# list = []
# # prompt user to choose between a basic analysis (single experiment)
# # or a comparative analysis (multiple experiments)
# prompt = 'How many experiments would you like to test?\n> '
# user_input = input(prompt)
# user_input = int(user_input)

# # single experiment
# if user_input == 1:
#     eeg, new_path = call_muse_eeg()
#     call_graphs(eeg, new_path)
#     call_basic_analysis(eeg, new_path)

# # multiple experiments
# elif user_input >= 2:
#     for experiment in range(user_input):
#         eeg, new_path = call_muse_eeg()
#         call_graphs(eeg, new_path)
#         entry = call_basic_analysis(eeg, new_path)
#         list.append(entry)
#         ca_eeg = call_compare_analysis(list, new_path)
#     pass
# else:
#     raise InputError('Incorrect input.')