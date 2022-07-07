from muse_eeg import MuseEEG

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
