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
eeg.del_first_min()

# transform Nan rdata values into zeroes (eeg.data_per_sec)
eeg.na_to_zero()

# create and return new directory for the result files, in the same folder as the original file
new_path = eeg.create_dir()


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