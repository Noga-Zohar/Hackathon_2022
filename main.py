from muse_eeg import MuseEEG
from basic_analysis import BasicAnalysis
from comparative_analysis import ComparativeAnalysis

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

# comparative analysis

# the following lines should be a list created (in a loop)
# when the user chooses more than one experiment
exp1 = beeg1.band_significance() # beeg = BasicAnalysis object
exp2 = beeg2.band_significance()
exp3 = beeg3.band_significance()
list = [exp1, exp2, exp3]

# create a ComparativeAnalysis object
ceeg = ComparativeAnalysis(list)

# compare highest band powers for pairwise comparisons of single experiments
ceeg.compare_electrodes()

# Calculate correlation coefficient per each band of each electrode,
# for pairwise comparisons of single experiments
ceeg.correlate_data()

